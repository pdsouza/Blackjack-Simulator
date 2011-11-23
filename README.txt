***You must have wxPython installed in order to run the GUI.

To run the game, run game_layout.py.

This is a Blackjack training game. The goal of the game is to try to match your strategy to a perfect Blackjack bot.

As in typical Blackjack, you will be dealt two cards after placing your bet. In order to place your bet, you can either use the slider or you can type in your bet in the text box. Don't forget to press ENTER after typing in the bet. Then press the Bet button.

After you receive your cards, you are given four options: Stand, Hit, Double Down, and Split.

Stand means that you do not wish to receive any more cards.
Hit means you want to be dealt another card.
Double Down doubles your bet and gives you only one more card.
Split is only available if you have a pair. You are then able to split the pair and play both hands independently. Your bet is also doubled because you now have two hands to play.

There are two more buttons in the interface: Clear Text and Next Round.

Clear Text clears the text that is shown at the bottom of the screen.
Next Round brings you to the next round, where everything starts over again.

The text area you see at the bottom of the window has two sections; the left section keeps track of your earnings while the right section keeps track of the bot's moves and earnings. This allows you to compare your strategy with the bot's strategy.

The bot follows a perfect Blackjack strategy but with card counting in order to maximize earnings. Usually casinos will give you a cheat sheet showing a perfect Blackjack strategy. The bot plays accordingly. In addition to this strategy, the bot will keep a running count of the deck and alters his bet based on the count.

If your cash value drops to 0 or below, the game will exit.