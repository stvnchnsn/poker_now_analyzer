import os
import pandas as pd
import matplotlib.pyplot as plt

filename = 'original_data/poker_now_log_4gcAQTnotvBq87RCX1oHXKvhM.csv'
data = pd.read_csv('./'+filename)
data = data.iloc[::-1]
data = data.reset_index(drop = True)
data