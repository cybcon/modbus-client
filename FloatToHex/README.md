# FloatToHex Python module

The software was taken/stolen from site:
  https://gregstoll.com/~gregstoll/floattohex/

# Synopsis

import FloatToHex
float = 29.625

# store float in 4 byte (32 bit) single precision (IEEE 754 binary32)
my_32bit_int = FloatToHex.floattohex(float)

# recover float from IEEE 754 binary32
print(FloatToHex.hextofloat(my_32bit_int))

# store float in 8 byte (64 bit) double precision (IEEE 754 binary64)
my_64bit_int = FloatToHex.doubletohex(float)

# recover float from IEEE 754 binary64
print(FloatToHex.hextodouble(my_64bit_int))

