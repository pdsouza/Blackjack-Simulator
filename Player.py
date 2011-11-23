from Person import Person

class Player(Person):

	def __init__(self, name, cash=3000): 
		Person.__init__(self)
		self.name = name
		self.cash = cash
		self.bet = 0

	def play(self):
		if self.val[0] > 21: return -1
		if self.val[0] < 17: return 1
		return 0

	def make_bet(self):
		self.bet = int(0.02*self.cash)
		self.cash -= self.bet

	def __repr__(self):
		return self.name + ': ' + '$' + str(self.cash) + ' ' + str(self.val) + ' ' + str(self.hands) + ' ' + str(self.aces)



