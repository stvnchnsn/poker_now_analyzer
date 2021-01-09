

class Player:
    def __init__(self,name):
        self.name = name
        self.purse = 0
    def name_of_player(self):
        return self.name
    def increase_purse(self,amount):
        self.purse = self.purse + amount
    def decrease_purse(self,amount):
        self.purse = self.purse - amount
    def purse(self):
        return self.purse


if __name__ =='__main__':
    steve= Player('Steve')
    steve.increase_purse(80)
    steve.increase_purse(30)
    steve.decrease_purse(70)
    print(steve.purse)