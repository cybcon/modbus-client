# Floating Point to Hex Converter

The software was taken from site: https://gregstoll.com/~gregstoll/floattohex/

## Contributor:

Gregory Stoll <greg@gregstoll.com>
https://gregstoll.com/

# Synopsis

```python
import FloatToHex
float = 29.625
```

# store float in 4 byte (32 bit) single precision (IEEE 754 binary32)
```python
my_32bit_int = FloatToHex.floattohex(float)
```

# recover float from IEEE 754 binary32
```python
print(FloatToHex.hextofloat(my_32bit_int))
```

# store float in 8 byte (64 bit) double precision (IEEE 754 binary64)
```python
my_64bit_int = FloatToHex.doubletohex(float)
```

# recover float from IEEE 754 binary64
```python
print(FloatToHex.hextodouble(my_64bit_int))
```
