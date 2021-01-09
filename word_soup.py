import os
import pandas as pd
import matplotlib.pyplot as plt
from action_identifier import Action_identifier as action_id


class Word_Soup:
    ''' Interprets poker now self.entry log and out puts usable data'''
    def __init__(self, entry):
        self.entry = entry

    def entry_analyzer(self):
        '''analyzes an self.entry and returns:
        self.action, self.actor, stack, self.player_s, handnumber'''
        self.action = 0
        self.actor = 0
        self.stack = 0
        self.player_s = 0
        self.handnumber = 0
        self.small_b = 0
        self.blind = 0
        self.amount= 0
        self.ans = False
        if action_id.requested_seat(self.entry):
            self.ans,self.actor,self.action = action_id.requested_seat(self.entry)    
        if action_id.buyin_approve(self.entry):
            self.ans,self.actor,self.action,self.stack = action_id.buyin_approve(self.entry)
        if action_id.admin(self.entry):
            self.ans,self.actor,self.action,self.handnumber = action_id.admin(self.entry)
        if action_id.joined_game(self.entry):
            self.ans,self.action, self.actor,self.stack = action_id.joined_game(self.entry)
        if action_id.player_stacks(self.entry):
            self.ans,self.action, self.player_s = action_id.player_stacks(self.entry)
        if action_id.your_hand(self.entry):
            self.ans,self.action = action_id.your_hand(self.entry)
        if action_id.blinds(self.entry):
            self.ans,self.actor,self.action,self.blind = action_id.blinds(self.entry)
        if action_id.player_action(self.entry):
            self.ans,self.action,self.actor,self.amount = action_id.player_action(self.entry)
        if action_id.card_reveal(self.entry):
            self.ans,self.action = action_id.card_reveal(self.entry)
        if action_id.pay_out(self.entry):
            self.ans, self.action, self.actor,self.amount = action_id.pay_out(self.entry)

        if self.ans == False:
            return ["action not defined",0,0,0,0,0,0]
        return self.action, self.actor, self.amount,self.stack, self.player_s,self.handnumber,self.blind

def main(filename = 'original_data/poker_now_log_4gcAQTnotvBq87RCX1oHXKvhM.csv'):
    import game_compiler
    i = 0
    data = game_compiler.Game_Compiler(filename)
    data = data.raw_log()
    entry = Word_Soup((data.iloc[i]))
    entry = Word_Soup((data.iloc[i+1]))
    print(data.iloc[i,0])
    print(entry.entry_analyzer())
if __name__ == '__main__':
    main()

