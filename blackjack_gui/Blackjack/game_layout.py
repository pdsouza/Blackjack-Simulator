import wx
from Bot import Bot
from Dealer import Dealer
from Deck import Deck
from Game import Game
from Person import Person
from Player import Player
from RulesEngine import RulesEngine

game = Game()
print game

class Blackjack_layout(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.BUTTON_PADDING = 36
        self.CARD_PADDING = 75
        self.prebet = True
        self.card_dict = {}
        
        self.panelA = wx.Window(self, style = wx.SIMPLE_BORDER)
        self.panelA.SetBackgroundColour("GREEN")
        
        self.panelB = wx.Window(self, style = wx.SIMPLE_BORDER)
        
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.panelA, 2.5, wx.EXPAND)
        box.Add(self.panelB, 1, wx.EXPAND)
        
        self.logger = wx.TextCtrl(self, pos = (0, 450), size=(800, 150), style=wx.TE_MULTILINE | wx.TE_READONLY)
        
        self.SetSizer(box)
        self.Layout()
        
        self.button1 = wx.Button(self.panelB, id=-1, label='Stand', pos=(47, 8), size=(175, 28))
        self.button2 = wx.Button(self.panelB, id=-1, label='Hit', pos=(47, 8 + self.BUTTON_PADDING), size=(175, 28))
        self.button3 = wx.Button(self.panelB, id=-1, label='Double Down', pos=(47, 8 + 2*self.BUTTON_PADDING), size=(175, 28))
        self.button4 = wx.Button(self.panelB, id=-1, label='Split', pos=(47, 8 + 3*self.BUTTON_PADDING), size=(175, 28))
        self.button5 = wx.Button(self.panelB, id=-1, label='Clear Text', pos=(47, 8 + 4*self.BUTTON_PADDING), size=(175, 28))
        self.button6 = wx.Button(self.panelB, id=-1, label='Bet!', pos=(134, 8 + 7*self.BUTTON_PADDING), size=(87, 28))
                
        self.button1.Bind(wx.EVT_BUTTON, self.stand)
        self.button2.Bind(wx.EVT_BUTTON, self.hit)
        self.button3.Bind(wx.EVT_BUTTON, self.double_down)
        self.button4.Bind(wx.EVT_BUTTON, self.split)
        self.button5.Bind(wx.EVT_BUTTON, self.clear)
        self.button6.Bind(wx.EVT_BUTTON, self.update_bet)
        
        self.slider = wx.Slider(self.panelB, -1, 0, 0, 300, (47, 8 + 6*self.BUTTON_PADDING), (175, 28),
                                wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.statictext = wx.StaticText(self.panelB, -1, "Bet: 0", (53, 8 + 7*self.BUTTON_PADDING), (87, 28))
        self.slider.Bind(wx.EVT_SLIDER, self.slider_update)
        
        self.img_convert()
        self.show_cards()
        
    def stand(self, event):
        self.logger.WriteText("Stand\n")
        game.move = 0
        game.run()
        while game.ongoing():
            game.run()
        game.payout()
        self.show_cards()
        print game
    
    def hit(self, event):
        self.logger.WriteText("Hit\n")
        game.move = 1
        game.run()
        self.show_cards()
        print game
    
    def double_down(self, event):
        self.logger.WriteText("Doubled Down\n")
        game.move = 2
        game.run()
        self.show_cards()
        print game
    
    def split(self, event):
        self.logger.WriteText("Split\n")
        game.move = 3
        game.run()
        self.show_cards()
        print game
        
    def clear(self, event):
        self.logger.Clear()
        
    def slider_update(self, event):
        self.statictext.SetLabel("Bet: " + str(self.slider.GetValue()))
        
    def update_bet(self, event):
        self.prebet = False     #REMEMBER TO SET BACK
        game.players[0].cash += game.players[0].bet
        game.players[0].bet = self.slider.GetValue()
        game.players[0].cash -= game.players[0].bet
        self.show_cards()
        
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
            wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175, 20))
            wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175 + self.CARD_PADDING/2, 20))
            wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175, 325))
            wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175 + self.CARD_PADDING/2, 325))
            
        elif not game.ongoing():
            hand = game.dealer.hands[0]
            for i in xrange(0, len(hand)):
                wx.StaticBitmap(self.panelA, -1, self.card_dict[hand[i]], (175 + i*self.CARD_PADDING/2, 20))
            
        else:
            hand = game.dealer.hands[0]
            wx.StaticBitmap(self.panelA, -1, self.bottomImage, (175, 20))
            wx.StaticBitmap(self.panelA, -1, self.card_dict[hand[1]], (175 + self.CARD_PADDING/2, 20))
            
#            for i in xrange(1, len(hand)):
#                wx.StaticBitmap(self.panelA, -1, self.card_dict[hand[i]], (175 + i*self.CARD_PADDING/2, 20))
                
            hand = game.rules.players[0].hands[0]
            for i in xrange(0, len(hand)):
                wx.StaticBitmap(self.panelA, -1, self.card_dict[hand[i]], (175 + i*self.CARD_PADDING/2, 325))
        
#    def paint(self, event):
#            self.dc = wx.PaintDC(self.panelA)
#            self.dc.Clear()
#            self.dc.BeginDrawing()
#            self.dc.SetPen(wx.Pen("Black", 1))
#            self.dc.DrawRectangle(150, 30, 75, 110)
#            self.dc.EndDrawing()
        
#class info_layout(wx.Panel):
#    def __init__(self, parent):
#        wx.Panel.__init__(self, parent, pos = (200, 200))
#        
#        self.logger = wx.TextCtrl(self, size=(800,150), style=wx.TE_MULTILINE | wx.TE_READONLY)
        
app = wx.App(False)
window = wx.Frame(None, -1, pos = wx.Point(300, 150), title = "Blackjack!", size = wx.Size(800, 600))
toppanel = Blackjack_layout(window)
window.Show()
app.MainLoop()