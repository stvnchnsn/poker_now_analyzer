

class Action_identifier:
    '''inentifies what the action was for the self.entry and 
    other relevant parameters.'''
    def __init__(self,entry):
        self.entry = self.entry
    def requested_seat(self):
        if 'requested a seat' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            return True, self.actor,'requested a seat'
        else:
            return False
    def buyin_approve(self):
        if 'The admin approved the player' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.stack = int(self.entry.strip('.').split()[-1])
            return True, self.actor,'buy-in approved',self.stack
        else:
            return False
    def admin(self):
        if "The game's small blind was changed " in self.entry:
            return True,'admin', 'small blind update'
        if "The game's big blind was changed " in self.entry:
            return True, 'admin','big blind update'
        if "-- starting hand " in self.entry:
            self.handnumber = self.entry.split('#')[1].split()[0]
            return True,'start hand',self.handnumber
        if "-- ending hand" in self.entry:
            self.handnumber = self.entry.split('#')[1].split()[0]
            return True, 'end hand', self.handnumber
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
                self.stack = int(self.entry.strip('.').split()[-1].strip('()'))
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
            if 'small' in self.entry:
                return True, 'small_blind',int(self.entry.split()[-1])
            if 'big' in self.self.entry:
                return True, 'big_blind',int(self.entry.split()[-1])
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
            self.amount = self.entry.split()[-1]
            return True, 'calls', self.actor, self.amount
        elif 'checks' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            return True, 'checks',self.actor,self.amount
        if 'bets' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.amount = self.entry.split()[-1]
            return True, 'bets', self.actor, self.amount
        if 'raises' in self.entry:
            self.actor = self.entry.split('"')[1].split()[0]
            self.amount = self.entry.split()[-1]
            return True, 'raises', self.actor, self.amount
        else:
            return False
    def card_reveal(self):
        if 'Flop' in self.entry:
            return True, 'flop'
        if 'Turn:' in self.entry:
            return True, 'turn'
        if 'River:' in self.entry:
            return True, 'river'
        else:
            return False