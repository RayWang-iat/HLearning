import wx
import os
from APPconfig import AppConfig
from english import *

class MyWin(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.icon = wx.Icon('hfut.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.SetBackgroundColour((255, 255, 255))
        self.app_title = "HLearning小学英语试题生成器"
        self.title = '小学四年级英语试卷'
        self.title2 = '姓名：__________ 日期：____月____日 时间：________ 得分：____分'
        self.Words_Choice = 1
        self.number1 = '30'  # 单词检测
        self.number2 = '15'  # 选择填空
        self.number3 = '10'  # 连词成句
        self.number4 = '1'  # 英语作文
        self.dic = {'随机': 1, '单词拼写': 2, '中译英': 3, '英译中': 4, '不添加': 5}
        self.grade = '四年级'
        self.Choice_Stauts = 0  # 是否添加选择题
        self.config = AppConfig()
        self.paper_num = "3"
        self.q_words = "30"
        self.q_choices = "15"
        self.q_sentence = "10"
        self.q_writing = "1"
        self.choice_words = 1
        self.choice_choices = 1
        self.choice_sentence = 1
        self.choice_writing = 1
        self.ratio_choose = wx.Slider(self, value=6, minValue=1, maxValue=10, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.ratio_text = wx.StaticText(self, label='当前难度系数为：', style=wx.ALIGN_RIGHT)
        self.ratio_text_2 = wx.StaticText(self, label='0.6', style=wx.ALIGN_RIGHT)
        self.grade_choice_1 = wx.RadioButton(self, 1, '一年级', style=wx.RB_GROUP)
        self.grade_choice_2 = wx.RadioButton(self, 2, '二年级')
        self.grade_choice_3 = wx.RadioButton(self, 3, '三年级')
        self.grade_choice_4 = wx.RadioButton(self, 4, '四年级')
        self.grade_choice_5 = wx.RadioButton(self, 5, '五年级')
        self.grade_choice_6 = wx.RadioButton(self, 6, '六年级')
        self.lst=['随机','单词拼写','中译英','英译中','不添加']
        self.listbox_words = wx.ComboBox(self,wx.ID_ANY,value='单词拼写',choices=self.lst,style=wx.CB_SORT)
        self.listbox_txt = wx.StaticText(self,label=' 单词检测     ')
        self.checkbox_choices = wx.CheckBox(self, wx.ID_ANY, u"选择填空     ")
        self.checkbox_sentence = wx.CheckBox(self, wx.ID_ANY, u"连词成句     ")
        self.checkbox_writing = wx.CheckBox(self, wx.ID_ANY, u"英语作文     ")
        self.button_choose = wx.Button(self, wx.ID_ANY, "确认选择", size=(105, 30))
        self.textctrl_words = wx.TextCtrl(self, wx.ID_ANY, u"30", style=wx.TE_CENTRE, size=(249, 30))
        self.textctrl_choices = wx.TextCtrl(self, wx.ID_ANY, u"15", style=wx.TE_CENTRE, size=(249, 30))
        self.textctrl_sentence = wx.TextCtrl(self, wx.ID_ANY, u"10", style=wx.TE_CENTRE, size=(249, 30))
        self.textctrl_writing = wx.TextCtrl(self, wx.ID_ANY, u"1", style=wx.TE_CENTRE, size=(249, 30))
        self.button_words = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.button_choices = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.button_sentence = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.button_writing = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.Num_of_testPaper = wx.TextCtrl(self, wx.ID_ANY, "5", style=wx.TE_CENTER, size=(280, 30))
        self.ButtonChangeConcent = wx.Button(self, wx.ID_ANY, u"设置试题保存路径")
        self.title_main = wx.TextCtrl(self, wx.ID_ANY, u"小学英语试卷", style=wx.TE_CENTER, size=(130, 30))
        self.title_second = wx.TextCtrl(self, wx.ID_ANY, u"姓名：__________ 日期：____月____日 时间：________ 得分：____分",
                                        size=(240, 30))
        self.saveTestPaper = wx.Button(self, wx.ID_ANY, u"点击生成英语试卷")
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
        Box_main.Add(box_grade,0 ,wx.ALL | wx.EXPAND, 1)

        box_choose = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"题型选择"), wx.HORIZONTAL)
        box_choose.Add(self.listbox_words, 0, 0, 0)
        box_choose.Add(self.listbox_txt, 0, 0, 0)
        box_choose.Add(self.checkbox_choices, 0, 0, 0)
        box_choose.Add(self.checkbox_sentence, 0, 0, 0)
        box_choose.Add(self.checkbox_writing, 0, 0, 0)
        box_choose.Add(self.button_choose, 0, 0, 0)
        Box_main.Add(box_choose)

        box_words = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"单词检测设置"), wx.HORIZONTAL)
        label_words = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中单词检测的数量：")
        box_words.Add(label_words, 0, 0, 0)
        box_words.Add(self.textctrl_words, 1, wx.ALL | wx.EXPAND, 0)
        box_words.Add(self.button_words, 0, 0, 0)
        Box_main.Add(box_words, 0, 0, 0)

        box_choices = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"选择填空设置"), wx.HORIZONTAL)
        label_choices = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中选择填空的数量：")
        box_choices.Add(label_choices, 0, 0, 0)
        box_choices.Add(self.textctrl_choices, 1, wx.ALL | wx.EXPAND, 0)
        box_choices.Add(self.button_choices, 0, 0, 0)
        Box_main.Add(box_choices, 0, 0, 0)

        box_sentence = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"连词成句设置"), wx.HORIZONTAL)
        label_sentence = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中连词成句的数量：")
        box_sentence.Add(label_sentence, 0, 0, 0)
        box_sentence.Add(self.textctrl_sentence, 1, wx.ALL | wx.EXPAND, 0)
        box_sentence.Add(self.button_sentence, 0, 0, 0)
        Box_main.Add(box_sentence, 0, 0, 0)

        box_writing = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"英语作文设置"), wx.HORIZONTAL)
        label_writing = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中英语作文的数量：")
        box_writing.Add(label_writing, 0, 0, 0)
        box_writing.Add(self.textctrl_writing, 1, wx.ALL | wx.EXPAND, 0)
        box_writing.Add(self.button_writing, 0, 0, 0)
        Box_main.Add(box_writing, 0, 0, 0)

        Box_set_papernum = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"试卷设置"), wx.HORIZONTAL)
        label_papernum = wx.StaticText(self, wx.ID_ANY, u"生成试卷的数量：")
        Box_set_papernum.Add(label_papernum, 0, 0, 0)
        Box_set_papernum.Add(self.Num_of_testPaper, 0, wx.LEFT, 8)
        Box_set_papernum.Add(self.ButtonChangeConcent)
        Box_main.Add(Box_set_papernum, 0, wx.ALL | wx.EXPAND, 1)
        Box_set_paper = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"试卷标题设置"), wx.HORIZONTAL)
        title_main_text = wx.StaticText(self, wx.ID_ANY, u"试卷大标题：")
        Box_set_paper.Add(title_main_text, 0, 0, 0)
        Box_set_paper.Add(self.title_main, 0, 0, 0)
        title_second_text = wx.StaticText(self, wx.ID_ANY, u"试卷小标题：")
        Box_set_paper.Add(title_second_text, 0, 0, 0)
        Box_set_paper.Add(self.title_second, 1, wx.ALL, 0)
        Box_main.Add(Box_set_paper)
        Box_main.Add(self.saveTestPaper, 0, wx.ALL | wx.EXPAND, 1)
        self.SetSizer(Box_main)
        Box_main.Fit(self)
        self.Layout()

    def setinitial(self):
        self.SetTitle(self.app_title)
        self.SetSize(500, 600)

        self.grade_choice_4.SetValue(True)

        # 标题和试卷数设置
        self.Num_of_testPaper.SetValue(self.paper_num)
        self.title_main.SetValue(self.title)
        self.title_second.SetValue(self.title2)

        # 每张试卷题目初始化
        self.textctrl_words.SetValue(self.q_words)
        self.textctrl_choices.SetValue(self.q_choices)
        self.textctrl_sentence.SetValue(self.q_sentence)
        self.textctrl_writing.SetValue(self.q_writing)

        # 题型选择初始化
        self.checkbox_choices.SetValue(self.choice_choices)
        self.checkbox_sentence.SetValue(self.choice_sentence)
        self.checkbox_writing.SetValue(self.choice_writing)

    def bind(self):
        self.ratio_choose.Bind(wx.EVT_SLIDER, self.ratio)

        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=1, id2=2)
        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=3, id2=4)
        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=5, id2=6)

        self.button_choose.Bind(wx.EVT_BUTTON, self.save_choice_button)

        self.textctrl_words.Bind(wx.EVT_TEXT, self.save_textctrl_words)
        self.textctrl_choices.Bind(wx.EVT_TEXT, self.save_textctrl_choices)
        self.textctrl_sentence.Bind(wx.EVT_TEXT, self.save_textctrl_sentence)
        self.textctrl_writing.Bind(wx.EVT_TEXT, self.save_textctrl_writing)

        self.button_words.Bind(wx.EVT_BUTTON, self.recover_words)
        self.button_choices.Bind(wx.EVT_BUTTON, self.recover_choices)
        self.button_sentence.Bind(wx.EVT_BUTTON, self.recover_sentence)
        self.button_writing.Bind(wx.EVT_BUTTON, self.recover_writing)

        self.Num_of_testPaper.Bind(wx.EVT_TEXT, self.save_num_paper)
        self.title_main.Bind(wx.EVT_TEXT, self.save_main_title)
        self.title_second.Bind(wx.EVT_TEXT, self.save_fu_title)
        self.saveTestPaper.Bind(wx.EVT_BUTTON, self.save)
        self.ButtonChangeConcent.Bind(wx.EVT_BUTTON, self.save_PSM_dir)

    def ratio(self, e):
        ratio = e.GetEventObject()
        val = ratio.GetValue()
        r = float(val) / 10
        ratio = str(r)
        self.ratio_text_2.SetLabel(ratio)

    def grade_choose(self,e):
        choice = e.GetEventObject()
        self.grade = choice.GetLabel()
        s = '小学'+self.grade+'英语试卷'
        self.title = s
        self.title_main.SetValue(s)

    def save_choice(self, e1, e2, e3, e4):
        self.choice_words=self.dic[e1.GetValue()]
        self.choice_choices = e2.GetValue()
        self.choice_sentence = e3.GetValue()
        self.choice_writing = e4.GetValue()

    def save_choice_button(self,e):
        self.save_choice(self.listbox_words,self.checkbox_choices,self.checkbox_sentence,self.checkbox_writing)
        print(self.choice_writing)
        dlg = wx.MessageDialog(None, u"题型设置成功", u"提示", wx.OK | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg.Destroy()

    def save_textctrl_words(self,e):
        self.q_words = str(self.textctrl_words.GetValue())

    def save_textctrl_choices(self,e):
        self.q_choices = str(self.textctrl_choices.GetValue())

    def save_textctrl_sentence(self,e):
        self.q_sentence = str(self.textctrl_sentence.GetValue())

    def save_textctrl_writing(self,e):
        self.q_writing = str(self.textctrl_writing.GetValue())

    def save_main_title(self,e):
        self.title = str(self.title_main.GetValue())

    def save_fu_title(self,e):
        self.title2 = str(self.title_second.GetValue())

    def save_num_paper(self,e):
        self.paper_num = str(self.Num_of_testPaper.GetValue())

    def recover_words(self,e):
        self.q_words = "30"
        self.textctrl_words.SetValue(self.q_words)

    def recover_choices(self,e):
        self.q_choices = "15"
        self.textctrl_choices.SetValue(self.q_choices)

    def recover_sentence(self,e):
        self.q_sentence = "10"
        self.textctrl_sentence.SetValue(self.q_sentence)

    def recover_writing(self,e):
        self.q_writing = "10"
        self.textctrl_writing.SetValue(self.q_writing)

    def save_PSM_dir(self, e):
        '''设置口算卷子保存目录
        '''
        dlg = wx.DirDialog(self, message="选择文件夹")
        if dlg.ShowModal() == wx.ID_OK:
            # self.savepath=os.path.dirname(os.path.abspath(__file__))
            self.config.saveDocx(dlg.GetPath())
            print(self.config.c.get('config', 'docx') + os.sep)
            wx.MessageBox('设置文件保存目录为：' + self.config.c.get('config', 'docx') + os.sep, '成功提示',
                          wx.OK | wx.ICON_INFORMATION)

    def save(self,e):
        m1 = 1
        m2 = 1
        m3 = 1
        m4 = 1
        paper_num=eval(self.paper_num)
        if paper_num == 0:
            dlg = wx.MessageDialog(None, u"请选择正确的试卷数量", u"提示", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            print('Error')
        else:
            if self.choice_words==5:
                m1=0
            elif self.choice_choices==False:
                m2=0
            elif self.choice_sentence==False:
                m3=0
            elif self.choice_writing==False:
                m4=0
            i=0
            while i<paper_num:
                s = self.title + str(i + 1)
                s1 = self.title2
                number = eval(self.q_words)
                number2 = eval(self.q_choices)
                number3 = eval(self.q_sentence)
                number4 = eval(self.q_writing)
                if number == 0:
                    number = 30
                if number2 == 0:
                    number2 = 15
                if number3 == 0:
                    number3 = 10
                if number4 == 0:
                    number4 = 1
                spelling = 0
                intertranslation = 0
                is_English = 0
                is_Chnese = 0
                is_Mixed = 0
                c = []
                g = EnglishGenerate(spelling, intertranslation, is_English, is_Chnese, is_Mixed, number, number2,
                                    number3, number4)
                if self.choice_words==1:
                    l=g.Mixed()
                elif self.choice_words==2:
                    l=g.Spelling()
                elif self.choice_words==3:
                    l=g.Chinese_to_English()
                else:
                    l=g.English_to_Chinese()
                c.append(l)
                l2 = g.Choice_Question()
                l3 = g.Sentence_Question()
                l4 = g.Writing()
                t = [s]
                pp = PrintPreview(l=c, l2=l2, l3=l3, l4=l4, m1=m1, m2=m2, m3=m3, m4=m4, tit=t, col=3,
                                  subtitle=s1, docxpath=self.config.c.get('config', 'docx') + os.sep)
                pp.produce()
                i += 1
            dlg = wx.MessageDialog(None, u"试卷已生成在" + self.config.c.get('config', 'docx') + os.sep + u"目录下", u"提示",
                                   wx.OK | wx.ICON_INFORMATION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            print('Success')


class MyApp_English(wx.App):
    def OnInit(self):
        self.frame = MyWin(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


def main():
    app = MyApp_English()
    app.MainLoop()


if __name__ == "__main__":
    main()




