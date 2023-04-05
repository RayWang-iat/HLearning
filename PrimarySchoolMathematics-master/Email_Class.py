import smtplib
from email.mime.text import MIMEText
from email.header import Header
import wx

class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title,size=(600, 400))
        self.icon = wx.Icon('hfut.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        panel1 = wx.Panel(self)
        #垂直盒子
        vbox = wx.BoxSizer(wx.VERTICAL)
        #水平盒子
        nmbox = wx.BoxSizer(wx.HORIZONTAL)
        #创建两个静态文本
        fn = wx.StaticText(panel1, -1, label="联系方式：")
        #创建两个输入框
        self.nm1 = wx.TextCtrl(panel1, -1,size = (200,20),style=wx.ALIGN_LEFT)
        self.Bind(wx.EVT_BUTTON,self.Onclick,self.nm1)
        #在垂直盒子里添加水平盒子
        vbox.Add(nmbox, 0, wx.ALL | wx.CENTER, 5)

        multiLabel = wx.StaticText(panel1, -1, "若您有任何意见和建议请您在下方输入并点击发送按钮，我们在收到后会第一时间回复您：")
        multiLabel.SetFont(wx.Font(-1, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(multiLabel, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(fn, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.nm1, 0, wx.ALL | wx.EXPAND, 5)

        tn=wx.StaticText(panel1, -1, "您要反馈的内容：")
        vbox.Add(tn, 0, wx.ALL | wx.EXPAND, 5)

        # 创建文本域
        self.multiText = wx.TextCtrl(panel1, -1,size=(200, 200), style=wx.TE_MULTILINE)  # 创建一个文本控件
        self.multiText.SetInsertionPoint(0)  # 设置插入点
        self.Bind(wx.EVT_BUTTON,self.Onclick,self.multiText)
        #  在垂直盒子里添加文本域
        vbox.Add(self.multiText, 1, wx.ALL | wx.EXPAND , 5)

        self.find_Button = wx.Button(panel1, label="确认发送")
        self.Bind(wx.EVT_BUTTON, self.Onclick, self.find_Button)
        vbox.Add(self.find_Button, 0, wx.ALL | wx.EXPAND)

        panel1.SetSizer(vbox)
        self.Show()

    def Onclick(self,event):
       txt1=self.nm1.GetValue()
       txt2=self.multiText.GetValue()
       txt="用户联系方式："+txt1+"\n"+"用户反馈内容："+txt2
       email = Email(txt)
       condition=email.sengemail()
       if condition==True:
           dlg = wx.MessageDialog(None, u"反馈发送成功！", u"提示", wx.OK | wx.ICON_INFORMATION)
           if dlg.ShowModal() == wx.ID_YES:
               self.Close(True)
           dlg.Destroy()
       else:
           dlg = wx.MessageDialog(None, u"反馈发送失败！请检查网络设置", u"提示", wx.OK | wx.ICON_QUESTION)
           if dlg.ShowModal() == wx.ID_YES:
               self.Close(True)
           dlg.Destroy()

class Email:
    def __init__(self,txt):
        self.txt=txt

    def sengemail(self):
        from_addr = 'hggt89728@163.com'#不可改动
        password = 'AGPXCBXUVIIZMDER'  #不可改动

        to_addr = '3451707815@qq.com'  #可修改，发送到的目标邮箱

        smtp_server = 'smtp.163.com'

        msg = MIMEText(self.txt, 'plain', 'utf-8')

        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('HLearning') #邮件标题

        try:
            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server, 465)
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
            server.quit()
            print('Email Success')
            return True
        except BaseException:
            print('Email Error!')
            return False


class Email_APP(wx.App):
    def OnInit(self):
        self.frame = Mywin(None,  '意见反馈')
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = Email_APP(0)
    app.MainLoop()
