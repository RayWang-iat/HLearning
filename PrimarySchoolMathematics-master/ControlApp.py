"""
App  Author   : Rui Wang
                Taili Yuan
                Haitao Wang
Finished time : 2021.3.20
Python version: Python 3.6.1


"""

import wx
from App_Math import MyApp
from App_Chinese import MyApp_ch
from App_English import MyEnglishAPP

class Create_Frame(wx.Frame):
    def __init__(self, parent, title):
        super(Create_Frame, self).__init__(parent, title=title, size=(800, 800))
        panel = wx.Panel(self)
        panel.SetBackgroundColour((255,255,204))
        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        self.icon = wx.Icon('hfut.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        vbox = wx.BoxSizer(wx.VERTICAL)
        sbox = wx.StaticBox(panel, -1, '试题类型选择', style=wx.CENTER)
        sboxSizer = wx.StaticBoxSizer(sbox, wx.VERTICAL)
        hbox = wx.BoxSizer(wx.VERTICAL)
        ChineseButton = wx.Button(panel, -1, '语文试题')
        self.Bind(wx.EVT_BUTTON, self.Chines_iems, ChineseButton)
        hbox.Add(ChineseButton, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        MathButton = wx.Button(panel, -1, '数学试题')
        EnglishButton = wx.Button(panel, -1, '英语试题')
        self.Bind(wx.EVT_BUTTON, self.Math_iems, MathButton)
        self.Bind(wx.EVT_BUTTON, self.English_iems, EnglishButton)
        hbox.Add(MathButton, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        hbox.Add(EnglishButton, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        sboxSizer.Add(hbox, proportion=3, flag=wx.ALL | wx.CENTER, border=10)
        vbox.Add(sboxSizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        panel.SetSizer(vbox)

        self.Centre()

        panel.Fit()
        self.Show()



    def Chines_iems(self,event):
        app = MyApp_ch(0)
        app.MainLoop()

    def English_iems(self,event):
        app = MyEnglishAPP(0)
        app.MainLoop()

    def Math_iems(self,event):
        app = MyApp(0)
        app.MainLoop()

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        p = wx.Image("background.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()  # 载入图片
        img = p.ConvertToImage()
        bgm = img.Scale(800, 800)
        bmp = wx.Bitmap(bgm)
        dc.DrawBitmap(bmp, 0, 0)



class MyAPP(wx.App):
    def OnInit(self):
        self.frame = Create_Frame(None,  'Hlearning小学智慧试题生成系统')
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyAPP(0)
    app.MainLoop()