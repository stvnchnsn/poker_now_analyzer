import os
import pandas as pd
import matplotlib.pyplot as plt
from word_soup import Word_Soup as ws

class Game_Compiler:
    '''Runs the entire game through word soup and outputs
    usable data'''
    def __init__(self, filename):
        self.r_data = pd.read_csv('./'+filename)
        self.r_data = self.r_data.iloc[::-1] # reverses order so first index is opening entry
        self.r_data = self.r_data.reset_index(drop = True)
    def raw_log(self):
        return self.r_data.iloc[:,0]
    def read_log(self):
        ''' Converts the entry of the log into something usable
        outputs a DataFrame'''
        self.list_of_cleaned_entries = []
        for i,_ in enumerate(self.r_data.iloc[:,0]):
            self.clean_soup = ws(self.r_data.iloc[i])
            self.list_of_cleaned_entries .append(self.clean_soup.entry_analyzer())
        self.cols=['action','player','amount','stack','player running stack','Hand #','blind']
        self.c_data = pd.DataFrame(self.list_of_cleaned_entries, columns=self.cols)
        self.c_data['entries'] = self.r_data.iloc[:,0]
        self.c_data['at'] = self.r_data.iloc[:,1]
        return self.c_data
    def duration_of_game(self):
        i_time = pd.to_datetime(self.c_data['at'].iloc[0])
        f_time = pd.to_datetime(self.c_data['at'].iloc[-1])
        return  (f_time - i_time)
    def list_of_player(self):
        self.read_log()
        self.players = (self.c_data['player'][(self.c_data['player'] != 'admin') &
        self.c_data['player']!= 0]).unique()
        return self.players
    def analyze_game(self):
        self.read_log()
        self.list_of_player()
        pass



    

nov2020 = 'poker_now_log_QG7YmhhsY1elwfGITlbPZTOgY.csv'
dec2020 = 'poker_now_log_4gcAQTnotvBq87RCX1oHXKvhM.csv'
def main(filename = 'original_data/'+nov2020):
    data = Game_Compiler(filename)
    log = data.read_log()
    duration = data.duration_of_game()
    print('duration = ', duration)
    players = data.list_of_player()
    print('players = ', players)
    log.to_clipboard()
    
if __name__ == '__main__':
    main()
