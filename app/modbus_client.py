# -*- coding: utf-8 -*-
""" ***************************************************************************
Modbus client script for debugging
Author: Michael Oberdorf IT-Consulting
Datum: 2020-05-20

example taken from: https://pymodbus.readthedocs.io/en/latest/source/example/synchronous_client.html
*************************************************************************** """
import sys
import os
import socket
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import logging
import argparse
from codecs import decode
import struct
import pandas as pd
import FloatToHex

VERSION='1.0.1'
DEBUG=False

"""
###############################################################################
# F U N C T I O N S
###############################################################################
"""
def float_to_hex(value):
    """ convert a float into a 4 byte hex string """
    binary_string=bin(struct.unpack('!I', struct.pack('!f', value))[0])[2:].zfill(32)
    return(format(int(binary_string, 2), 'x').upper())

def hex_to_float(value):
    """ convert a 4 byte hex string into a float """
    my_int = int('0x' + value, 16)
    #binary = bin(my_int)[2:]
    #return(struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0])
    return FloatToHex.hextofloat(my_int)

def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def float_to_bin(num):
    return bin(struct.unpack('!I', struct.pack('!f', num))[0])[2:].zfill(32)


def bin_to_float64(b):
    """ Convert binary string to a float. """
    bf = int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
    return struct.unpack('>d', bf)[0]


def int_to_bytes(n, length):  # Helper function
    """ Int/long to byte string.

        Python 3.2+ has a built-in int.to_bytes() method that could be used
        instead, but the following works in earlier versions including 2.x.
    """
    return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]

def float64_to_bin(value):  # For testing.
    """ Convert float to 64-bit binary string. """
    [d] = struct.unpack(">Q", struct.pack(">d", value))
    return '{:064b}'.format(d)


def parse_modbus_result(registers, start_register):
    """
    parse_modbus_result - function to parse the modbus result and encode several format types
    @param registers: list(), the registers result list from modbus client read command
    @param start_register: integer, the start register number
    @return: pandas.DataFrame(), table of calculated values per register 
    """
    bitLength32 = 0
    bitLength64 = 0
    previousRegister32 = ''
    previousRegister64 = ''
    DATA = list()
    for register in registers:
        DATASET = dict()
        DATASET['register'] = start_register
        htext = format(register, 'x')
        decParts = [int(htext[i:i+2],16) for i in range(0,len(htext),2)]
        DATASET['INT16'] = register
        DATASET['UINT16'] = register & 0xffff
        hexParts = ['0x' + htext[i:i+2] for i in range(0,len(htext),2)]
        DATASET['HEX16'] = '0x' + htext.upper()
        #DATASET['HEX16'] = ' '.join(hexParts)
        chrParts = [chr(val) for val in decParts]
        DATASET['ASCII'] = ' '.join(chrParts)
        bitString = bin(int(htext, 16))[2:].zfill(16)
        DATASET['BIT'] = bitString
        
        if bitLength32 >= 1:
            #DATASET['HEX32'] = '0x' + previousRegister32 + htext
            DATASET['INT32'] =  int(previousRegister32 + htext, 16)
            DATASET['UINT32'] =  DATASET['INT32'] & 0xffffffff
            bits_32 = bin(DATASET['INT32'])[2:].zfill(32)
            DATASET['FLOAT32'] = bin_to_float(bits_32)
            
            if DATASET['INT32'] == 0.000000e+00: DATASET['INT32'] = 0.0
            if DATASET['FLOAT32'] == 0.000000e+00: DATASET['FLOAT32'] = 0.0
            previousRegister32 = htext
        bitLength32+=1
        
        """
        if bitLength64 == 3:
            #DATASET['HEX64'] = '0x' + previousRegister64 + htext
            DATASET['INT64'] = int(previousRegister64 + htext, 16)
            DATASET['UINT64'] = DATASET['INT64'] & 0xffffffffffffffff
            bits_64 = bin(DATASET['INT64'])[2:].zfill(64)
            DATASET['FLOAT64'] = bin_to_float64(bin(DATASET['INT64'])[2:].zfill(32))
            previousRegister64 = ''
            bitLength64 = 0
        else:
            previousRegister64 += htext
            bitLength64+=1
        """
        
        start_register+=1
        DATA.append(DATASET)
    
    
    df = pd.DataFrame.from_dict(DATA, orient='columns')
    df.set_index('register', drop=True, inplace=True)
    
    if bitLength32 > 1:
        df = df[['HEX16', 'INT16', 'BIT', 'FLOAT32', 'INT32']]
    else:
        df = df[['HEX16', 'INT16', 'BIT']]
    return(df)


