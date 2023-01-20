# Quick reference

Maintained by: [Michael Oberdorf IT-Consulting](https://www.oberdorf-itc.de/)

Source code: [GitHub](https://github.com/cybcon/modbus-client)

# Supported tags and respective `Dockerfile` links

* [`latest`, `1.0.8`](https://github.com/cybcon/modbus-client/blob/v1.0.8/Dockerfile)
* [`1.0.6`](https://github.com/cybcon/modbus-client/blob/1.0.6/Dockerfile)
* [`1.0.5`](https://github.com/cybcon/modbus-client/blob/1.0.5/Dockerfile)
* [`1.0.4`](https://github.com/cybcon/modbus-client/blob/1.0.4/dockerfile)


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
                        [-t REGISTERTYPE] [-r REGISTER] [-l LENGTH] [-b] [-c]
                        [-d]

Modbus TCP Client v1.0.5

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
  -b, --bigEndian       Use big endian instead of little endian when
                        calculating the 32bit values
  -c, --csv             Output as CSV
  -d, --debug           Enable debug output
```

# Example

```bash
docker run --rm oitc/modbus-client:latest -s 192.168.58.70 -p 1503 -t 4 -r 0 -l 10
           HEX16  UINT16  INT16               BIT       HEX32    FLOAT32
register
30000     0x84D9   34009 -31527  1000010011011001  0x84D90000  -0.000000
30001     0x41ED   16877  16877  0100000111101101  0x41ED84D9  29.689867
30002     0x0000       0      0  0000000000000000  0x000041ED   0.000000
30003     0xC24C   49740 -15796  1100001001001100  0xC24C0000 -51.000000
30004     0x0000       0      0  0000000000000000  0x0000C24C   0.000000
30005     0xBF80   49024 -16512  1011111110000000  0xBF800000  -1.000000
30006     0x0068     104    104  0000000001101000  0x0068BF80   0.000000
30007     0x006C     108    108  0000000001101100  0x006C0068   0.000000
30008     0x0074     116    116  0000000001110100  0x0074006C   0.000000
30009     0x0032      50     50  0000000000110010  0x00320074   0.000000
```

# License

Copyright (c) 2020-2023 Michael Oberdorf IT-Consulting

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
