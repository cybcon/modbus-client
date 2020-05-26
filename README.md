# Quick reference

Maintained by: [Michael Oberdorf IT-Consulting](https://www.oberdorf-itc.de/)

Source code: [Bitbucket](https://bitbucket.org/Cybcon/modbus-client/src/master/)

# Supported tags and respective `Dockerfile` links

* [`latest`, `1.0.4`](https://bitbucket.org/Cybcon/modbus-client/src/1.0.4/dockerfile)
* [`1.0.3`](https://bitbucket.org/Cybcon/modbus-client/src/1.0.3/dockerfile)
* [`1.0.2`](https://bitbucket.org/Cybcon/modbus-client/src/1.0.2/dockerfile)

# What is Modbus TCP Client?

The Modbus TCP Client is a comand line tool, written in python to read and interpret Modbus registers.

# QuickStart with Modbus TCP Client and Docker

Step - 1 : Pull the Modbus TCP Client

```bash
docker pull oitc/modbus-client
```

Step - 2 : Run the Modbus TCP Client to scan your Modbus Server Registers

```bash
docker run --rm oitc/modbus-client:latest [options]

usage: modbus_client.py [-h] [-s SLAVE] [-p PORT] [-i SLAVEID]
                        [-t REGISTERTYPE] [-r REGISTER] [-l LENGTH] [-c] [-d]

Modbus TCP Client v1.0.4

optional arguments:
  -h, --help            show this help message and exit

  -s SLAVE, --slave SLAVE
                        Hostname or IP address of the Modbus TCP slave
                        (default: 127.0.0.1)
  -p PORT, --port PORT  TCP port (default: 502)
  -i SLAVEID, --slaveid SLAVEID
                        The slave ID, between 1 and 247 (default: 1)
  -t REGISTERTYPE, --registerType REGISTERTYPE
                        Register type 1 to 4 to read (1=Discrete Output Coils,
                        2=Discrete Input Contacts, 3=Analog Output Holding
                        Register, 4=Analog Input Register) (default: 3)
  -r REGISTER, --register REGISTER
                        The register address between 0 and 9999 (default: 0)
  -l LENGTH, --length LENGTH
                        How many registers should be read, between 1 and 125
                        (default: 1)
  -c, --csv             Output as CSV
  -d, --debug           Enable debug output
```

# License
 
Copyright (c) 2020 Michael Oberdorf IT-Consulting

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.