"""
###############################################################################
# M A I N
###############################################################################
"""

# Initialize logger
#FORMAT = ('%(asctime)-15s %(threadName)-15s  %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
FORMAT = ('%(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()

if DEBUG: log.setLevel(logging.DEBUG)
else: log.setLevel(logging.INFO)

# Parsing command line arguments
parser = argparse.ArgumentParser(description='Modbus TCP Client')
group = parser.add_argument_group()
group.add_argument('-s', '--slave', help='Hostname or IP address of the Modbus TCP slave (default: 127.0.0.1)', default='127.0.0.1')
group.add_argument('-p', '--port', help='TCP port (default: 502)', default=502)
group.add_argument('-i', '--slaveid', help='The slave ID, between 1 and 247 (default: 1)', default=1)
group.add_argument('-t', '--registerType', help='Register type 1 to 4 to read (1=Discrete Output Coils, 2=Discrete Input Contacts, 3=Analog Output Holding Register, 4=Analog Input Register) (default: 3)', default=3)
group.add_argument('-r', '--register', help='The register address between 0 and 9999 (default: 0)', default=0)
group.add_argument('-l', '--length', help='How many registers should be read between 1 and 125 (default: 1)', default=1)
args = parser.parse_args()
# validate input
if not isinstance(args.slaveid, int): args.slaveid = int(args.slaveid)
if args.slaveid < 1 or args.slaveid > 247:
    log.error('SlaveID needs to be in a range between 1 and 247!')
    sys.exit(1)
if not isinstance(args.registerType, int): args.registerType = int(args.registerType)
if args.registerType < 1 or args.registerType > 4:
    log.error('Register typer needs to be 1, 2, 3 or 4!')
    sys.exit(1)
if not isinstance(args.register, int): args.register = int(args.register)
if args.register < 0 or args.register > 9999:
    log.error('Register needs to be in a range between 0 and 9999!')
    sys.exit(1)
if not isinstance(args.length, int): args.length = int(args.length)
if args.length < 1 or args.length > 125:
    log.error('Register read length needs to be in a range between 1 and 125!')
    sys.exit(1)
if args.length < 1 or args.register + args.length - 1 > 9999:
    log.error('Register length does not exceed the maximum register addresses in a range between 1 and 9999!')
    sys.exit(1)

# define some values, based on the input
if args.registerType == 1:
    register_type = 'Discrete Output Coils'
    register_number = args.register 
elif args.registerType == 2:
    register_type = 'Discrete Input Contacts'
    register_number = 10000 + args.register
elif args.registerType == 3:
    register_type = 'Analog Output Holding Register'
    register_number = 40000 + args.register
elif args.registerType == 4:
    register_type = 'Analog Input Register'
    register_number = 30000 + args.register


# start the master and connect to slave
if DEBUG:
    print('Starting Modbus TCP master client, v' + str(VERSION))
    print('Trying to connect to slave: ' + str(args.slave) + ':' + str(args.port))
    print('Query with slave id: ' + str(args.slaveid) + ', register: "' + register_type + '", start register: ' + str(args.register) + ', read register Length: ' + str(args.length))
    print()

# create the client
client = ModbusClient(args.slave, port=args.port)
# connect to server
result = client.connect()
if not result:
    log.error('Error while connecting to Modbus TCP slave on:' + str(args.slave) + ':' + str(args.port))
    sys.exit(2)


# read the registers, dependent on the requested type
if args.registerType == 1:   rr = client.read_coils(args.register, args.length, unit=args.slaveid)
elif args.registerType == 2: rr = client.read_discrete_inputs(args.register, args.length, unit=args.slaveid)
elif args.registerType == 3: rr = client.read_holding_registers(args.register, args.length, unit=args.slaveid)
elif args.registerType == 4: rr = client.read_input_registers(args.register, args.length, unit=args.slaveid)
if rr.isError():
    log.error('Error while querying Modbus TCP slave!')
    client.close()
    sys.exit(3)
# close connection
client.close()

# parse the results
df = parse_modbus_result(rr.registers, register_number)

# output results
with pd.option_context('display.max_rows', None, 'display.max_columns', None): print(df)


sys.exit(0)