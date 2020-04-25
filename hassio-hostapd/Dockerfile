ARG BUILD_FROM
FROM $BUILD_FROM

MAINTAINER João Loureiro <joaofl@gmail.com>

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV LANG C.UTF-8

# Install requirements for add-on
RUN apk update && apk add --no-cache bash jq iw linux-firmware-other hostapd networkmanager net-tools sudo && rm -rf /var/cache/apk/*

RUN touch /etc/network/interfaces
COPY hostapd.conf /
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
