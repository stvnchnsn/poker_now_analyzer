
class Player:
    def __init__(self,name,purse):
        self.name = name
        self.purse = purse
        self.small_blind_status = 0
        self.betting_status = 0
        self.outstanding_bet = 0
        self.outstanding_bet_amount = 0
        self.count_uncalled_bets = 0
        
    def name_of_player(self):
        return self.name
    def increase_purse(self,amount):
        self.purse = self.purse + int(amount)
    def decrease_purse(self,amount):
        try:
            self.purse = self.purse - int(amount)
        except:
            #pass
            print(amount)
    def current_purse(self):
        return self.purse


def test_purse():
    steve= Player('Steve',0)
    steve.increase_purse(80)
    steve.increase_purse(30)
    steve.decrease_purse(70)
    print(steve.purse)
def test_creating_list_of_player_obj():
    list_of_players = ['Ton', 'Alex' ,'Steve', 'Sean' ,'ChadSlap' ,'charles']
    player_obj = []
    for p in list_of_players:
        player_obj.append(Player(p,0))
    player = 'Ton'
    for p in player_obj:
        if p.name_of_player() == player:
            p.increase_purse(50)
    [print(p.name_of_player(),p.purse) for p in player_obj]

    


if __name__ =='__main__':
    #test_purse()
    test_creating_list_of_player_obj()