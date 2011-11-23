class Person:

	def __init__(self):
		self.hands = [[]]
		self.val = [0]
		self.aces = [0]
		self.tmp = [0]

	def add(self, card, hand=0):
		self.hands[hand].append(card)
		if not type(card[1]) is str:
			self.val[hand] += card[1]
		elif card[1] == 'A':
			self.val[hand] += 11
			self.aces[hand] += 1
			self.tmp[hand] += 1
		else: self.val[hand] += 10

		if self.val[hand] > 21 and self.tmp[hand] > 0:
			self.val[hand] -= 10
			self.tmp[hand] -= 1

	def play(self):
		pass

	def clear_hand(self):
		self.hands = [[]]
		self.val = [0]
		self.aces =[0]
		self.tmp = [0]

	def __repr__(self):
		return str(self.val) + ' ' + str(self.hands)
