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

        
app = wx.App(False)
frame = MyFrame(None, 'Small editor')
app.MainLoop()
