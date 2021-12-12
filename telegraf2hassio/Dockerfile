ARG BUILD_FROM
FROM $BUILD_FROM

MAINTAINER João Loureiro <joaofl@gmail.com>

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV LANG C.UTF-8

# Install requirements for add-on
RUN apk update && apk add --no-cache bash python3 py3-pip  && \
                            rm -rf /var/cache/apk/*

RUN pip3 install paho-mqtt

COPY source/* /opt/telegraf2hassio/
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
