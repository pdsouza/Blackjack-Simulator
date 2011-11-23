from Dealer import Dealer
from Deck import Deck
from Game import Game

NUM_GAMES = 1 # number of simultaneous games
NUM_PLAYERS = 1 # number of normal players
NUM_DECKS = 6
NUM_ROUNDS = 50*3 # 50 hands per hour

games = [Game(NUM_PLAYERS, NUM_DECKS) for i in xrange(0,NUM_GAMES)]
done = []

for round in xrange(0,NUM_ROUNDS):
	print '\n\nBEGINNING\n\n' + str(games)
	while len(done) < len(games):
		for i in xrange(0,len(games)):
			if games[i].ongoing():
				games[i].run()
			elif games[i] not in done: 
				done.append(games[i])


	print '\n\nEND\n\n'
	for game in games: 
		game.payout()
		print game
		if round != NUM_ROUNDS-1:
			game.reset()

	done = []
	round += 1


	print '-------------------------'

dealer_wins, player_wins, ties = 0.0, 0.0, 0.0
player_cash = {}
averages = {}

for i in xrange(0,len(games)):
	for player in games[i].rules.players:
		if player.name in player_cash:
			player_cash[player.name] += [player.cash]
		else:
			player_cash[player.name] = [player.cash]

for k,v in player_cash.items():
	averages[k] = int(reduce(lambda x,y:x+y,v)/NUM_GAMES)
	player_cash[k].sort()

wins = 0
for c in player_cash['Bot']:
	if c > 3000: wins += 1

print 'AVERAGE: ' + str(averages)
print 'MEDIAN: ' + str(player_cash['Bot'][NUM_GAMES/2])
print 'WINS: ' + str(wins)


print player_cash['Bot']

