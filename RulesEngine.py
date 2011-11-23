from Dealer import Dealer
from Player import Player

class RulesEngine:
	
	def __init__(self, dealer, players):
		self.players = players
		self.dealer = dealer

	def update(self, standing):
		for player in standing:
			for i in xrange(0,len(player.hands)):
				# Blackjack
				if (player.val[i] == 21 and len(player.hands[i]) == 2) and (self.dealer.val[0] != 21 and len(self.dealer.hands[0]) != 2):
					player.cash += int((3/2)*player.bet)
				
				elif self.dealer.val[0] > 21 or player.val[i] > self.dealer.val[0]:
					player.cash += 2*player.bet

				elif self.dealer.val[0] == player.val[i] and player.val[i] <= 21:
					player.cash += player.bet

			player.bet = 0

		
