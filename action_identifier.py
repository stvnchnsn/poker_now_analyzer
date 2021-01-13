

class Action_identifier:
    '''inentifies what the action was for the self.entry and 
    other relevant parameters.'''
    def __init__(self,entry):
        self.entry = entry
        print(type(self),'ai')
    def requested_seat(self):
        if 'requested a seat' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            return True, self.actor,'requested a seat'
        else:
            return False
    def buyin_approve(self):
        if 'The admin approved the player' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.amount = int(self.entry.strip('.').split()[-1])
            return True, self.actor,'buy-in approved',self.amount
        else:
            return False
    def admin(self):
        if "The game's small blind was changed " in self.entry:
            return True,'admin', 'small blind update',0
        if "The game's big blind was changed " in self.entry:
            return True, 'admin','big blind update',0
        if "-- starting hand " in self.entry:
            self.handnumber = self.entry.split('#')[1].split()[0]
            return True, 'admin','start hand',self.handnumber
        if "-- ending hand" in self.entry:
            self.handnumber = self.entry.split('#')[1].split()[0]
            return True,'admin', 'end hand', self.handnumber
        if "Dead Small Blind" in self.entry:
            return True,'admin', 'dead small blind',0
        else:
            return False
    def joined_game(self):
        if 'joined the game' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.stack = int(self.entry.strip('.').split()[-1])
            return True, 'joined game',self.actor, self.stack
        else:
            return False
    def player_stacks(self):
        if 'Player stacks: ' in self.entry:
            self.player_s = {}
            for player in self.entry.split('|'):
                self.actor = player.split('"')[1].split()[0]
                self.stack = int(player.strip('.').split()[-1].strip('()'))
                self.player_s[self.actor] = self.stack
            return True, 'player_stacks',self.player_s
        else:
            return False
    def your_hand(self):
        if 'Your hand' in self.entry:
            return True, "your_hand"
        else:
            return False
    def blinds(self):
        if 'posts a' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            if 'small' in self.entry:
                return True, self.actor ,'small_blind',int(self.entry.split()[-1])
            if 'big' in self.entry:
                return True,self.actor , 'big_blind',int(self.entry.split()[-1])
        else:
            return False
    def player_action(self):
        '''returns: T/F,action,self.actor',self.amount'''
        self.amount= 0
        if 'folds' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            return True, "fold", self.actor,self.amount
        elif 'calls' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            if 'go all in' in self.entry:
                self.amount = self.entry.split()[-5]
                return True, 'bets all in', self.actor,self.amount
            else:
                self.amount = self.entry.split()[-1]
                return True, 'calls', self.actor, self.amount
        elif 'checks' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            return True, 'checks',self.actor,self.amount
        if 'bets' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            if 'go all in' in self.entry:
                self.amount = self.entry.split()[-5]
                return True, 'bets all in', self.actor, self.amount
            else:
                self.amount = self.entry.split()[-1]
                return True, 'bets', self.actor, self.amount
        if 'raises' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            if 'go all in' in self.entry:
                self.amount = self.entry.split()[-5]
                return True, 'bets all in', self.actor, self.amount
            else:
                self.amount = self.entry.split()[-1]
                return True, 'raises', self.actor, self.amount
        if 'shows' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            return True, 'shows', self.actor, self.amount  
        if 'stand up' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0] 
            return True, 'stand up', self.actor, self.amount
        if 'sit down' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0] 
            return True, 'sit down', self. actor, self.amount
        if 'sit back' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.amount = self.entry.split()[-1]
            return True, 'sit back', self.actor, self.amount
        if 'quits the game' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.amount = self.entry.split()[-1]
            return True, 'quits the game', self.actor, self.amount
        if 'WARNING: the admin queued' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.amount = self.entry.split()[-6]
            return True, 'admin approved stack upate',self.actor, self.amount
        if 'The admin updated the player' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.amount = self.entry.split()[-1]
            return True, 'stack update', self.actor, self.amount
                
        else:
            return False
    def card_reveal(self):
        if 'flop' in self.entry.lower():
            return True, 'flop'
        if 'turn:' in self.entry.lower():
            return True, 'turn'
        if 'river:' in self.entry.lower():
            return True, 'river'
        else:
            return False
    def pay_out(self):
        if 'Uncalled bet' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.amount = self.entry.split()[3]
            return True, 'uncalled bet',self.actor, self.amount
        if 'collected ' in self.entry:
            self.actor= self.entry.split('"')[1].split()[0]
            self.amount = self.entry.split('from')[0].split()[-1]
            return True ,'collected', self.actor, self.amount
        else:
            return False

            

def main(filename = 'original_data/poker_now_log_4gcAQTnotvBq87RCX1oHXKvhM.csv'):
    import game_compiler
    i = 40
    data = game_compiler.Game_Compiler(filename)
    data = data.raw_log()
    print(data.iloc[i,0])
    entry = Action_identifier(entry = (data.iloc[i,0]))
    
    print(entry.pay_out()) 


if __name__ == '__main__':
    main()