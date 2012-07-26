#!/usr/bin/env python
import wx
from ParetoAnalyzer import ParetoAnalyzer
class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(900,600))

        self.SetBackgroundColour('cyan')

        #Create splitters:
        self.split1 = ProportionalSplitter(self, -1, 0.5)
        
        #self.split1 = wx.SplitterWindow(self)
        #self.split2 = wx.SplitterWindow(self.split1)
        
        self.leftPanel = leftPanel(self, self.split1)
        
        self.rightPanel = rightPanel(self, self.split1)
        
        #Add controls to the splitters:
        self.split1.SplitVertically(self.leftPanel, self.rightPanel)

        #txt1 = wx.StaticText(self, -1, "Select a file. DUDE!")
        
        
        #      self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)

    def populateTextCtrl(self, filePath):
        self.rightPanel.populateTextCtrl(filePath);

    

#Left Panel: Contains directory and handles traversal.
class leftPanel(wx.Panel):
    def __init__(self, primaryFrame, parent, *args, **kwargs):
        # Create the panel.
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.primaryFrame = primaryFrame
        self.dir = wx.GenericDirCtrl(self, -1, size=(900,600), style=0, filter = "*.csv")

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSel, self.dir.TreeCtrl)
    
    def onSel(self, event):
<<<<<<< HEAD
        self.primaryFrame.populateTextCtrl(self.dir.GetFilePath())

#Right Panel: CSV Upload bar and instructions.
class rightPanel(wx.Panel):
    def __init__(self, primaryFrame, parent, *args, **kwargs):
        # Create the panel.
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.primaryFrame = primaryFrame

        #Right Panel: Instructions on formatting, upload file bar
        self.button = wx.Button(self, label="Calculate")
        self.fileUpload = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        
        # Add buttons, file uploader.
        self.uploadSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.uploadBar = wx.BoxSizer(wx.HORIZONTAL)
        self.uploadBar.Add(self.fileUpload, 1, wx.EXPAND)
        self.uploadBar.Add(self.button, 0, wx.EXPAND)

        self.SetAutoLayout(True)
        
        self.instructions = wx.StaticText(self, label="""1. Upload a CSV file \n\n Browse for your CSV on the left, or enter the full path name in the text box below. Your CSV should contain two columns: a column of item IDs and a column of transaction amounts, separated by commas. No headers please. \n\n Example: \n
 '1321', 24.95 \n '1322', 16.50 \n '1321', 22.95 \n\n\n""")

        self.uploadSizer.Add(self.instructions)
        self.uploadSizer.Add(self.uploadBar, .2, wx.EXPAND)
       
        self.SetSizer(self.uploadSizer)
        self.SetAutoLayout(True)
        self.uploadBar.Fit(self)
        self.uploadSizer.Fit(self)
        
        self.instructions.Wrap(430)


    def populateTextCtrl(self, filePath):
        self.fileUpload.WriteText(filePath);

class ProportionalSplitter(wx.SplitterWindow):
    def __init__(self,parent, id = -1, proportion=0.66, size = wx.DefaultSize, **kwargs):
        wx.SplitterWindow.__init__(self,parent,id,wx.Point(0, 0),size, **kwargs)
        self.SetMinimumPaneSize(50) #the minimum size of a pane.
        self.proportion = proportion
        if not 0 < self.proportion < 1:
            raise ValueError, "proportion value for ProportionalSplitter must be between 0 and 1."
        self.ResetSash()
        self.Bind(wx.EVT_SIZE, self.OnReSize)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged, id=id)
                ##hack to set sizes on first paint event
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.firstpaint = True
        
    def SplitHorizontally(self, win1, win2):
        if self.GetParent() is None: return False
        return wx.SplitterWindow.SplitHorizontally(self, win1, win2,
                                                   int(round(self.GetParent().GetSize().GetHeight() * self.proportion)))
        
    def SplitVertically(self, win1, win2):
        if self.GetParent() is None: return False
        return wx.SplitterWindow.SplitVertically(self, win1, win2,
                                                     int(round(self.GetParent().GetSize().GetWidth() * self.proportion)))
        
    def GetExpectedSashPosition(self):
        if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().height)
        else:
            tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().width)
        return int(round(tot * self.proportion))
            
    def ResetSash(self):
        self.SetSashPosition(self.GetExpectedSashPosition())
                
    def OnReSize(self, event):
        "Window has been resized, so we need to adjust the sash based on self.proportion."
        self.ResetSash()
        event.Skip()
            
    def OnSashChanged(self, event):
        "We'll change self.proportion now based on where user dragged the sash."
        pos = float(self.GetSashPosition())
        if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().height)
        else:
            tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().width)
        self.proportion = pos / tot
        event.Skip()

    def OnPaint(self,event):
        if self.firstpaint:
            if self.GetSashPosition() != self.GetExpectedSashPosition():
                self.ResetSash()
            self.firstpaint = False
        event.Skip()
