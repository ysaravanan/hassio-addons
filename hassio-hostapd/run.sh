#!/bin/bash

# SIGTERM-handler this funciton will be executed when the container receives the SIGTERM signal (when stopping)
reset_interfaces(){
    ifdown $INTERFACE
    sleep 1
    ip link set $INTERFACE down
    ip addr flush dev $INTERFACE
}

term_handler(){
    echo "Resseting interfaces"
    reset_interfaces
    echo "Stopping..."
    exit 0
}

# Setup signal handlers
trap 'term_handler' SIGTERM

echo "Starting..."

CONFIG_PATH=/data/options.json

SSID=$(jq --raw-output ".ssid" $CONFIG_PATH)
WPA_PASSPHRASE=$(jq --raw-output ".wpa_passphrase" $CONFIG_PATH)
CHANNEL=$(jq --raw-output ".channel" $CONFIG_PATH)
ADDRESS=$(jq --raw-output ".address" $CONFIG_PATH)
NETMASK=$(jq --raw-output ".netmask" $CONFIG_PATH)
BROADCAST=$(jq --raw-output ".broadcast" $CONFIG_PATH)
INTERFACE=$(jq --raw-output ".interface" $CONFIG_PATH)
ALLOW_INTERNET=$(jq --raw-output ".allow_internet" $CONFIG_PATH)
DHCP_SERVER=$(jq --raw-output ".enable_dhcp" $CONFIG_PATH)

# Enforces required env variables
required_vars=(SSID WPA_PASSPHRASE CHANNEL ADDRESS NETMASK BROADCAST)
for required_var in "${required_vars[@]}"; do
    if [[ -z ${!required_var} ]]; then
        echo >&2 "Error: $required_var env variable not set."
        exit 1
    fi
done


INTERFACES_AVAILABLE="$(ifconfig -a | grep wl | cut -d ' ' -f '1')"
UNKNOWN=true

if [[ -z ${INTERFACE} ]]; then
        echo >&2 "Network interface not set. Please set one of the available:"
        echo >&2 "${INTERFACES_AVAILABLE}"
        exit 1
fi

for OPTION in ${INTERFACES_AVAILABLE}; do
    if [[ ${INTERFACE} == ${OPTION} ]]; then
        UNKNOWN=false
    fi 
done

if [[ ${UNKNOWN} == true ]]; then
        echo >&2 "Unknown network interface ${INTERFACE}. Please set one of the available:"
        echo >&2 "${INTERFACES_AVAILABLE}"
        exit 1
fi

echo "Set nmcli managed no"
nmcli dev set ${INTERFACE} managed no

echo "Network interface set to ${INTERFACE}"

# Setup hostapd.conf
HCONFIG="/hostapd.conf"

echo "Setup hostapd ..."
echo "ssid=${SSID}" >> ${HCONFIG}
echo "wpa_passphrase=${WPA_PASSPHRASE}" >> ${HCONFIG}
echo "channel=${CHANNEL}" >> ${HCONFIG}
echo "interface=${INTERFACE}" >> ${HCONFIG}
echo "" >> ${HCONFIG}

# Setup interface
IFFILE="/etc/network/interfaces"

echo "Setup interface ..."
echo "" > ${IFFILE}
echo "iface ${INTERFACE} inet static" >> ${IFFILE}
echo "  address ${ADDRESS}" >> ${IFFILE}
echo "  netmask ${NETMASK}" >> ${IFFILE}
echo "  broadcast ${BROADCAST}" >> ${IFFILE}
echo "" >> ${IFFILE}

echo "Resseting interfaces"
reset_interfaces
ifup ${INTERFACE}
sleep 1

if test ${DHCP_SERVER} = true; then
    DHCP_CONFIG="/etc/udhcpd.conf"
    echo "Starting DHCP server..."
    echo "interface ${INTERFACE}" >> ${DHCP_CONFIG}
    echo "udhcpd config:"
    cat ${DHCP_CONFIG}
    echo ""    
    udhcpd -f &
fi

if test ${ALLOW_INTERNET} = true; then
    echo "Configuring IP tables for NAT"
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    iptables -A FORWARD -i eth0 -o ${INTERFACE} -m state --state RELATED,ESTABLISHED -j ACCEPT
    iptables -A FORWARD -i ${INTERFACE} -o eth0 -j ACCEPT
else
    echo "Disabling NAT"
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    iptables -A FORWARD -i eth0 -o ${INTERFACE} -m state --state RELATED,ESTABLISHED -j DROP
    iptables -A FORWARD -i ${INTERFACE} -o eth0 -j DROP
fi

sleep 2

echo "Starting HostAP daemon ..."
hostapd ${HCONFIG} &

while true; do 
    echo "Interface stats:"
    ifconfig | grep ${INTERFACE} -A5
    sleep 60
done
