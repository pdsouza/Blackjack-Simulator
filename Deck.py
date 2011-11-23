import random

class Deck:
	
	def __init__(self, num):
		self.num_decks = num
		self.deck = self.generate(num)
		self.shuffle()	
		
	def generate(self, num):
		deck = [(s,i) for s in ['D','S','C','H'] for i in [j for j in xrange(2,11)] + ['J','Q','K','A'] for k in xrange(0,num)]
		return deck
	
	def shuffle(self):
		random.shuffle(self.deck)	
		
	def draw(self):
		return self.deck.pop()
	
	def __repr__(self):
		return str(self.deck)
	