=======
        filename = self.dir.GetFilePath()
        if(filename):
            print (filename)

class Results(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640,400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
>>>>>>> ce74e5dae923dec482fef19fbe0f8e51de37144a

        self.headFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_BOLD, wx.FONTSTYLE_NORMAL)
        self.bigNumberFont = wx.Font(64, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_BOLD, wx.FONTSTYLE_NORMAL)
        self.regNumberFont = wx.Font(42, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_BOLD, wx.FONTSTYLE_NORMAL)
        
        button = wx.Button(panel, -1)
        button.SetPosition((450, 320))
        button.SetLabel("Save IDs")
        button.Bind(wx.EVT_BUTTON, self.OnSave)

        def make_range_slider(position):
            slider = wx.Slider(panel, 99,
                    pos=(position),
                    size=(250, -1),
                    style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS )
            slider.SetRange(0, 100)
            slider.SetTickFreq(5, 1)
            return slider

        self.minSlider = make_range_slider((170,280))
        self.minSlider.SetValue(80)
        self.minSlider.Bind(wx.EVT_SLIDER, self.update_values)
        self.maxSlider = make_range_slider((170,320))
        self.maxSlider.SetValue(100)
        self.maxSlider.Bind(wx.EVT_SLIDER, self.update_values)

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
        lo = min(self.minSlider.GetValue(), self.maxSlider.GetValue())
        hi = max(self.minSlider.GetValue(), self.maxSlider.GetValue())
        data = self.pareto.get_range_info(lo,hi)
        self.revPercent.SetLabel(self.format_value_string(data['revPercent'], True))
        self.revAmount.SetLabel("$"+self.format_value_string(data['revTotal']))
        self.idPercent.SetLabel(self.format_value_string(data['idPercent'], True))
        self.idAmount.SetLabel(self.format_value_string(data['idTotal']))


    def create_pareto(self, fileName):
        self.pareto = ParetoAnalyzer(fileName)
        self.update_values(None)

    def format_value_string(self, value, percent=False):
        if(percent):
            return str(int(value))+"%"
        else:
            if(int(value)/1000000 > 0):
                return '%0.1fM' % (value/1000000.0)
            elif(int(value)/1000 > 0):
                return '%0.1fK' % (value/1000.0)
            else:
                return str(int(value))


    def OnSave(self, event):
        lo = min(self.minSlider.GetValue(), self.maxSlider.GetValue())
        hi = max(self.minSlider.GetValue(), self.maxSlider.GetValue())
        
        try:
            msg = "Saved as " + self.pareto.save_range(lo, hi)
        except IOError as e:
            msg = str(e)

        dlg = wx.MessageDialog(self, msg, "OK", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnClose(self, event):
            self.Destroy()

app = wx.App(False)
<<<<<<< HEAD
frame = MyFrame(None, 'Pareto Principle')
=======
#frame = MyFrame(None, 'Small editor')

results = Results(None, 'Testing Results')
results.Show()
results.create_pareto("test.csv")
>>>>>>> ce74e5dae923dec482fef19fbe0f8e51de37144a
app.MainLoop()
