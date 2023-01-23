FROM python:3.10.9-alpine3.17 AS base
RUN apk upgrade --available --no-cache --update \
    && /usr/local/bin/python -m pip install --upgrade pip

# Compiling python modules
FROM base as builder
RUN apk add --no-cache \
      g++=12.2.1_git20220924-r4 \
      python3-dev=3.10.9-r1 \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h
COPY FloatToHex /FloatToHex
WORKDIR /FloatToHex
RUN python3 setup.py install

# Building the docker image with already compiled modules
FROM base
LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.vendor="Michael Oberdorf IT-Consulting"
LABEL site.local.os.main="Linux"
LABEL site.local.os.dist="Alpine"
LABEL site.local.os.version="3.17"
LABEL site.local.runtime.name="Python"
LABEL site.local.runtime.version="3.10.9"
LABEL site.local.program.name="Python Modbus TCP Client"
LABEL site.local.program.version="1.0.9"

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

RUN apk add --no-cache \
      libstdc++=12.2.1_git20220924-r4 \
      py3-pandas=1.5.1-r0 \
    && pip3 install --no-cache-dir \
       'pymodbus>=2,<3' \
    && addgroup -g 1000 -S pythonuser \
    && adduser -u 1000 -S pythonuser -G pythonuser \
    && mkdir -p /app
COPY --chown=root:root app/* /app/

USER pythonuser

# Start Server
ENTRYPOINT ["python", "-u", "/app/modbus_client.py"]
