from Deck import Deck
from Dealer import Dealer
from Player import Player
from Bot import Bot
from RulesEngine import RulesEngine

class Game:
	
	def __init__(self, num_players=1, num_decks=6):
		self.num_decks = num_decks
		self.dealer = Dealer()
		self.bot = Bot('Bot')
		self.players = []
		self.busted = []
		self.stand = []
		self.move = 0
		self.dealer_done = False
		self.bot_moves = []
		for i in xrange(0,num_players):
			self.players.append(Player('Player'+str(i+1)))

		self.players.append(self.bot)
		self.deck = Deck(num_decks)
		self.bot_deck = self.deck.deck * 1
		for player in self.players:
			player.make_bet()
			if player.name == 'Bot':
				player.add(self.bot_deck.pop())
				player.add(self.bot_deck.pop())
				self.bot_deck.pop()
				self.bot_deck.pop()
			else:
				player.add(self.deck.draw())
				player.add(self.deck.draw())
				self.dealer.add(self.deck.draw())
				self.dealer.add(self.deck.draw())

		self.rules = RulesEngine(self.dealer, self.players)

	def ongoing(self):
		return not len(self.players) == 0 or not self.dealer_done

	def winner(self):
		self.stand.sort(key=lambda x: x.val)
		self.stand.reverse()
		winner = self.dealer if self.dealer.val <= 21 else Player("Default")
		for player in self.stand:
			if player.val > winner.val:
				winner = player
		return winner

	def payout(self):
		self.rules.update(self.stand)

	def reset(self):
		self.players = self.rules.players
		self.stand = []
		self.busted = []
		self.dealer_done = False
		self.bot.update(self.players+[self.dealer])
		if len(self.deck.deck) <= self.deck.num_decks*52*0.25: # re-shuffle if < 75% of deck left
			self.deck.deck = self.deck.generate(self.deck.num_decks)
			self.deck.shuffle()
			self.reset_count()

		self.dealer.clear_hand()
		for player in self.players:
			player.clear_hand()
		self.bot_deck = self.deck.deck * 1
		for player in self.players:
			player.make_bet()
			if player.name == 'Bot':
				player.add(self.bot_deck.pop())
				player.add(self.bot_deck.pop())
				self.bot_deck.pop()
				self.bot_deck.pop()
			else:
				player.add(self.deck.draw())
				player.add(self.deck.draw())
				self.dealer.add(self.deck.draw())
				self.dealer.add(self.deck.draw())
		
		self.bot_moves = []

	def move_player(self, player, hand):
		newplayers = []
		
		if self.players[0].name == "Bot":
			move = player.play(self.dealer,hand)
		else:
			move = self.move

		if move == 1:
			player.add(self.deck.draw(),hand)
			if hand == len(player.hands)-1:
				newplayers.append(player)

		elif move == -1:
			if hand == len(player.hands)-1:
				self.busted.append(player)

		elif move == 2:
			player.add(self.deck.draw(),hand)
			player.doubled_down = True
			player.cash -= player.bet
			player.bet *= 2
			if hand == len(player.hands)-1:
				newplayers.append(player)

		elif move == 3:
			player.aces.append(0)
			player.tmp.append(0)

			player.hands.append([])
			card2 = player.hands[0].pop()
			player.val[0] = 0
			player.add(player.hands[0].pop(),0)
			player.cash -= player.bet
			player.val.append(0)
			player.add(card2,1)
			player.add(self.deck.draw(),0)
			player.add(self.deck.draw(),1)
			newplayers.append(player)

	def run(self):
		newplayers = []

		move = self.dealer.play()
		if move == 1:
			self.dealer.add(self.deck.draw())
			self.bot_deck.pop()
		else:
			self.dealer_done = True

		for i in xrange(0,len(self.players)):
			for j in xrange(0,len(self.players[i].hands)):
				if self.players[i].name == "Bot":
					move = self.players[i].play(self.dealer,j)
					if move == 2 and len(self.bot.hands[j]) > 2:
						move = 1
					if not (move == 0 and (j,move) in self.bot_moves):
						self.bot_moves.append((j,move))
				else:
					move = self.move

				if move == 1:
					if self.players[i].name == 'Bot':
						self.players[i].add(self.bot_deck.pop(),j)
					else:
						self.players[i].add(self.deck.draw(),j)
					if j == len(self.players[i].hands)-1:
						newplayers.append(self.players[i])

				elif move == -1:
					if j == len(self.players[i].hands)-1:
						self.busted.append(self.players[i])

				elif move == 2:
					if self.players[i].name == 'Bot':
						self.players[i].add(self.bot_deck.pop(),j)
					else:
						self.players[i].add(self.deck.draw(),j)
					self.players[i].doubled_down = True
					self.players[i].cash -= self.players[i].bet
					self.players[i].bet *= 2
					if j == len(self.players[i].hands)-1:
						newplayers.append(self.players[i]) # STAND?

				elif move == 3:
					self.players[i].aces.append(0)
					self.players[i].tmp.append(0)

					self.players[i].hands.append([])
					card2 = self.players[i].hands[0].pop()
					self.players[i].val[0] = 0
					self.players[i].add(self.players[i].hands[0].pop(),0)
					self.players[i].cash -= self.players[i].bet
					self.players[i].val.append(0)
					self.players[i].add(card2,1)
					
					if self.players[i].name == 'Bot':
						self.players[i].add(self.bot_deck.pop(),0)
						self.players[i].add(self.bot_deck.pop(),1)						
					else:
						self.players[i].add(self.deck.draw(),0)
						self.players[i].add(self.deck.draw(),1)
					newplayers.append(self.players[i])
					
				else:
					if j == len(self.players[i].hands)-1:
						self.stand.append(self.players[i])

		self.players = newplayers

	def reset_count(self):
		self.bot.rcount = 0
		self.bot.tcount = 0
		self.bot.dead_cards = 0

	def __repr__(self):
		repr = ['\n']
		repr.append('Dealer: ' + str(self.dealer))
		for player in self.players:
			repr.append('Active Player --> ' + str(player))
		for player in self.stand:
			repr.append('Standing Player --> ' + str(player))
		for player in self.busted:
			repr.append('Busted Player --> ' + str(player))
		repr.append('\n')
		return '\n'.join(repr)
