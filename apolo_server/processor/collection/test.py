from pandas.io import data, wb # becomes
from pandas_datareader import data, wb
import pandas_datareader as pdr
pdr.get_data_yahoo('AAPL')