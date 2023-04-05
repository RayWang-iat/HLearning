#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import wx


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.icon = wx.Icon('hfut.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.SetTitle('关注我们')
        self.SetSize(320,450)
        image_file = 'Code_N.jpg'
        to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))


class MyApp_Aboutus(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

def main():
    app = MyApp_Aboutus(0)
    app.MainLoop()

if __name__ == "__main__":
    main()
