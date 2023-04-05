import wx
import os
import xlrd
import time
import random

class SiteLog(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='添加试题至数据库', size=(350, 120))
        self.icon = wx.Icon('hfut.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.flag=0
        self.SetBackgroundColour((255, 255, 255))
        self.Text = wx.StaticText(self,-1, "文件位置：",pos=(5,9))
        self.SelBtn = wx.Button(self, label='选择文件位置', pos=(85, 45), size=(80, 25))
        self.SelBtn.Bind(wx.EVT_BUTTON, self.OnOpenFile)
        self.OkBtn = wx.Button(self, label='确认添加', pos=(195, 45), size=(80, 25))
        self.OkBtn.Bind(wx.EVT_BUTTON, self.ReadFile)
        self.FileName = wx.TextCtrl(self, pos=(65, 5),size=(230, 25))
        #self.FileContent = wx.TextCtrl(self, pos=(5, 35), size=(620, 480), style=(wx.TE_MULTILINE))

    def OnOpenFile(self, event):
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None, 'select', os.getcwd(), '', wildcard, wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.FileName.SetValue(dialog.GetPath())
            dialog.Destroy
            self.flag = 1

    def ReadFile(self, event):
        if self.flag==1:
            progressMax = 100
            dialog = wx.ProgressDialog("题目上传中.....", "请稍等", progressMax,
                                       style= wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
            keepGoing = True
            count = 0
            num=random.randint(1,99)
            while keepGoing and count < progressMax:
                count = count + 1
                keepGoing = dialog.Update(count)
                if count==num:
                    time.sleep(2)
            dialog.Destroy()
        else:
            dlg = wx.MessageDialog(None, u"请选择文件", u"提示", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
                dlg.Destroy()

class SetQuestion(wx.App):
    def OnInit(self):
        self.SiteFrame = SiteLog()
        self.SiteFrame.Show()
        return True

if __name__ == '__main__':
    app = SetQuestion(0)
    app.MainLoop()