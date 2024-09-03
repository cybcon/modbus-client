FROM alpine:3.18.8 AS base
RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.11.8-r1 \
       py3-pip=23.1.2-r0 \
    # Cleanup APK
    && rm -rf /var/cache/apk/* /tmp/* /var/tmp/*



# Compiling python modules
FROM base as builder
RUN apk add --no-cache --update \
      g++=12.2.1_git20220924-r10 \
      python3-dev=3.11.8-r1 \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h
COPY --chown=root:root FloatToHex /FloatToHex

WORKDIR /FloatToHex

RUN python3 setup.py install




# Building the docker image with already compiled modules
FROM base
LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.0.15"

COPY --from=builder /usr/lib/python3.11/site-packages /usr/lib/python3.11/site-packages

RUN apk add --no-cache --update \
      libstdc++=12.2.1_git20220924-r10 \
      py3-wheel=0.40.0-r1 \
      py3-pandas=1.5.3-r1

COPY --chown=root:root /src /

RUN pip3 install --no-cache-dir -r /requirements.txt

USER 3748:3748

# Start Server
ENTRYPOINT ["python", "-u", "/app/modbus_client.py"]
