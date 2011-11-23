from Person import Person

class Dealer(Person):

	def __init__(self): 
		Person.__init__(self)

	def play(self):
		if self.val[0] > 21: return -1
		if self.val[0] < 17: return 1
		return 0


