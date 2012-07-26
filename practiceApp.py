#!/usr/bin/env python
import wx
from ParetoAnalyzer import ParetoAnalyzer
class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(900,600))
        txt1 = wx.StaticText(self, -1, "Select a file. DUDE!")
        
        self.dir = wx.GenericDirCtrl(self, -1, size=(900,600), style=0, filter = "*.csv")

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSel, self.dir.TreeCtrl)
        
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)

    def onSel(self, event):
        filename = self.dir.GetFilePath()
        if(filename):
            print (filename)

class Results(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640,400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        testButton = wx.Button(panel)
        testButton.SetPosition((5, 365))
        testButton.Bind(wx.EVT_BUTTON, self.update_values)

        self.headFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_BOLD, wx.FONTSTYLE_NORMAL)
        self.bigNumberFont = wx.Font(64, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_BOLD, wx.FONTSTYLE_NORMAL)
        self.regNumberFont = wx.Font(42, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_BOLD, wx.FONTSTYLE_NORMAL)


        #wx has horrible text helper. Let's write our own.
        def make_text(text, position, font):
            header = wx.StaticText(panel, -1, text)
            header.SetPosition(position)
            header.SetFont(font)
            return header
        def make_header(text, position):
            return make_text(text, position, self.headFont)
        def make_big_number(position):
            return make_text("00", position, self.bigNumberFont)
        def make_reg_number(position):
            return make_text("00", position, self.regNumberFont)
        
        #make headers
        revPercentHeader = make_header("Percent of Revenue", (360,20))
        revAmountHeader = make_header("Amount of Revenue", (360,160))
        idPercentHeader = make_header("Percent of IDs", (20,20))
        idAmountHeader = make_header("Amount of IDs", (20,160))

        #make numbers
        self.revPercent = make_big_number((360, 40))
        self.revAmount = make_reg_number((360, 180))
        self.idPercent = make_big_number((20, 40))
        self.idAmount = make_reg_number((20, 180))

        #m_text.SetSize(m_text.GetBestSize())


        #m_text.SetLabel(str(self.pareto.get_range_info(80,100)))

    def update_values(self, event):
        data = self.pareto.get_range_info(80,100)
        self.revPercent.SetLabel(self.format_value_string(data['revPercent'], True))
        self.revAmount.SetLabel("$"+self.format_value_string(data['revTotal']))
        self.idPercent.SetLabel(self.format_value_string(data['idPercent'], True))
        self.idAmount.SetLabel(self.format_value_string(data['idTotal']))


    def create_pareto(self, fileName):
        self.pareto = ParetoAnalyzer(fileName)

    def format_value_string(self, value, percent=False):
        if(percent):
            return str(int(value))+"%"
        else:
            if(int(value)/1000000 > 0):
                print value/1000000.0
                return '%0.1fM' % (value/1000000.0)
            elif(int(value)/1000 > 0):
                return '%0.1fK' % (value/1000.0)
            else:
                return str(int(value))




    def OnClose(self, event):
        self.Destroy()

app = wx.App(False)
#frame = MyFrame(None, 'Small editor')

results = Results(None, 'Testing Results')
results.Show()
results.create_pareto("test.csv")
app.MainLoop()
