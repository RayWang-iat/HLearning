# coding:utf-8
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sys
import qtawesome
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from Appmath import MyApp_math
from App_Chinese import MyApp_ch
from App_English import MyApp_English
from Email_Class import Email_APP
from setqu import *
from AboutUs_Class import *
from MeetQuestion_Class import *
from Cloud_Class import *


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.setWindowIcon(QIcon('hfut.ico'))
        self.setWindowTitle('HLearning小学智慧试题生成系统')
        # self.app_title = 'HLearning小学智慧试题生成系统'
        self.left_label_1 = QtWidgets.QPushButton("试题选择")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("数据展示")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.globe', color='white'), "语文试题")
        self.left_button_1.clicked.connect(self.Chines_iems)
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.magic', color='white'), "数学试题")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(self.Math_iems)
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.bold', color='white'), "英语试题")
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.clicked.connect(self.English_iems)
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.cloud-upload', color='white'), "添加试题")
        self.left_button_4.clicked.connect(self.SetQuestion_items)
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "数据展示")
        self.left_button_5.clicked.connect(self._HTML)
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), "词云统计")
        self.left_button_6.clicked.connect(self.Cloud)
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_7.clicked.connect(self.Email_items)
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_8.clicked.connect(self.About)
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_9.setObjectName('left_button')
        self.left_button_9.clicked.connect(self.Meet)
        self.left_xxx = QtWidgets.QPushButton(" ")

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
        self.left_close.setFixedSize(20, 20)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(20, 20)  # 设置按钮大小
        self.left_mini.setFixedSize(20, 20)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        ''')
        ###########右侧部分处理############################
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:30px;
                font-weight:200;
                font-family:Tahoma,Helvetica,Arial,sans-serif;
            }
        ''')
        # font - family: "宋体"
        # font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        self.right_recommend_label2 = QtWidgets.QLabel()
        self.right_recommend_label2.setPixmap(QPixmap('hfut.ico'))
        self.right_recommend_label2.raise_()
        self.right_recommend_label = QtWidgets.QLabel("HLearning小学智慧试题生成系统")
        self.right_recommend_label.setObjectName('right_lable')
        self.right_recommend_label.setAlignment(Qt.AlignCenter)
        self.right_recommend_label.setFont(QFont("Roman times", 20, QFont.Bold))
        # self.right_recommend_label.setIcon(QtGui.QIcon('background.png'))
        self.right_recommend_widget = QtWidgets.QWidget()  # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("欢迎使用HLearning团队产品！")  # 设置按钮文本
        self.recommend_button_1.setIcon(QtGui.QIcon('background.png'))  # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(900, 900))  # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
        self.recommend_button_1.setStyleSheet(
            '''recommend_button_1{background:yellow;}''')

        # self.recommend_button_1.setIcon(QIcon('hfut.ico'))
        # self.recommend_button_1.setStyleSheet("QPushButton{border-image: url(background.png)}")
        self.right_recommend_layout.addWidget(self.recommend_button_1, 0, 0)

        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)

        ##################设置最后背景#############################
        self.setWindowOpacity(0.92)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.left_widget.setStyleSheet('''
                QWidget#left_widget{
    background:gray;
    border-top:1px solid white;
    border-bottom:1px solid white;
    border-left:1px solid white;
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
}
            ''')
        self.main_layout.setSpacing(0)

    def init_ui(self):
        self.setFixedSize(860, 650)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

    def Chines_iems(self, event):
        app = MyApp_ch(0)
        app.MainLoop()

    def Math_iems(self, event):
        app = MyApp_math(0)
        app.MainLoop()

    def English_iems(self, event):
        app = MyApp_English()
        app.MainLoop()

    def Email_items(self, event):
        app = Email_APP(0)
        app.MainLoop()

    def SetQuestion_items(self, event):
        app = SetQuestion(0)
        app.MainLoop()

    def join_us(self, event):
        # self.ui()
        self.right_recommend_label2 = QtWidgets.QLabel("我们的QQ公众号为:2707571796，里面会发布一些关于这个软件的有趣小故事。\n欢迎并期待您加入我们这个大家庭。")
        self.right_recommend_label2.setObjectName('right_lable')
        self.right_layout.addWidget(self.right_recommend_label1, 1, 0, 1, 9)

    def face_problem(self, event):
        # self.ui()
        self.right_recommend_label = QtWidgets.QLabel(
            "1.若您点击\"实时数据\"按钮，此时软件系统正在网上爬取信息，在短时间内点击系统无反馈属于正常现象。\n2.生成\"课程报告\"需要一定的时间，请耐心等待。\n3.data文件夹下储存有您的往期数据，您查看课程的变化趋势时与之密切相关。\n若您有其它问题，请及时通知我们，我们将第一时间为您解决。\n联系电话:\n小助手1:18856359800\n小助手2:18856301011\n小助手3:17356379709\n我们随时欢迎您来电咨询。")
        self.right_recommend_label.setObjectName('right_lable')
        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)

    def About(self, event):
        app = MyApp_Aboutus(0)
        app.MainLoop()

    def Meet(self, event):
        app = MyApp_MeetQuestion(0)
        app.MainLoop()

    def _HTML(self, event):
        url = 'Questions.html'
        webbrowser.open(url=url, new=0)

    def Cloud(self, event):
        loadframe()


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
