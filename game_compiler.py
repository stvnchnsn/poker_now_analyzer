import os
import pandas as pd
import matplotlib.pyplot as plt
from word_soup import Word_Soup as ws
from players import Player # not currently using 

class Game_Compiler:
    '''Runs the entire game through word soup and outputs
    usable data'''
    def __init__(self, filename):
        self.r_data = pd.read_csv('./'+filename)
        self.r_data = self.r_data.iloc[::-1] # reverses order so first index is opening entry
        self.r_data = self.r_data.reset_index(drop = True)
        self.read_log()
        self.list_of_player()
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
        
        self.player_list = (self.c_data['player'][(self.c_data['player'] != 'admin') &
        self.c_data['player']!= 0]).unique()
        for player in self.player_list: #create player columns
            self.c_data[player] = 0
        return self.player_list

    def analyze_gameII(self):
        self.players_objects = []
        for player in self.player_list:
            self.p = Player(player,0)
            self.players_objects.append(self.p.name_of_player())
            self.c_data[player] = self.player_actionsII(player)
        return self.c_data

    def player_actionsII(self,player):
        increase_actions = ['buy-in approved','collected']
        decrease_actions = ['big_blind','bets','rasies','calls']
        small_blind_action = ['small_blind']
        all_in_action = ['bets all in']
        rasies_action = ['rasies']
        self.action_list = []

        for i, a in enumerate(self.c_data['action']):
            amount = self.c_data.loc[i,'amount']      # amount in current action
            if self.c_data.loc[i,'player']==player:
                if a in increase_actions:
                    self.p.increase_purse(amount)
                elif a in decrease_actions:
                    # small blind check
                    if self.p.small_blind_status == 0: 
                        self.p.decrease_purse(amount)  
                    else:  
                        if a == 'folds':
                            self.p.decrease_purse(self.p.small_blind_amount)
                        else:
                            self.p.decrease_purse(amount)
                        self.p.small_blind_status = 0   #turn off small blind 
                # small blind action
                elif a in small_blind_action:
                    self.p.small_blind_amount = amount
                    self.p.small_blind_status = 1
                elif a in all_in_action:
                    self.p.purse = 0
                elif a in rasies_action:
                    pass
            self.action_list.append(self.p.current_purse())
        return self.action_list

    def analyze_by_action(self):
        ''' differnt approach to iterating through the log
            obsoletes analyze_gameII '''
        self.player_obj_list = []
        [self.player_obj_list.append(Player(p,0)) for p in self.player_list]
        increase_actions = ['buy-in approved','collected']
        decrease_actions = ['big_blind','uncalled bet','fold']
        small_blind_action = ['small_blind']
        all_in_action = ['bets all in']
        betting_action = ['raises','bets']
        call = ['calls']
        end_of_betting = ['flop','turn','river','shows','end hand']

        self.betting_status = 0
        

        for i, a in enumerate(self.c_data['action']):
            amount = self.c_data.loc[i,'amount']
            # check if player action
            if self.c_data.loc[i,'player'] in self.player_list:
                for p in self.player_obj_list:
                    if p.name_of_player() == self.c_data.loc[i,'player']:
                        # increase_actions
                        if a in increase_actions:
                            p.increase_purse(amount)
                            p.outstanding_bet = 0
                            p.outstanding_bet_amount = 0
                        # decrease_actions    
                        elif a in decrease_actions:
                            if a == 'fold':
                                if p.small_blind_status == 1:
                                    p.decrease_purse(p.small_blind_amount)
                                    p.betting_status = 0
                                    p.small_blind_status = 0
                                else:
                                    p.decrease_purse(p.outstanding_bet_amount)
                                p.betting_status = 0

                            elif a =='uncalled bet':
                                p.count_uncalled_bets +=1
                            #elif p.small_blind_status == 0: 
                             #   p.decrease_purse(amount)
                            elif a=='big_blind':
                                p.decrease_purse(amount)
                        # small blind action
                        elif a in small_blind_action:
                            p.small_blind_amount = amount
                            p.small_blind_status = 1
                        # all in action
                        elif a in all_in_action:
                            p.purse = 0
                        # raise action
                        elif a in betting_action:
                            p.betting_status = 1
                            p.outstanding_bet = 1
                            p.outstanding_bet_amount =int(amount)
                            self.betting_status = 1
                        elif a in call:
                            if self.betting_status ==1:
                                p.betting_status = 1
                                p.outstanding_bet_amount = int(amount)
                                #self.betting_status = 0
                                #for p in self.player_obj_list:
                                 #   if p.betting_status ==1:
                                  #      p.decrease_purse(amount)
                                   #     p.betting_status = 0
                                        
                            elif self.betting_status == 0:
                                p.decrease_purse(amount)
                            

            if a in end_of_betting: 
                # collect all oustanding bets and set all players betting status to zero
                for p in self.player_obj_list:
                    if p.betting_status ==1:
                        p.decrease_purse(p.outstanding_bet_amount)
                    p.small_blind_status = 0
                    p.outstanding_bet_amount = 0

                self.betting_status = 0
                for p in self.player_obj_list:
                    p.betting_status = 0 

                

                            
            # check player stacks
            elif a == 'player_stacks':
                stacks = self.c_data.loc[i,'player running stack']
                for p in self.player_obj_list:
                    try:
                        if p.current_purse() != stacks[p.name_of_player()]:
                            self.c_data.loc[i,'stack_mismatch']=1
                        else:
                            self.c_data.loc[i,'stack_mismatch']=0
                    except:
                        pass

                
                        
            for player in self.player_obj_list:
                self.c_data.loc[i,player.name_of_player()]=player.purse
                self.c_data.loc[i,'betting status'] = self.betting_status
        return self.c_data
                    






        
        




    

nov2020 = 'poker_now_log_QG7YmhhsY1elwfGITlbPZTOgY.csv'
dec2020 = 'poker_now_log_4gcAQTnotvBq87RCX1oHXKvhM.csv'
def main(filename = 'original_data/'+dec2020):
    data = Game_Compiler(filename)
    log = data.read_log()
    log.to_clipboard()
    duration = data.duration_of_game()
    print('duration = ', duration)
    players = data.list_of_player()
    print('players = ', players)
    updatedlist = data.analyze_game()
    updatedlist.to_clipboard()
    
def test_main(filename = 'original_data/'+dec2020):
    data = Game_Compiler(filename)
    analyzed_game = data.analyze_gameII()
    analyzed_game.to_clipboard()
    
def test2_main(filename = 'original_data/'+dec2020):
    data = Game_Compiler(filename)
    analyzed_game = data.analyze_by_action()
    analyzed_game.to_clipboard()
if __name__ == '__main__':
    #main()
    #test_main()
    test2_main()
