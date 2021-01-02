import os
import pandas as pd
import matplotlib.pyplot as plt

class Game_Compiler:
    '''Runs the entire game through word soup and outputs
    usable data'''
    def __init__(self, filename):
        self.data = pd.read_csv('./'+filename)
        self.data = self.data.iloc[::-1] # reverses order so first index is opening entry
        self.data = self.data.reset_index(drop = True)
    def raw_log(self):
        return self.data