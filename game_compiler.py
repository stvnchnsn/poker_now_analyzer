import os
import pandas as pd
import matplotlib.pyplot as plt
from word_soup import Word_Soup as ws

class Game_Compiler:
    '''Runs the entire game through word soup and outputs
    usable data'''
    def __init__(self, filename):
        self.data = pd.read_csv('./'+filename)
        self.data = self.data.iloc[::-1] # reverses order so first index is opening entry
        self.data = self.data.reset_index(drop = True)
    def raw_log(self):
        return self.data.iloc[:,0]
    def read_log(self):

        self.list_of_cleaned_entries = []

        for i,_ in enumerate(self.data.iloc[:,0]):
            self.clean_soup = ws(self.data.iloc[i])
            

            self.list_of_cleaned_entries .append(self.clean_soup.entry_analyzer())
        self.cols=['action','player','amount','stack','player running stack','Hand #','blind']
        self.df_cleaned_entries = pd.DataFrame(self.list_of_cleaned_entries, columns=self.cols)
        self.df_cleaned_entries['entries'] = self.data.iloc[:,0]
        self.df_cleaned_entries['at'] = self.data.iloc[:,1]

        return self.df_cleaned_entries
    def read_log2(self):
        pass

def main(filename = 'original_data/poker_now_log_4gcAQTnotvBq87RCX1oHXKvhM.csv'):
    data = Game_Compiler(filename)
    data = data.read_log()
    print(data[data['action']=='action not defined'])
if __name__ == '__main__':
    main()
