#!/usr/bin/env python
import wx
from ParetoAnalyzer import ParetoAnalyzer
class Results(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640,400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

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
