FROM python:3.8-alpine AS base

# Compiling python modules
FROM base as builder

RUN apk add --no-cache g++ python3-dev && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h
ADD FloatToHex /FloatToHex
RUN cd /FloatToHex; python3 setup.py install
RUN pip3 install pandas


# Building the docker image with already compiled modules
FROM base
LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.vendor="Michael Oberdorf IT-Consulting"
LABEL site.local.os.main="Linux"
LABEL site.local.os.dist="Alpine"
LABEL site.local.runtime.name="Python"
LABEL site.local.runtime.version="3.8"
LABEL site.local.program.name="Python Modbus TCP Client"
LABEL site.local.program.version="1.0.4"

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

RUN apk add --no-cache libstdc++ && \
    addgroup -g 1000 -S pythonuser && \
    adduser -u 1000 -S pythonuser -G pythonuser && \
    mkdir -p /app && \
    pip3 install pymodbus
ADD --chown=root:root app/* /app/
RUN python /app/test.py && rm -f /app/test.py

USER pythonuser

# Start Server
ENTRYPOINT ["python"]
CMD ["-u", "/app/modbus_client.py"]
