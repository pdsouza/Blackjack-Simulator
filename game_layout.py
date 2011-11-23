import wx
import sys
from Bot import Bot
from Dealer import Dealer
from Deck import Deck
from Game import Game
from Person import Person
from Player import Player
from RulesEngine import RulesEngine

game = Game()

class Blackjack_layout(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.BUTTON_PADDING = 36
        self.CARD_PADDING = 75
        self.finished_hands = 0
        self.prebet = True
        self.card_dict = {}
        self.drawn_cards = []
        self.buttons = []
        self.player = game.rules.players[0]
        self.dealer = game.rules.dealer
        self.bot = game.bot
        self.round_number = 1
        
        self.panelA = wx.Window(self, style = wx.SIMPLE_BORDER)
        self.panelA.SetBackgroundColour("GREEN")
        
        self.panelB = wx.Window(self, style = wx.SIMPLE_BORDER)
        
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.box.Add(self.panelA, 2.5, wx.EXPAND)
        self.box.Add(self.panelB, 1, wx.EXPAND)
        
        self.logger = wx.TextCtrl(self, pos=(0, 431), size=(400, 150), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.bot_logger = wx.TextCtrl(self, pos=(396, 431), size=(404, 150), style=wx.TE_MULTILINE | wx.TE_READONLY)
        
        self.SetSizer(self.box)
        self.Layout()
        
        self.bet_box = wx.TextCtrl(self.panelB, pos=(170, 8 + 7*self.BUTTON_PADDING), size=(50, 20), style=wx.TE_PROCESS_ENTER)
        
        self.stand_button = wx.Button(self.panelB, id=-1, label='Stand', pos=(47, 8), size=(175, 28))
        self.hit_button = wx.Button(self.panelB, id=-1, label='Hit', pos=(47, 8 + self.BUTTON_PADDING), size=(175, 28))
        self.double_button = wx.Button(self.panelB, id=-1, label='Double Down', pos=(47, 8 + 2*self.BUTTON_PADDING), size=(175, 28))
        self.split_button = wx.Button(self.panelB, id=-1, label='Split', pos=(47, 8 + 3*self.BUTTON_PADDING), size=(175, 28))
        self.clear_button = wx.Button(self.panelB, id=-1, label='Clear Text', pos=(47, 8 + 4*self.BUTTON_PADDING), size=(175, 28))
        self.bet_button = wx.Button(self.panelB, id=-1, label='Bet!', pos=(47, 8 + 8*self.BUTTON_PADDING), size=(175, 28))
        self.reset_button = wx.Button(self.panelB, id=-1, label='Next Round', pos=(47, 8 + 10.5*self.BUTTON_PADDING), size=(175, 28))
        
        if self.player.hands[0][0][1] != self.player.hands[0][1][1]:
            self.split_button.Disable()
        self.reset_button.Disable()
        
        self.buttons.extend([self.stand_button, self.hit_button, self.double_button, self.split_button, self.clear_button, self.bet_button])
        for button in self.buttons[:-1]:
            button.Disable()
                
        self.stand_button.Bind(wx.EVT_BUTTON, self.stand)
        self.hit_button.Bind(wx.EVT_BUTTON, self.hit)
        self.double_button.Bind(wx.EVT_BUTTON, self.double_down)
        self.split_button.Bind(wx.EVT_BUTTON, self.split)
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear)
        self.bet_button.Bind(wx.EVT_BUTTON, self.update_bet)
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset)
        self.bet_box.Bind(wx.EVT_TEXT_ENTER, self.bet_text_slider)
        
        self.slider = wx.Slider(self.panelB, -1, 0, 0, self.player.cash + self.player.bet, (47, 8 + 6*self.BUTTON_PADDING), (175, 28),
                                wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.statictext = wx.StaticText(self.panelB, -1, "Bet: $0", (53, 8 + 7*self.BUTTON_PADDING), (87, 28))
        self.slider.Bind(wx.EVT_SLIDER, self.slider_update)
        
        self.img_convert()
        self.show_cards()
        
    def bet_text_slider(self, event):
        self.slider.SetValue(int(self.bet_box.GetValue()))
        self.slider_update(None)
        self.bet_box.Clear()
        
    def finish_round(self):
        while game.ongoing():
            game.run()
        game.payout()
        self.show_cards()
        for button in self.buttons:
            button.Disable()
        self.reset_button.Enable(True)
        
    def test_win(self, player, hand):
        if player.val[hand] > 21:
            return -1
        elif (self.dealer.val[0] < player.val[hand] and player.val[hand] <= 21) or (self.dealer.val[0] > 21 and player.val[hand] <=21):
            return 1
        elif self.dealer.val[0] == player.val[hand]:
            return 0
        
    def print_result(self):
        for hand,move in game.bot_moves:
            if move == 0:
                self.bot_logger.WriteText("The bot stood.\n")
            elif move == 1:
                self.bot_logger.WriteText("The bot hit.\n")
            elif move == 2:
                self.bot_logger.WriteText("The bot doubled down.\n")
            elif move == 3:
                self.bot_logger.WriteText("The bot split.\n")
        
        for hand in xrange(0, len(self.bot.hands)):
            if self.test_win(self.bot, hand) == 1:
                self.bot_logger.WriteText("The bot won the hand and $%d!\n" %self.bot.bet)
            elif self.test_win(self.bot, hand) == 0:
                self.bot_logger.WriteText("The bot pushed.\n")
            else: self.bot_logger.WriteText("The bot lost the hand and $%d.\n" %self.bot.bet)
        
        for hand in xrange(0, len(self.player.hands)):
            if self.test_win(self.player, hand) == 1:
                self.logger.WriteText("You won the hand and $%d!\n" %self.player.bet)
            elif self.test_win(self.player, hand) == 0:
                self.logger.WriteText("You push.\n")
            else: self.logger.WriteText("You lost the hand and $%d.\n" %self.player.bet)
        if self.player.cash <= 0:
            self.logger.WriteText("You're broke. Game exiting.\n")
            wx.FutureCall(2000, lambda : sys.exit())
        
    def stand(self, event):
        game.move = 0
        game.move_player(self.player, self.finished_hands)
        self.finished_hands += 1
        
        if self.finished_hands == len(self.player.hands):
            self.finish_round()
            self.print_result()
        else: self.logger.WriteText("Play the second hand.\n")
    
    def hit(self, event):
        game.move = 1
        game.move_player(self.player, self.finished_hands)
        self.show_cards()
        self.double_button.Disable()
        self.split_button.Disable()
        
        for hand in xrange(0,len(self.player.hands)):
            if self.player.val[hand] > 21:
                self.finished_hands += 1
                game.move = -1
                
                if self.finished_hands == len(self.player.hands):
                    self.finish_round()
                    self.print_result()
                else: self.logger.WriteText("Play the second hand.\n")
            break
    
    def double_down(self, event):
        self.logger.WriteText("You doubled your bet.\n")
        game.move = 2
        game.run()
        self.show_cards()
        while game.ongoing():
            if self.player.val[0] > 21:
                game.move = -1
            else: game.move = 0
            game.run()
            
        for button in self.buttons:
            button.Disable()
            
        game.payout()
        self.show_cards()
        self.reset_button.Enable(True)
        self.print_result()
    
    def split(self, event):
        self.logger.WriteText("You split. Bottom hand plays first.\n")
        game.move = 3
        game.run()
        self.show_cards()
        self.double_button.Disable()
        self.split_button.Disable()
                
    def clear(self, event):
        self.logger.Clear()
        self.bot_logger.Clear()
        
    def slider_update(self, event):
        self.statictext.SetLabel("Bet: $" + str(self.slider.GetValue()))
        
    def update_bet(self, event):
        self.prebet = False
        self.player.cash += self.player.bet
        self.player.bet = self.slider.GetValue()
        self.player.cash -= self.player.bet
        self.show_cards()
        for button in self.buttons:
            button.Enable(True)
        if self.player.hands[0][0][1] != self.player.hands[0][1][1]:
            self.split_button.Disable()
        self.bet_button.Disable()
        self.slider.Disable()
        self.bet_box.Disable()
        self.bot_logger.WriteText("The bot bet $%d.\n" % self.bot.bet)
        
    def reset(self, event):
        game.reset()
        self.erase_cards()
        self.prebet = True
        self.show_cards()
        self.round_number += 1
            
        self.logger.WriteText("-------------------\nCash: $%d\n" % (self.player.cash + self.player.bet))
        self.logger.WriteText("Round %d\n" % self.round_number)
        self.bot_logger.WriteText("-------------------\nCash: $%d\n" % (self.bot.cash + self.bot.bet))
        self.bot_logger.WriteText("Round %d\n" % self.round_number)
        
        self.reset_button.Disable()
        if self.player.hands[0][0][1] != self.player.hands[0][1][1]:
            self.split_button.Disable()
        for button in self.buttons[:-1]:
            button.Disable()
        self.bet_button.Enable(True)
        self.finished_hands = 0
        self.slider.Enable(True)
        self.slider.SetMax(self.player.cash + self.player.bet)
        self.bet_box.Enable(True)
        
    def erase_cards(self):
        for image in self.drawn_cards:
            image.Show(False)
        self.drawn_cards = []
        
    def img_convert(self):
        for i in xrange(2, 15):
            for s in ["C", "D", "H", "S"]:
                if i < 10:
                    imageFile = "0" + str(i) + s.lower() + ".gif"
                else:
                    imageFile = str(i) + s.lower() + ".gif"
                image = wx.Image("./cardset-gpl/" + imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                self.card_dict[(s, i if i <= 10 else ["J", "Q", "K", "A"][i - 11])] = wx.Image("./cardset-gpl/" + imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bottomImage = wx.Image("./cardset-gpl/back01.gif", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

    def show_cards(self):
        if self.prebet:
            a = wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175, 20))
            b = wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175 + self.CARD_PADDING/2, 20))
            c = wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175, 325))
            d = wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175 + self.CARD_PADDING/2, 325))
            self.drawn_cards.extend([a, b, c, d])
            
        elif not game.ongoing():
            hand = game.dealer.hands[0]
            for i in xrange(0, len(hand)):
                e = wx.StaticBitmap(self.panelA, -1, self.card_dict[hand[i]], (175 + i*self.CARD_PADDING/2, 20))
                self.drawn_cards.append(e)
                
        elif game.move == 3:
            hands = self.player.hands
            for j in xrange(0, len(hands)):
                for i in xrange(0, len(hands[j])):
                    k = wx.StaticBitmap(self.panelA, -1, self.card_dict[hands[j][i]], (175 + i*self.CARD_PADDING/2, 220 if j == 1 else 325))
                    self.drawn_cards.append(k)
            
        else:
            hand = game.dealer.hands[0]
            f = wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175, 20))
            g = wx.StaticBitmap(self.panelA, -1, self.card_dict[hand[1]], (175 + self.CARD_PADDING/2, 20))
            self.drawn_cards.extend([f, g])
                
            hands = self.player.hands
            for j in xrange(0, len(hands)):
                for i in xrange(0, len(hands[j])):
                    k = wx.StaticBitmap(self.panelA, -1, self.card_dict[hands[j][i]], (175 + i*self.CARD_PADDING/2, 220 if j == 1 else 325))
                    self.drawn_cards.append(k)
                    
