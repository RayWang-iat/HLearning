'''
这是语文试题的上层界面文件，在这个文件中我们完成人机交互
'''

import wx
import os
import shutil
from Chinese import Chinese
from Chinese import PrintPreview
from Chinese import Chinese_sentence
from Chinese import Chinese_article
from Chinese import Chinese_Choose


class MyFrame_ch(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.icon = wx.Icon('hfut.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.SetBackgroundColour((255, 255, 255))
        self.Q_title = "小学四年级语文试卷"
        self.grade = '四年级'
        list_q = []
        self.ratio_choose = wx.Slider(self, value=6, minValue=1, maxValue=10, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.ratio_text = wx.StaticText(self, label='当前难度系数为：', style=wx.ALIGN_RIGHT)
        self.ratio_text_2 = wx.StaticText(self, label='0.6', style=wx.ALIGN_RIGHT)
        self.ratio_choose.Bind(wx.EVT_SLIDER, self.ratio)
        self.grade_choice_1 = wx.RadioButton(self, 1, '一年级', style=wx.RB_GROUP)
        self.grade_choice_2 = wx.RadioButton(self, 2, '二年级')
        self.grade_choice_3 = wx.RadioButton(self, 3, '三年级')
        self.grade_choice_4 = wx.RadioButton(self, 4, '四年级')
        self.grade_choice_5 = wx.RadioButton(self, 5, '五年级')
        self.grade_choice_6 = wx.RadioButton(self, 6, '六年级')
        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=1, id2=2)
        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=3, id2=4)
        self.Bind(wx.EVT_RADIOBUTTON, self.grade_choose, id=5, id2=6)
        self.zuowenti = ""
        self.savepath = os.path.dirname(os.path.abspath(__file__))
        self.choice = 0
        self.article_choice = 1
        self.num_of_choose = "5"
        self.num_of_sentence = "5"
        self.num_q_everypaper = "10"
        self.num_paper_all = "5"
        self.Q_title_fu = "姓名：__________ 日期：____月____日 时间：________ 得分：____分"
        self.app_title = "HLearning小学语文试题生成器"
        self.choose = wx.TextCtrl(self, wx.ID_ANY, u"5", style=wx.TE_CENTER, size=(270, 30))
        self.choice_leixing = wx.RadioBox(self, wx.ID_ANY, u"古诗词题目类型选择",
                                          choices=[u"随机", u"写诗名", u"写作者", u"写前句", u"写后句"],
                                          majorDimension=1, style=wx.RA_SPECIFY_ROWS, size=(500, 60))
        self.Num_of_q = wx.TextCtrl(self, wx.ID_ANY, u"10", style=wx.TE_CENTER, size=(270, 30))
        self.ButtonAdd = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.ButtonChoose = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.Buttonsentence = wx.Button(self, wx.ID_ANY, u"恢复默认")
        self.set_article = wx.TextCtrl(self, wx.ID_ANY, u"", style=wx.TE_CENTRE)
        self.question_sentence = wx.TextCtrl(self, wx.ID_ANY, u"5", style=wx.TE_CENTRE)
        self.choice_article = wx.RadioBox(self, wx.ID_ANY, u"作文选择",
                                          choices=[u"不设置作文", u"随机设置作文题", u"手动设置作文"],
                                          majorDimension=1, style=wx.RA_SPECIFY_ROWS, size=(500, 60))
        # self.title_article = wx.TextCtrl(self,wx.ID_ANY,u"")
        self.Num_of_testPaper = wx.TextCtrl(self, wx.ID_ANY, "5", style=wx.TE_CENTER, size=(280, 30))
        self.ButtonChangeConcent = wx.Button(self, wx.ID_ANY, u"设置试题保存路径")
        self.title_main = wx.TextCtrl(self, wx.ID_ANY, u"小学语文练习题", style=wx.TE_CENTER, size=(130, 30))
        self.title_second = wx.TextCtrl(self, wx.ID_ANY, u"姓名：__________ 日期：____月____日 时间：________ 得分：____分",
                                        size=(240, 30))
        self.saveTestPaper = wx.Button(self, wx.ID_ANY, u"点击生成语文试卷")

        self.set_inital()
        self.layout_Chinese()

        self.choice_leixing.Bind(wx.EVT_RADIOBOX, self.choice_timuleixing)
        self.choice_article.Bind(wx.EVT_RADIOBOX, self.choice_zuowenti)
        self.ButtonAdd.Bind(wx.EVT_BUTTON, self.Remove_timushu)
        # self.BUttonRemove.Bind(wx.EVT_BUTTON,self.Remove_timushu)
        self.ButtonChangeConcent.Bind(wx.EVT_BUTTON, self.save_PSM_dir)
        self.saveTestPaper.Bind(wx.EVT_BUTTON, self.save)
        self.ButtonChoose.Bind(wx.EVT_BUTTON, self.back_choose_num)
        self.Buttonsentence.Bind(wx.EVT_BUTTON, self.back_sentence_num)

        self.choose.Bind(wx.EVT_TEXT, self.save_choose)
        self.set_article.Bind(wx.EVT_TEXT, self.save_zuowenti)
        self.Num_of_q.Bind(wx.EVT_TEXT, self.save_timushu)
        self.question_sentence.Bind(wx.EVT_TEXT, self.save_sentence)
        self.title_main.Bind(wx.EVT_TEXT, self.save_titel1)
        self.title_second.Bind(wx.EVT_TEXT, self.save_title2)
        self.Num_of_testPaper.Bind(wx.EVT_TEXT, self.save_juanzishu)

    def set_inital(self):
        self.SetTitle(self.app_title)
        self.grade_choice_4.SetValue(True)
        self.SetSize(500, 600)
        self.Num_of_q.SetValue(self.num_q_everypaper)
        self.choice_leixing.SetSelection(self.choice)
        self.choice_article.SetSelection(self.article_choice)
        self.Num_of_testPaper.SetValue(self.num_paper_all)
        self.choose.SetValue(self.num_of_choose)
        self.title_main.SetValue(self.Q_title)
        self.title_second.SetValue(self.Q_title_fu)

    def layout_Chinese(self):

        Box_Main = wx.BoxSizer(wx.VERTICAL)
        box_ratio = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"难度系数选择"), wx.HORIZONTAL)
        box_ratio.Add(self.ratio_choose, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP)
        box_ratio.Add(self.ratio_text, 0, wx.ALL)
        box_ratio.Add(self.ratio_text_2, 0, wx.ALL)
        Box_Main.Add(box_ratio, 0, wx.ALL | wx.EXPAND, 1)

        box_grade = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"年级选择"), wx.HORIZONTAL)
        box_grade.Add(self.grade_choice_1, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_2, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_3, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_4, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_5, 1, wx.ALL | wx.FIXED_MINSIZE)
        box_grade.Add(self.grade_choice_6, 1, wx.ALL | wx.FIXED_MINSIZE)
        Box_Main.Add(box_grade, 0, wx.ALL | wx.EXPAND, 1)
        Box_choose = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"添加选择题"), wx.HORIZONTAL)
        label_choose = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷选择题题量")
        Box_choose.Add(label_choose, 0, 0, 0)
        Box_choose.Add(self.choose, 1, wx.ALL | wx.EXPAND, 0)
        Box_choose.Add(self.ButtonChoose, 0, 0, 0)
        Box_Main.Add(Box_choose)
        Box_leixing = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY), wx.HORIZONTAL)
        Box_leixing.Add(self.choice_leixing, 0, 0, 0)
        Box_Main.Add(Box_leixing, 0, wx.ALL | wx.EXPAND, 1)
        Box_Add_q = wx.BoxSizer(wx.HORIZONTAL)
        label_box_add = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷古诗词题量")
        Box_Add_q.Add(label_box_add, 0, 0, 0)
        Box_Add_q.Add(self.Num_of_q, 0, 0, 0)
        Box_Add_q_Button = wx.BoxSizer(wx.HORIZONTAL)
        Box_Add_q_Button.Add(self.ButtonAdd, 0, wx.ALL | wx.EXPAND, 0)
        # Box_Add_q_Button.Add(self.BUttonRemove,0, wx.ALL | wx.EXPAND, 0)
        Box_Add_q.Add(Box_Add_q_Button, 1, wx.EXPAND, 0)
        Box_Add_q_main = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"添加古诗词到试卷中"), wx.VERTICAL)
        Box_Add_q_main.Add(Box_Add_q, 0, 0, 0)
        Box_Main.Add(Box_Add_q_main, 0, wx.ALL | wx.EXPAND, 1)
        Box_Add_end = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"添加句型变换到试卷中"), wx.HORIZONTAL)
        label_sentence = wx.StaticText(self, wx.ID_ANY, u"设置每张试卷中句型变换题量")
        Box_Add_end.Add(label_sentence, 0, 0, 0)
        Box_Add_end.Add(self.question_sentence, 1, wx.ALL | wx.EXPAND, 0)
        Box_Add_end.Add(self.Buttonsentence, 0, 0, 0)
        Box_Main.Add(Box_Add_end, 1, wx.ALL | wx.EXPAND, 1)
        Box_article = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY), wx.HORIZONTAL)
        Box_article.Add(self.choice_article, 0, 0, 0)
        Box_Main.Add(Box_article, 0, wx.ALL | wx.EXPAND, 1)
        Box_Add_article = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"请输入您需要添加的作文题"), wx.HORIZONTAL)
        Box_Add_article.Add(self.set_article, 1, wx.ALL | wx.EXPAND, 0)
        Box_Main.Add(Box_Add_article, 0, wx.ALL | wx.EXPAND, 1)
        Box_set_papernum = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"试卷设置"), wx.HORIZONTAL)
        label_papernum = wx.StaticText(self, wx.ID_ANY, u"生成试卷的数量")
        Box_set_papernum.Add(label_papernum, 0, 0, 0)
        Box_set_papernum.Add(self.Num_of_testPaper, 0, wx.LEFT, 8)
        Box_set_papernum.Add(self.ButtonChangeConcent)
        Box_Main.Add(Box_set_papernum, 0, wx.ALL | wx.EXPAND, 1)
        Box_set_paper = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"试卷标题设置"), wx.HORIZONTAL)
        title_main_text = wx.StaticText(self, wx.ID_ANY, u"试卷大标题：")
        Box_set_paper.Add(title_main_text, 0, 0, 0)
        Box_set_paper.Add(self.title_main, 0, 0, 0)
        title_second_text = wx.StaticText(self, wx.ID_ANY, u"试卷小标题：")
        Box_set_paper.Add(title_second_text, 0, 0, 0)
        Box_set_paper.Add(self.title_second, 1, wx.ALL, 0)
        Box_Main.Add(Box_set_paper)
        Box_Main.Add(self.saveTestPaper, 0, wx.ALL | wx.EXPAND, 1)
        self.SetSizer(Box_Main)
        Box_Main.Fit(self)
        self.Layout()

    def ratio(self, e):
        ratio = e.GetEventObject()
        val = ratio.GetValue()
        r = float(val) / 10
        ratio = str(r)
        self.ratio_text_2.SetLabel(ratio)

    def grade_choose(self, e):
        choice = e.GetEventObject()
        self.grade = choice.GetLabel()
        s = '小学' + self.grade + '语文试卷'
        self.Q_title = s
        self.title_main.SetValue(s)

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

    def back_sentence_num(self, e):
        self.num_of_sentence = "5"
        self.question_sentence.SetValue(self.num_of_sentence)

    def back_choose_num(self, e):
        self.num_of_choose = "5"
        self.choose.SetValue(self.num_of_choose)

    def save_timushu(self, e):
        self.num_q_everypaper = str(self.Num_of_q.GetValue())

    def save_sentence(self, e):
        self.num_of_sentence = str(self.question_sentence.GetValue())

    # def Add_Timushu(self,e):
    #     self.Add_to_test.SetValue("成功创建诗词古诗词填空题" + self.num_q_everypaper + "道!")
    def save_choose(self, e):
        self.num_of_choose = str(self.choose.GetValue())

    def Remove_timushu(self, e):
        self.num_q_everypaper = "10"
        self.Num_of_q.SetValue(self.num_q_everypaper)

    def choice_timuleixing(self, e):
        rb = e.GetEventObject()
        self.choice = rb.GetSelection()

    def choice_zuowenti(self, e):
        rb = e.GetEventObject()
        self.article_choice = rb.GetSelection()

    def save_juanzishu(self, e):
        self.num_paper_all = str(self.Num_of_testPaper.GetValue())

    def save_zuowenti(self, e):
        self.zuowenti = str(self.set_article.GetValue())

    def save_titel1(self, e):
        self.Q_title = str(self.title_main.GetValue())

    def save_title2(self, e):
        self.Q_title_fu = str(self.title_second.GetValue())

    def save_PSM_dir(self, e):
        '''设置口算卷子保存目录
        '''
        dlg = wx.DirDialog(self, message="选择文件夹")
        if dlg.ShowModal() == wx.ID_OK:
            # print(dlg.GetPath())
            # self.config.saveDocx(dlg.GetPath())
            self.savepath = dlg.GetPath()
            wx.MessageBox('设置文件保存目录为：' + self.savepath + os.sep, '成功提示', wx.OK | wx.ICON_INFORMATION)

    def save(self, e):
        # if self.Add_to_test.GetValue() == "":
        #     # print('还没有添加口算题到列表中哈！')  # 打印测试
        #     wx.MessageBox('还没有添加口算题到列表中哈！', '提示',wx.OK | wx.ICON_INFORMATION)
        #
        # else:
        ch = Chinese()
        ch_sentence = Chinese_sentence()
        ch_article = Chinese_article()
        ch_choose = Chinese_Choose()
        ch_sentence.load()
        ch_sentence.getQuestion(int(self.num_paper_all), int(self.num_of_sentence))
        ch_choose.load_choose()
        ch_choose.get_question_choose(int(self.num_paper_all), int(self.num_of_choose))
        if (self.article_choice == 0):
            for i in range(int(self.num_paper_all)):
                list_temp = []
                ch_article.list_question.append(list_temp)

        elif (self.article_choice == 1):
            ch_article.load_article()
            ch_article.get_question(int(self.num_paper_all))
        else:
            list_temp = []
            list_temp.append("作文")
            list_temp.append(self.zuowenti)
            list_temp.append("")
            for i in range(int(self.num_paper_all)):
                ch_article.list_question.append(list_temp)

        if (self.choice == 0):
            print(int(self.num_paper_all), int(self.num_q_everypaper))
            ch.Load_poem()
            ch.Model0(int(self.num_paper_all), int(self.num_q_everypaper))

        elif (self.choice == 1):
            ch.Load_poem()
            ch.Model1(int(self.num_paper_all), int(self.num_q_everypaper))
        elif (self.choice == 2):
            ch.Load_poem()
            ch.Model2(int(self.num_paper_all), int(self.num_q_everypaper))

        elif (self.choice == 3):
            ch.Load_poem()
            ch.Model3(int(self.num_paper_all), int(self.num_q_everypaper))

        else:
            ch.Load_poem()
            print(int(self.num_paper_all), int(self.num_q_everypaper))
            ch.Model4(int(self.num_paper_all), int(self.num_q_everypaper))
        pp = PrintPreview(ch_choose.list_question, ch_article.list_question, ch.list_q, ch_sentence.list_ques,
                          self.Q_title, self.Q_title_fu, docxpath=os.path.join(self.savepath, ""))
        pp.produce()
        wx.MessageBox('文件发布成功，保存在' + self.savepath + '目录下，请查看！！', '成功提示', wx.OK | wx.ICON_INFORMATION)


class MyApp_ch(wx.App):
    def OnInit(self):
        self.frame = MyFrame_ch(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


def main():
    app = MyApp_ch()
    app.MainLoop()


if __name__ == "__main__":
    main()

