# -*- coding: utf-8 -*-
import FloatToHex
import sys
import numpy as np
import pandas as pd

print('Testing: FloatToHex')
float = 29.625
print(float)
decimal = FloatToHex.floattohex(float)
print(hex(decimal))
float_new = FloatToHex.hextofloat(decimal)
print(float_new)

print('Testing: pandas')
DATA = dict()
DATA['COL1'] = 123
DATA['COL2'] = 4.56
DATA['COL3'] = 'test'

df = pd.DataFrame.from_dict([DATA], orient='columns')
with pd.option_context('display.max_rows', None, 'display.max_columns', None): print(df)

print('Testing: numpy')
value = 292
print(np.int16(value))
print(np.uint16(value))

sys.exit()