class game_window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title = title, size = wx.Size(800, 600))
        self.CenterOnScreen()
        self.player = game.rules.players[0]
        self.bot = game.bot
        
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(201, "&Instructions")
        menuBar.Append(menu1, "&Help")
        
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.help_menu, id = 201)
        self.instructions = open("instructions.txt", "r").read()
        
    def help_menu(self, event):
        help_dlg = wx.MessageDialog(self, self.instructions, "Instructions", wx.OK | wx.ICON_INFORMATION)
        help_dlg.ShowModal()
        help_dlg.Destroy()
        
def show_initial(layout):
    layout.logger.WriteText("Initial Cash: $%d\n" % (game.rules.players[0].cash + game.rules.players[0].bet))
    layout.logger.WriteText("Decks: %d\n" % (game.num_decks))
    layout.logger.WriteText("-------------------\n")
    layout.logger.WriteText("Round 1\n")
    
    layout.bot_logger.WriteText("Initial Bot Cash: $%d\n" % (game.bot.cash + game.bot.bet))
    layout.bot_logger.WriteText("Decks: %d\n" % (game.num_decks))
    layout.bot_logger.WriteText("-------------------\n")
    layout.bot_logger.WriteText("Round 1\n")
        
app = wx.App(False)
window = game_window(None, -1, "Blackjack!")
toppanel = Blackjack_layout(window)
window.Show()
while True:
    enter_cash = wx.GetNumberFromUser("", "Enter your starting cash value.", "Initial Cash", 0, 0, 999999999, parent = window)
    if not (enter_cash == -1 or enter_cash == 0):
        game.rules.players[0].cash = enter_cash - game.rules.players[0].bet
        game.bot.cash = enter_cash - game.bot.bet
        break
show_initial(toppanel)
app.MainLoop()
