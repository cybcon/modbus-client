FROM alpine:3.21.0 AS base
RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.12.8-r1 \
       py3-pip=24.3.1-r0 \
    # Cleanup APK
    && rm -rf /var/cache/apk/* /tmp/* /var/tmp/*



# Compiling python modules
FROM base AS builder
RUN apk add --no-cache --update \
      g++=14.2.0-r4 \
      python3-dev=3.12.8-r1 \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h
COPY --chown=root:root FloatToHex /FloatToHex

WORKDIR /FloatToHex

RUN python3 setup.py install




# Building the docker image with already compiled modules
FROM base
LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.0.16"

COPY --from=builder /usr/lib/python3.12/site-packages /usr/lib/python3.12/site-packages

RUN apk add --no-cache --update \
      libstdc++=14.2.0-r4 \
      py3-wheel=0.43.0-r0 \
      py3-pandas=2.2.3-r0

COPY --chown=root:root /src /

RUN pip3 install --no-cache-dir -r /requirements.txt --break-system-packages

USER 3748:3748

# Start Server
ENTRYPOINT ["python", "-u", "/app/modbus_client.py"]
