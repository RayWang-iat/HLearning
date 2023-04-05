'''
这是Math的上层界面类，从来完成人机交互
'''

import wx
import os
from Math import Math_xz
from Math import Math_tk
from Math import Math_ss
from Math import Math_pd
from Math import Math_yy
from Math import PrintPreview
import shutil


class My_Frame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.icon = wx.Icon('hfut.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.SetBackgroundColour((255, 255, 255))
        self.app_title = "Python自动生成数学试题"
        self.savepath = os.path.dirname(os.path.abspath(__file__))
        self.main_title = "小学数学试题"
        self.fu_title = "姓名：__________ 日期：____月____日 时间：________ 对题：____道"
        # 初始化的数字
        self.paper_num = "5"
        self.q_xz = "5"
        self.q_tk = "5"
        self.q_pd = "5"
        self.q_ss = "10"
        self.q_yy = "5"

        self.grade = '四年级'

        self.choice_xz = 1      #
        self.choice_tk = 1
        self.choice_pd = 1
        self.choice_ss = 1
        self.choice_yy = 1

        self.ratio_choose = wx.Slider(self, value=6, minValue=1, maxValue=10, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.ratio_text = wx.StaticText(self, label='当前难度系数为：', style=wx.ALIGN_RIGHT)
        self.ratio_text_2 = wx.StaticText(self, label='0.6', style=wx.ALIGN_RIGHT)

        self.grade_choice_1 = wx.RadioButton(self, 1, '一年级', style=wx.RB_GROUP)
        self.grade_choice_2 = wx.RadioButton(self, 2, '二年级')
        self.grade_choice_3 = wx.RadioButton(self, 3, '三年级')
        self.grade_choice_4 = wx.RadioButton(self, 4, '四年级')
        self.grade_choice_5 = wx.RadioButton(self, 5, '五年级')
        self.grade_choice_6 = wx.RadioButton(self, 6, '六年级')

        self.checkbox_xz = wx.CheckBox(self,wx.ID_ANY,u"选择题     ")
        self.checkbox_tk = wx.CheckBox(self,wx.ID_ANY,u"填空题     ")
        self.checkbox_pd = wx.CheckBox(self,wx.ID_ANY,u"判断题     ")
        self.checkbox_ss = wx.CheckBox(self,wx.ID_ANY,u"算术题     ")
        self.checkbox_yy = wx.CheckBox(self,wx.ID_ANY,u"应用题     ")
        self.button_choose = wx.Button(self,wx.ID_ANY,"确认选择",size = (105,30))

        self.textctrl_xz = wx.TextCtrl(self,wx.ID_ANY,u"5",style = wx.TE_CENTRE,size = (249,30))
        self.textctrl_tk = wx.TextCtrl(self,wx.ID_ANY,u"5",style = wx.TE_CENTRE,size = (249,30))
        self.textctrl_pd = wx.TextCtrl(self, wx.ID_ANY, u"5", style=wx.TE_CENTRE,size = (249,30))
        self.textctrl_ss = wx.TextCtrl(self, wx.ID_ANY, u"10", style=wx.TE_CENTRE,size = (249,30))
        self.textctrl_yy = wx.TextCtrl(self, wx.ID_ANY, u"5", style=wx.TE_CENTRE, size=(249, 30))

        self.button_xz = wx.Button(self,wx.ID_ANY,u"恢复默认")
        self.button_tk = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.button_pd = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.button_ss = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.button_yy = wx.Button(self, wx.ID_ANY, u"恢复默认")

        self.Num_of_testPaper = wx.TextCtrl(self,wx.ID_ANY,"5",style=wx.TE_CENTER,size=(280,30))
        self.ButtonChangeConcent = wx.Button(self,wx.ID_ANY,u"设置试题保存路径")
        self.title_main = wx.TextCtrl(self,wx.ID_ANY,u"小学数学试卷",style = wx.TE_CENTER,size=(130,30))
        self.title_second = wx.TextCtrl(self,wx.ID_ANY,u"姓名：__________ 日期：____月____日 时间：________ 对题：____道",size=(240,30))
        self.saveTestPaper = wx.Button(self,wx.ID_ANY,u"点击生成练习题打印文件")
        self.setinitial()
        self.bind()
        self.layout()

    def layout(self):
        Box_main = wx.BoxSizer(wx.VERTICAL)
        box_ratio = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"难度系数选择"), wx.HORIZONTAL)
        box_ratio.Add(self.ratio_choose, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP)
        box_ratio.Add(self.ratio_text, 0, wx.ALL)
        box_ratio.Add(self.ratio_text_2, 0, wx.ALL)
        Box_main.Add(box_ratio, 0, wx.ALL | wx.EXPAND, 1)

        box_grade = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"年级选择"), wx.HORIZONTAL)
        box_grade.Add(self.grade_choice_1, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_2, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_3, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_4, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_5, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_6, 1, wx.ALL | wx.FIXED_MINSIZE)
        Box_main.Add(box_grade, 0, wx.ALL | wx.EXPAND, 1)

        box_choose = wx.StaticBoxSizer(wx.StaticBox(self,wx.ID_ANY,u"题型选择"),wx.HORIZONTAL)
        box_choose.Add(self.checkbox_xz,0,0,0)
        box_choose.Add(self.checkbox_tk,0,0,0)
        box_choose.Add(self.checkbox_pd,0,0,0)
        box_choose.Add(self.checkbox_ss,0,0,0)
        box_choose.Add(self.checkbox_yy,0,0,0)
        box_choose.Add(self.button_choose,0,0,0)
        Box_main.Add(box_choose)

        # Box_Add_end = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"添加句子有关题目到卷子中"), wx.HORIZONTAL)
        # label_sentence = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中句子题目量")
        # Box_Add_end.Add(label_sentence, 0, 0, 0)
        # Box_Add_end.Add(self.question_sentence, 1, wx.ALL | wx.EXPAND, 0)
        # Box_Add_end.Add(self.Buttonsentence, 0, 0, 0)
        # Box_Main.Add(Box_Add_end, 1, wx.ALL | wx.EXPAND, 1)
        box_xz = wx.StaticBoxSizer(wx.StaticBox(self,wx.ID_ANY,u"选择题设置"),wx.HORIZONTAL)
        label_xz = wx.StaticText(self,wx.ID_ANY,u"设置每张试卷中选择题的数量：")
        box_xz.Add(label_xz,0,0,0)
        box_xz.Add(self.textctrl_xz,1,wx.ALL | wx.EXPAND,0)
        box_xz.Add(self.button_xz,0,0,0)
        Box_main.Add(box_xz,0,0,0)

        box_tk = wx.StaticBoxSizer(wx.StaticBox(self,wx.ID_ANY,u"填空题设置"),wx.HORIZONTAL)
        label_tk = wx.StaticText(self,wx.ID_ANY,u"设置每张试卷中填空题的数量：")
        box_tk.Add(label_tk,0,0,0)
        box_tk.Add(self.textctrl_tk,1,wx.ALL | wx.EXPAND,0)
        box_tk.Add(self.button_tk,0,0,0)
        Box_main.Add(box_tk,0,0,0)

        box_pd = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"判断题设置"), wx.HORIZONTAL)
        label_pd = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中判断题的数量：")
        box_pd.Add(label_pd, 0, 0, 0)
        box_pd.Add(self.textctrl_pd, 1, wx.ALL | wx.EXPAND, 0)
        box_pd.Add(self.button_pd, 0, 0, 0)
        Box_main.Add(box_pd, 0, 0, 0)

        box_ss = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"算术题设置"), wx.HORIZONTAL)
        label_ss = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中算术题的数量：")
        box_ss.Add(label_ss, 0, 0, 0)
        box_ss.Add(self.textctrl_ss, 1, wx.ALL | wx.EXPAND, 0)
        box_ss.Add(self.button_ss, 0, 0, 0)
        Box_main.Add(box_ss, 0, 0, 0)

        box_yy = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"应用题设置"), wx.HORIZONTAL)
        label_yy = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中应用题的数量：")
        box_yy.Add(label_yy, 0, 0, 0)
        box_yy.Add(self.textctrl_yy, 1, wx.ALL | wx.EXPAND, 0)
        box_yy.Add(self.button_yy, 0, 0, 0)
        Box_main.Add(box_yy, 0, 0, 0)

        Box_set_papernum = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"卷子设置"), wx.HORIZONTAL)
        label_papernum = wx.StaticText(self, wx.ID_ANY, u"生成试卷的数量：")
        Box_set_papernum.Add(label_papernum, 0, 0, 0)
        Box_set_papernum.Add(self.Num_of_testPaper, 0, wx.LEFT, 8)
        Box_set_papernum.Add(self.ButtonChangeConcent)
        Box_main.Add(Box_set_papernum, 0, wx.ALL | wx.EXPAND, 1)
        Box_set_paper = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"卷子大标题小标题设置"), wx.HORIZONTAL)
        title_main_text = wx.StaticText(self, wx.ID_ANY, u"卷子标题：")
        Box_set_paper.Add(title_main_text, 0, 0, 0)
        Box_set_paper.Add(self.title_main, 0, 0, 0)
        title_second_text = wx.StaticText(self, wx.ID_ANY, u"卷子副标题：")
        Box_set_paper.Add(title_second_text, 0, 0, 0)
        Box_set_paper.Add(self.title_second, 1, wx.ALL, 0)
        Box_main.Add(Box_set_paper)
        Box_main.Add(self.saveTestPaper, 0, wx.ALL | wx.EXPAND, 1)
        self.SetSizer(Box_main)
        Box_main.Fit(self)
        self.Layout()

    def setinitial(self):
        self.SetTitle(self.app_title)
        self.SetSize(500,600)

        self.grade_choice_4.SetValue(True)

        # 标题和试卷数设置
        self.Num_of_testPaper.SetValue(self.paper_num)
        self.title_main.SetValue(self.main_title)
        self.title_second.SetValue(self.fu_title)

        # 每张试卷题目初始化
        self.textctrl_xz.SetValue(self.q_xz)
        self.textctrl_tk.SetValue(self.q_tk)
        self.textctrl_pd.SetValue(self.q_pd)
        self.textctrl_ss.SetValue(self.q_ss)
        self.textctrl_yy.SetValue(self.q_yy)

        # 题型选择初始化
        self.checkbox_xz.SetValue(self.choice_xz)
        self.checkbox_tk.SetValue(self.choice_tk)
        self.checkbox_pd.SetValue(self.choice_pd)
        self.checkbox_ss.SetValue(self.choice_ss)
        self.checkbox_yy.SetValue(self.choice_yy)

    def bind(self):
        self.ratio_choose.Bind(wx.EVT_SLIDER, self.ratio)

        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=1, id2=2)
        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=3, id2=4)
        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=5, id2=6)
        self.button_choose.Bind(wx.EVT_BUTTON,self.save_choice_button)
        # self.checkbox_xz.Bind(wx.EVT_CHECKBOX,self.)
        self.textctrl_xz.Bind(wx.EVT_TEXT,self.save_textctrl_xz)
        self.textctrl_tk.Bind(wx.EVT_TEXT,self.save_textctrl_tk)
        self.textctrl_pd.Bind(wx.EVT_TEXT,self.save_textctrl_pd)
        self.textctrl_ss.Bind(wx.EVT_TEXT,self.save_textctrl_ss)
        self.textctrl_yy.Bind(wx.EVT_TEXT,self.save_textctrl_yy)

        self.button_xz.Bind(wx.EVT_BUTTON,self.recover_xz)
        self.button_tk.Bind(wx.EVT_BUTTON,self.recover_tk)
        self.button_pd.Bind(wx.EVT_BUTTON,self.recover_pd)
        self.button_ss.Bind(wx.EVT_BUTTON,self.recover_ss)
        self.button_yy.Bind(wx.EVT_BUTTON,self.recover_yy)

        self.Num_of_testPaper.Bind(wx.EVT_TEXT,self.save_num_paper)
        self.title_main.Bind(wx.EVT_TEXT,self.save_main_title)
        self.title_second.Bind(wx.EVT_TEXT,self.save_fu_title)
        self.saveTestPaper.Bind(wx.EVT_BUTTON,self.save)
        self.ButtonChangeConcent.Bind(wx.EVT_BUTTON,self.save_PSM_dir)

    def ratio(self, e):
        ratio = e.GetEventObject()
        val = ratio.GetValue()
        r = float(val) / 10
        ratio = str(r)
        self.ratio_text_2.SetLabel(ratio)

    def grade_choose(self,e):
        choice = e.GetEventObject()
        self.grade = choice.GetLabel()
        s = '小学'+self.grade+'数学试卷'
        self.main_title = s
        self.title_main.SetValue(s)

    def save_choice(self,e1,e2,e3,e4,e5):
        self.choice_xz = e1.GetValue()
        self.choice_tk = e2.GetValue()
        self.choice_pd = e3.GetValue()
        self.choice_ss = e4.GetValue()
        self.choice_yy = e5.GetValue()

    def save_choice_button(self,e):
        self.save_choice(self.checkbox_xz,self.checkbox_tk,self.checkbox_pd,self.checkbox_ss,self.checkbox_yy)

    def save_textctrl_xz(self,e):
        self.q_xz = str(self.textctrl_xz.GetValue())

    def save_textctrl_tk(self,e):
        self.q_tk = str(self.textctrl_tk.GetValue())

    def save_textctrl_pd(self,e):
        self.q_pd = str(self.textctrl_pd.GetValue())

    def save_textctrl_ss(self,e):
        self.q_ss = str(self.textctrl_ss.GetValue())

    def save_textctrl_yy(self,e):
        self.q_yy = str(self.textctrl_yy.GetValue())

    def save_main_title(self,e):
        self.main_title = str(self.title_main.GetValue())

    def save_fu_title(self,e):
        self.fu_title = str(self.title_second.GetValue())

    def save_num_paper(self,e):
        self.paper_num = str(self.Num_of_testPaper.GetValue())

    def recover_xz(self,e):
        self.q_xz = "5"
        self.textctrl_xz.SetValue(self.q_xz)

    def recover_tk(self,e):
        self.q_tk = "5"
        self.textctrl_tk.SetValue(self.q_tk)

    def recover_pd(self,e):
        self.q_pd = "5"
        self.textctrl_pd.SetValue(self.q_pd)

    def recover_ss(self,e):
        self.q_ss = "10"
        self.textctrl_ss.SetValue(self.q_ss)

    def recover_yy(self,e):
        self.q_yy = "5"
        self.textctrl_yy.SetValue(self.q_yy)

    def save_PSM_dir(self, e):
        '''设置口算卷子保存目录
        '''
        dlg = wx.DirDialog(self, message="选择文件夹")
        if dlg.ShowModal() == wx.ID_OK:
            #print(dlg.GetPath())
            # self.config.saveDocx(dlg.GetPath())
            self.savepath = dlg.GetPath()
            wx.MessageBox('设置文件保存目录为：'+self.savepath+os.sep, '成功提示',wx.OK | wx.ICON_INFORMATION)

    def movdocx(self):
        '''负责把生成的口算题文件移动到指定目录
        默认把口算题移动到'项目/docx/'下，其他目录需要指定。

        '''
        docs = []  # 当前目录生成的文件列表

        for p in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            if p.endswith('.docx'):
                docs.append(p)
        # print(docs)
        # p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docx')
        p = os.path.join(self.savepath, 'docx')  # 最后保存目录设置，保存在当前目录下的docx目录下
        if os.path.isdir(p):
            shutil.rmtree(p)
            os.mkdir(p)
            for f in docs:
                shutil.move(f, p)
        else:
            os.mkdir(p)
            for f in docs:
                shutil.move(f, p)

    def save(self,e):
        xz = Math_xz()
        tk = Math_tk()
        pd = Math_pd()
        ss = Math_ss()
        yy = Math_yy()

        if(self.choice_xz == 1):
            xz.load()
            xz.get_q(int(self.q_xz), int(self.paper_num))
            xz.deal_q()
        else:
            temp = []
            for i in range(int(self.paper_num)):
                xz.list_q.append(temp)

        if(self.choice_tk == 1):
            tk.load_tk()
            tk.get_q(int(self.q_tk),int(self.paper_num))
        else:
            temp = []
            for i in range(int(self.paper_num)):
                tk.list_q.append(temp)

        if(self.choice_pd == 1):
            pd.load_pd()
            pd.get_q(int(self.q_pd),int(self.paper_num))
        else:
            temp = []
            for i in range(int(self.paper_num)):
                pd.list_q.append(temp)

        if(self.choice_ss == 1):
            ss.load_ss()
            ss.get_q(int(self.q_ss),int(self.paper_num))
        else:
            temp = []
            for i in range(int(self.paper_num)):
                ss.list_q.append(temp)

        if (self.choice_yy == 1):
            yy.load()
            yy.get_q(int(self.q_yy), int(self.paper_num))
        else:
            temp = []
            for i in range(int(self.paper_num)):
                yy.list_q.append(temp)

        pp = PrintPreview(xz.list_q,tk.list_q,pd.list_q,ss.list_q,yy.list_q,self.main_title, self.fu_title, docxpath=os.path.join(self.savepath, ""))
        pp.produce()
        wx.MessageBox('文件发布成功，保存在' + self.savepath + '目录下，请查看！！', '成功提示',wx.OK | wx.ICON_INFORMATION)


class MyApp_math(wx.App):
    def OnInit(self):
        self.frame = My_Frame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

def main():
    app = MyApp_math(0)
    app.MainLoop()

if __name__ == "__main__":
    main()