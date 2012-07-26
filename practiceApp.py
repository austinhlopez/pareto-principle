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
        
        self.leftPanel = leftPanel(self.split1)
        
        self.rightPanel = rightPanel(self.split1)
        
        #Add controls to the splitters:
        self.split1.SplitVertically(self.leftPanel, self.rightPanel)

        #txt1 = wx.StaticText(self, -1, "Select a file. DUDE!")
        
        
        #      self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)

    

#Left Panel: Contains directory and handles traversal.
class leftPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        # Create the panel.
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        #self.dir = wx.GenericDirCtrl(self, -1, size=(900,600), style=0, filter = "*.csv")

        #       self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSel, self.dir.TreeCtrl)
    
        def onSel(self):
            pass
        #     txt1 = wx.St

#Right Panel: CSV Upload bar and instructions.
class rightPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        # Create the panel.
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.SetBackgroundColour('cyan')


        self.parent = parent

        #Right Panel: Instructions on formatting, upload file bar
        self.button = wx.Button(self, label="Calculate")
        self.fileUpload = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)

        # Add buttons, file uploader.
        self.uploadSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.uploadBar = wx.BoxSizer(wx.HORIZONTAL)
        self.uploadBar.Add(self.fileUpload, 1)
        self.uploadBar.Add(self.button, 1)

        self.instructions = wx.StaticText(self, label="""1. Upload a CSV file \n\n Your CSV should contain two columns: a column of item IDs and a column of transaction amounts, separated by commas. No headers please. \n\n Example: \n
 '1321', 24.95 \n '1322', 16.50 \n '1321', 22.95""")

        self.uploadSizer.Add(self.instructions)
        self.uploadSizer.Add(self.uploadBar)

        self.SetSizer(self.uploadSizer)
        self.SetAutoLayout(True)
        self.uploadSizer.Fit(self)

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

        
app = wx.App(False)
frame = MyFrame(None, 'Pareto Principle')
app.MainLoop()
