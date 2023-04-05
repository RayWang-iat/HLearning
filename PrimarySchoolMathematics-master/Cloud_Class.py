import wx

def loadframe():

    app = wx.App()

    mywindow = myframe()

    mywindow.Show()

    app.MainLoop()


class myframe(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self,None,-1,u'词云统计',size=(1200,600))
        self.icon = wx.Icon('hfut.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.SetBackgroundColour((255, 255, 255))
        mypanel = wx.Panel(self,-1,size=(1200,800))

        image = wx.Image(r'ChineseCloud.jpg',wx.BITMAP_TYPE_JPEG)
        portion = 0.75
        w = image.GetWidth()*portion
        h = image.GetHeight()*portion
        image.Rescale(w,h)
        mypic = image.ConvertToBitmap()
        wx.StaticBitmap(mypanel,-1,bitmap=mypic,pos=(15,2))
        custom=wx.StaticText(mypanel, -1, label='语文词云统计图', pos=(120,500))
        custom.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        custom.SetForegroundColour((0,0,0))


        image2 = wx.Image(r'MathCloud.jpg', wx.BITMAP_TYPE_JPEG)
        portion = 0.75
        w = image2.GetWidth() * portion
        h = image2.GetHeight() * portion
        image2.Rescale(w, h)
        mypic2 = image2.ConvertToBitmap()
        wx.StaticBitmap(mypanel, -1, bitmap=mypic2, pos=(445, 2))
        custom2 = wx.StaticText(mypanel, -1, label='数学词云统计图', pos=(490, 500))
        custom2.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        custom2.SetForegroundColour((0, 0, 0))

        image3 = wx.Image(r'EnglishCloud.jpg', wx.BITMAP_TYPE_JPEG)
        portion = 0.75
        w = image3.GetWidth() * portion
        h = image3.GetHeight() * portion
        image3.Rescale(w, h)
        mypic3 = image3.ConvertToBitmap()
        wx.StaticBitmap(mypanel, -1, bitmap=mypic3, pos=(775, 2))
        custom3 = wx.StaticText(mypanel, -1, label='英语词云统计图', pos=(920, 500))
        custom3.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        custom3.SetForegroundColour((0, 0, 0))

if __name__ == '__main__':
    loadframe()