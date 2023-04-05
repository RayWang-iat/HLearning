#-*-coding:utf-8-*-
#获取路径
import sys,os
path=os.getcwd()
#python爬虫爬取网络信息
import requests,re
import lxml.html
import pandas as pd
import json
#numpy数据运算库
import numpy as np
#获取当前时间给当日数据文件命名
import datetime
from datetime import timezone
import time
#使用pyqt5搭建主图形界面
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore,QtGui,QtWidgets
import qtawesome
import sip
from PyQt5.QtGui import *
#使用tinter搭建辅图形界面
import tkinter as tk
from matplotlib import pyplot as plt
from pandas.api import types
from tkinter import Tk, Scrollbar, Frame,Button,messagebox
from tkinter.ttk import Treeview
#制作python词云 
from PIL import Image
import jieba
#因为封装成exe后，wordcloud包的路径容易读取出错，所以将其取出改写存入word文件夹下
from word import WordCloud
#对数据进行三次样条插值
from scipy.interpolate import interp1d
#新课程情况预测
import xgboost as xgb
from snownlp import SnowNLP
#若文件夹不小心删除，则重新建立
pathurl=path+'/report'
os.makedirs("./data", exist_ok=True)
os.makedirs("./category", exist_ok=True)
os.makedirs("./picture", exist_ok=True)
os.makedirs("./word", exist_ok=True)
os.makedirs("./prediction_model", exist_ok=True)
os.makedirs(pathurl, exist_ok=True)
#临时路径的选择
try:
    if hasattr(sys, '_MEIPASS'):
        self.appPath = os.path.dirname(os.path.realpath(sys.executable))
    else:
        self.appPath, filename = os.path.split(os.path.abspath( __file__))
except:
    pass
#python爬虫爬取网络信息并进行简单的预处理，将处理好的数据存入data文件夹，目录存入category文件夹
def sortcols(df):
    col_str = []
    col_num = []
    col_unc = [] 
    for column in df.columns:
        if types.is_string_dtype(df[column]):
            col_str.append(column)
        elif types.is_numeric_dtype(df[column]):
            col_num.append(column)
        else:
            col_unc.append(column)
    return(col_str, col_num, col_unc)
def data_capture():
    #root = tk.Tk()
    #root.destroy()
    #messagebox.showinfo(title="提示", message="点击确认开始爬取实时信息，数据收集完成后子窗口将会自动弹出，请稍候")
    QMessageBox.information(None, "提示", "正在网上爬取实时信息，数据收集完成会提醒您，请稍候！", QMessageBox.Yes)
    url_main = 'https://study.163.com'
    r = requests.get(url_main)
    html_text = r.content.decode()
    tree = lxml.html.fromstring(html_text)
    items1 = tree.cssselect('a.f-f0.first.cat2.tit.f-fl')
    list_category = []
    items = items1
    for idx,item in enumerate(items):
        try:
            # 栏目标题
            c_name = item.text_content()        
            # 父栏目
            c_parent = item.get('data-index')
            # 子栏目
            c_child = item.get('data-name')
            # 栏目编号
            c_url = item.get('href')       
            list_category.append([c_name,c_parent,c_child,c_url])
        except:
            pass
    items2 = tree.cssselect('p.cate3links > a.f-f0')
    items = items2  
    for idx,item in enumerate(items):
        try:
            # 栏目标题
            c_name = item.text_content()       
            # 父栏目
            c_parent = item.get('data-index')
            # 子栏目
            c_child = item.get('data-name')
            # 栏目编号
            c_url = item.get('href')       
            list_category.append([c_name,c_parent,c_child,c_url])
        except:
            pass
    data_category = pd.DataFrame(list_category, columns=['name','parent','child','url'])
    # 清洗数据
    # 去掉name列中的换行符
    data_category['name'] = data_category['name'].apply(lambda x:x.replace('\n',''))
    # 去掉parent列中的'_类目框'
    data_category['parent'] = data_category['parent'].apply(lambda x:x.replace('_类目框',''))
    # 新增一列栏目编号，cat_id
    data_category['cat_id'] = data_category['url'].apply(lambda x:x.split('/')[-1])
    # 补全url
    data_category['url'] = data_category['cat_id'].apply(lambda x:'https://study.163.com/category/'+x)
    # 检查数据是否有重复
    # 总行数==主键的去重计数
    data_category = data_category.drop_duplicates(subset=['cat_id'])
    data_category.loc[data_category['name']!=data_category['child']]
    del data_category['name']
    # 过滤掉非数字的cat_id
    data_category = data_category.loc[data_category['cat_id'].apply(str.isnumeric)]
    data_category.to_csv('./category/categorydata.csv')
    # 载入离线数据
    data_category = pd.read_csv('./category/categorydata.csv')
    headers_cat = {
    'Referer': 'https://study.163.com/category/480000003124027'
    ,'cookie':'NTESSTUDYSI=c2b373320c9e4bdcbaaf3e472e82f2d6; EDUWEBDEVICE=affc57a4b6aa408091a8f0c9752b08d9; utm=eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly9zdHVkeS4xNjMuY29tL2NhdGVnb3J5LzQ4MDAwMDAwMzEyNDAyNw==; __utma=129633230.1300737634.1560475613.1560475613.1560475613.1; __utmc=129633230; __utmz=129633230.1560475613.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=129633230.2.10.1560475613'
    ,'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'    
    }
    dt = datetime.datetime.now()
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    mark = 1
    # 第一层循环，cat_id
    for cat_id in data_category['cat_id']:   
        url_cat = 'https://study.163.com/j/web/fetchPersonalData.json?categoryId='+str(cat_id)   
        url_check = 'https://study.163.com/category/'+str(cat_id)
        # 更新refer中的url
        headers_cat['Referer'] = url_check    
        r_cat = requests.get(url_cat, headers=headers_cat)   
        try:
            html_text = r_cat.content.decode()
            html_json = json.loads(html_text)
            # 课程推荐的模块一般会有多个
            modules = html_json['result']        
            # 第2层循环，module
            for module in modules:
                # 每个模块下通常会有多门课程推荐
                courses = module['contentModuleVo'] #json格式           
                tmp_df = pd.DataFrame.from_dict(courses)           
                if mark == 1:
                    # 初始化dataframe
                    data_courses_raw1 = tmp_df
                    # 重置标记
                    mark = 0
                else:
                    data_courses_raw1 = pd.concat([data_courses_raw1,tmp_df], axis=0,)
        except:
            pass
    # 备份数据
    data_courses_bak1 = data_courses_raw1
    col_empty = []
    col_notemp = []
    # 总行数
    row_cnt,col_cnt = data_courses_raw1.shape
    for column in data_courses_raw1.columns:    
        # 注意isna和isnull的效果是一样的，不要重复计算
        rcnt_empty = sum(pd.isna(data_courses_raw1[column]))\
                    +sum(data_courses_raw1[column].apply(lambda x:str(x).replace(' ',''))=='')\
                    +sum(data_courses_raw1[column].apply(lambda x:str(x).upper())=='NULL')    
        if rcnt_empty >= row_cnt*0.9:
            col_empty.append(column)
        else:
            col_notemp.append(column)       
    data_courses_raw1 = data_courses_raw1[col_notemp]
    log_file = 'data_check.txt'
    col_str,col_num,col_unc = sortcols(data_courses_raw1)
    with open(log_file,'wb') as f:    
        for column in data_courses_raw1.columns:       
            tmp_stat = data_courses_raw1.groupby(column)[column].count()       
            f.write(bytes(str(tmp_stat),'utf-8'))
            f.write(b'\n*************************************\n')
    # 对于离散变量则需要检查枚举值的统计情况，看看是否有的列只有少数几个无用的枚举值
    log_file = './data/data_check.txt'
    with open(log_file,'wb') as f:    
        row_num = data_courses_raw1.shape[0]    
        for column in col_str:
            val_cnt = len(pd.unique(data_courses_raw1[column]))
            if val_cnt >=row_num/3 or val_cnt>=15 :
                f.write(bytes(column+' 属于离散枚举值','utf-8'))
            else:
                tmp_stat = data_courses_raw1.groupby(column)[column].count()
                f.write(bytes(str(tmp_stat),'utf-8'))       
            f.write(b'\n*************************************\n')
    col_selected1 = ['productId','productName','description','categoryId'\
                             ,'provider','targetUrl'\
                             ,'originalPrice','discountPrice'\
                             ,'learnerCount','score','scoreLevel'
                             ,'productType','isTopGrade','topGrade']
    data_courses_1 = data_courses_raw1[col_selected1]
    data_courses_1 = data_courses_1.drop_duplicates(subset=['productId'])
    today=datetime.date.today().strftime("%Y_%m_%d")
    file_cat='./data/'+today+'.csv'
    category=data_category.fillna(0)
    data=data_courses_1.fillna(0)
    data=data.replace(to_replace=-1, value=0)
    data.to_csv(file_cat)
    QMessageBox.information(None, "提示", "数据已经成功获取！", QMessageBox.Yes)
    return np.array(data),np.array(category)[:,1:]#返回处理后的数据
#制作学习人数分布图，并将该图存入./picture文件夹下
def learnerDistribution(data,cate):
    sort=np.unique(cate[:,0])
    number=np.zeros(len(sort))
    lenth=len(cate[:,0])
    for i in range(0,len(data[:,3])):
        for j in range(0,lenth):
            if data[:,3][i]==cate[j,3]:
                number+=(cate[j,0]==sort)
    plt.rcParams['font.sans-serif']='SimHei'#设置中文显示
    plt.figure(num='CCourse云课程管家',figsize=(6,6))#将画布设定为正方形，则绘制的饼图是正圆
    label=sort#定义饼图的标签，标签是列表
    explode=[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]#设定各项距离圆心n个半径
    #plt.pie(values[-1,3:6],explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
    values=number
    plt.pie(values,explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
    plt.title('学习人数占比',size=16)#绘制标题
    plt.savefig('./picture/课堂各类型学习人数占比')#保存图片
    plt.show()
#制作收入情况分布图，并将该图存入./picture文件夹下
def revenueDistribution(data,cate):
    sort=np.unique(cate[:,0])
    revenue=np.zeros(len(sort))
    lenth=len(cate[:,0])    
    for i in range(0,len(data[:,3])):
        for j in range(0,lenth):
            if data[:,3][i]==cate[j,3]:
                revenue[cate[j,0]==sort]+=data[i,7]*data[i,8]
    plt.rcParams['font.sans-serif']='SimHei'#设置中文显示
    plt.figure(num='CCourse云课程管家',figsize=(6,6))#将画布设定为正方形，则绘制的饼图是正圆
    label=sort#定义饼图的标签，标签是列表
    explode=revenue/revenue.sum()#设定各项距离圆心n个半径
    #plt.pie(values[-1,3:6],explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
    values=revenue
    plt.pie(values,explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
    plt.title('收入占比',size=16)#绘制标题
    plt.savefig('./picture/课堂各类型课程利润占比')#保存图片
    plt.show()
#制作课程主题类别及数量分布图，分为免费和付费课程两种，并将该图存入./picture文件夹下
def couseNumber(data,cate):
    sort=np.unique(cate[:,0])
    freenumber=np.zeros(len(sort))
    earnnumber=np.zeros(len(sort))
    lenth=len(cate[:,0])    
    for i in range(0,len(data[:,3])):
        for j in range(0,lenth):
            if data[:,3][i]==cate[j,3]:
                if data[:,7][i]==0:
                    freenumber+=(cate[j,0]==sort)
                else:
                    earnnumber+=(cate[j,0]==sort)
    plt.rcParams['font.sans-serif']='SimHei'
    plt.figure(num='CCourse云课程管家',figsize=(10,8))
    n = len(earnnumber)
    X = np.arange(n)+1 #X是1,2,3,4,5,6,7,8,柱的个数
    #uniform均匀分布的随机数，normal是正态分布的随机数，0.5-1均匀分布的数，一共有n个
    plt.bar(X-0.2, freenumber, alpha=0.9, width = 0.4, label='免费课程', lw=1)#,color = 'c'
    for a,b in zip(X,freenumber):
        plt.text(a-0.2, b+0.5, '%.0f' % b, ha='center', va= 'bottom',fontsize=12)
    plt.xticks(X,sort,rotation=30)
    plt.tick_params(labelsize=13)
    plt.bar(X+0.2, earnnumber, alpha=0.9, width = 0.4, label='付费课程', lw=1)#color = 'yellow'
    for a,b in zip(X,earnnumber):
        plt.text(a+0.2, b+0.5, '%.0f' % b, ha='center', va= 'bottom',fontsize=12)
    #plt.xlabel('课程主题类别及数量',size=20)
    plt.ylabel('number',size=15)
    plt.title('数量分布',size=20)#不同类别的课程数量
    plt.legend(loc="upper left") # label的位置在左上，没有这句会找不到label去哪了
    plt.savefig('./picture/课程主题类别及数量')
    plt.show()
#数据分类处理
def  data_classification(data,cate,name):
    sort=np.unique(cate[:,0])
    lenth=len(cate[:,0])
    namesort=[]
    for i in range(0,len(data[:,3])):
        for j in range(0,lenth):
            if data[:,3][i]==cate[j,3]:
                if cate[j,0]==name:
                    namesort.append(data[i].tolist())
    return np.array(namesort)
#将课程分类，共九类
def data_class(namenumber):
    if int(namenumber) == 1:
        name='AI/数据科学'
    elif int(namenumber)==2:
        name='产品与运营'
    elif int(namenumber)==3:
        name='生活兴趣'
    elif int(namenumber)==4:
        name='电商运营'
    elif int(namenumber)==5:
        name='编程与开发'
    elif int(namenumber)==6:
        name='职业考试'
    elif int(namenumber)==7:
        name='职场提升'
    elif int(namenumber)==8:
        name='设计创意'
    else :
        name='语言学习'
    return name
#获取数据
def get_data():
    try:
        today=datetime.date.today().strftime("%Y_%m_%d")
        file_cat='./data/'+today+'.csv'
        data=pd.read_csv(file_cat)
        data_category = pd.read_csv('./category/categorydata.csv')
        data=np.array(data)[:,1:]
        cate=np.array(data_category)[:,1:]
        QMessageBox.information(None, "提示", "数据已经成功获取！", QMessageBox.Yes)
    except:
        flag=0
        while flag<1:
            try:
                data,cate=data_capture()
                flag=10
            except:
                flag+=1           
        if(flag<10):
            try:
                days=1
                while days<365:
                    try:
                        oneday=datetime.timedelta(days=days)
                        today=datetime.date.today()
                        day=(today-oneday).strftime("%Y_%m_%d")
                        file_cat='./data/'+day+'.csv'
                        data=pd.read_csv(file_cat)
                        data_category = pd.read_csv('./category/categorydata.csv')
                        data=np.array(data)[:,1:]
                        cate=np.array(data_category)[:,1:]
                        days=365
                    except:
                        days+=1
            except:
                file_cat='./data/2020_02_17.csv'
                data=pd.read_csv(file_cat)
                data_category = pd.read_csv('./category/categorydata.csv')
                data=np.array(data)[:,1:]
                cate=np.array(data_category)[:,1:]
            QMessageBox.information(None, "提示", "数据已经成功获取！", QMessageBox.Yes)
    return data,cate
#获取往前数据
def get_pastdata(days):
    try:
        while days<365:
            try:
                oneday=datetime.timedelta(days=days)
                today=datetime.date.today()
                day=(today-oneday).strftime("%Y_%m_%d")
                file_cat='./data/'+day+'.csv'
                data=pd.read_csv(file_cat)
                data_category = pd.read_csv('./category/categorydata.csv')
                data=np.array(data)[:,1:]
                cate=np.array(data_category)[:,1:]
                days=365
            except:
                days+=1
    except:
        try:
            file_cat='./data/2020_02_17.csv'
            data=pd.read_csv(file_cat)
            data_category = pd.read_csv('./category/categorydata.csv')
            data=np.array(data)[:,1:]
            cate=np.array(data_category)[:,1:]
        except:
            data,cate=get_data()
    return data,cate
#获取往期pandas数据
def get_pandasdata():
    days=0
    try:
        while days<365:
            try:
                oneday=datetime.timedelta(days=days)
                today=datetime.date.today()
                day=(today-oneday).strftime("%Y_%m_%d")
                file_cat='./data/'+day+'.csv'
                data=pd.read_csv(file_cat)
                days=365
            except:
                days+=1
    except:
        try:
            file_cat='./data/2020_02_17.csv'
            data=pd.read_csv(file_cat)
        except:
            pass
    return data
#生成数据分析报告
def report():
    global pathurl
    pathhere=pathurl+"/analysis_report.html"
    try:
        #生成数据分析报告
        import pandas_profiling
        QMessageBox.information(None, "提示", "正在生成报告，报告生成后将会提醒您，请稍候。", QMessageBox.Yes)
        data=get_pandasdata()
        profile =data.profile_report(title='慕课数据分析报告')   
        profile.to_file(pathhere)
    except:
        pass
    try:
        os.system(pathhere)
    except:   
        QMessageBox.information(None, "提示", "报告已生成，请到report文件夹下查看analysis_report.html报告。", QMessageBox.Yes)
#制作词云图
def cloud(data,number,picture):
    path_of_font ="./word/DroidSansFallbackFull.ttf"
    outfile = open(r'./word/ciyun.txt','w',encoding='utf-8')
    for eachline in [ i for i in data[:,number]]:#data[:,1]
         outfile.write(str(eachline))
    outfile.close()
    #从本地文件系统读取内容
    text_from_file_with_path = open('./word/ciyun.txt',encoding = 'utf-8').read()
    wordlist_after_jieba = jieba.cut(text_from_file_with_path, cut_all = True)
    wl_space_split = " ".join(wordlist_after_jieba)
    if picture==1:
        mask = np.array(Image.open('./picture/男人.jpg'))
    else:
        mask = np.array(Image.open('./picture/女人.jpg'))
    my_wordcloud = WordCloud(font_path=path_of_font,mask=mask,background_color='white',max_font_size=60).generate(wl_space_split)#mask=mask,
    plt.figure(num='CCourse云课程管家',figsize=(7,6))#
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()
def treeviewClick(event):
    pass
#制作学习人数排名图表
class learnerRank():
    def __init__(self,data,cate):
        self.data=data
        self.cate=cate
    def data_hand(self,classdata):
        #classdata=data_classification(self.data,self.cate,classfication)
        lenth=len(self.cate[:,0])
        ll=[int(float(i)) for i in classdata[:,8].tolist()]
        LearnerCount=np.argsort(ll)#numdata[:,8]
        LearnerCount=LearnerCount[-1:0:-1]
        LearnerCountResult=[]
        LearnerCountResult2=[]
        LearnerCountnew=[]
        for i in LearnerCount:
            LearnerCountnew.append([classdata[:,0][i],classdata[:,1][i],classdata[:,4][i],classdata[:,7][i],classdata[:,8][i]])
            for j in range(0,lenth):
                if int(classdata[:,3][i])==(self.cate[j,3]):
                    LearnerCountResult.append(self.cate[j,0])
                    LearnerCountResult2.append(self.cate[j,1])
        LearnerCountanalyse=pd.DataFrame({'category':LearnerCountResult,'type':LearnerCountResult2,'productName':[ i[1] for i in LearnerCountnew],'provider':[ i[2] for i in LearnerCountnew],'discountPrice':[ i[3] for i in LearnerCountnew],'learnerCount':[ i[4] for i in LearnerCountnew]},index=['%d'%i for i in range(1,len(LearnerCountnew)+1)])
        namelist=list(LearnerCountanalyse)#'productId':[ i[0] for i in LearnerCountnew],
        data=np.array(LearnerCountanalyse)
        for i in range(len(data[:,3])):
            if data[i,3]==0 or data[i,3]=='0':
                data[i,3]='NULL'
        #创建tkinter应用程序窗口
        root = tk.Tk()
        #root=tk.Tk()
        #设置窗口大小和位置
        root.geometry('800x540')
        #不允许改变窗口大小
        root.resizable(False, False)
        #设置窗口标题
        root.title("学习人数排名")
        #使用Treeview组件实现表格功能
        frame = Frame(root)
        frame.place(x=0, y=10, width=800, height=540)
        #滚动条
        scrollBar = tk.Scrollbar(frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        #Treeview组件，6列，显示表头，带垂直滚动条'a4'tree.column('a4', width=100, anchor='center')tree.heading('a4', text='作品编号')
        tree = Treeview(frame,
        columns=('a1', 'a2', 'a3', 'a5', 'a6','a7','a8'),
        show="headings",
        yscrollcommand=scrollBar.set)
        #设置每列宽度和对齐方式
        tree.column('a1', width=40, anchor='center')
        tree.column('a2', width=100, anchor='center')
        tree.column('a3', width=100, anchor='center')
        tree.column('a5', width=240, anchor='center')
        tree.column('a6', width=130, anchor='center')
        tree.column('a7', width=80, anchor='center')
        tree.column('a8', width=100, anchor='center')
        #设置每列表头标题文本
        tree.heading('a1', text='排名')
        tree.heading('a2', text='类别')
        tree.heading('a3', text='小类')
        tree.heading('a5', text='名称')
        tree.heading('a6', text='作者')
        tree.heading('a7', text='价格')
        tree.heading('a8', text='学习人数')
        tree.pack(side=tk.LEFT, fill=tk.Y)
        #Treeview组件与垂直滚动条结合
        scrollBar.config(command=tree.yview)
        #定义并绑定Treeview组件的鼠标单击事件
        tree.bind('<Button-1>', treeviewClick)
        #插入演示数据
        for i in range(len(data)):
            tree.insert('', i, values=[str(i+1)]+[str(data[i,j]) for j in range(len(namelist))])
        #运行程序，启动事件循环
        root.mainloop()
#制作收入排名图表
class revenueRank():
    def __init__(self,data,cate):
        self.data=data
        self.cate=cate
    def data_hand(self,classdata):
        #classdata=data_classification(self.data,self.cate,classfication)
        lenth=len(self.cate[:,0])
        l1=[float(i) for i in classdata[:,7].tolist()]
        l2=[float(i) for i in classdata[:,8].tolist()]
        ll=np.array(l1)*np.array(l2)
        revenueCount=np.argsort(ll)#numdata[:,8]
        revenueCount=revenueCount[-1:0:-1]
        revenueCountResult=[]
        revenueCountResult2=[]
        revenueCountnew=[]
        for i in revenueCount:
            revenueCountnew.append([classdata[:,1][i],classdata[:,4][i],classdata[:,7][i],ll[i]])
            for j in range(0,lenth):
                if int(classdata[:,3][i])==(self.cate[j,3]):
                    revenueCountResult.append(self.cate[j,0])
                    revenueCountResult2.append(self.cate[j,1])
        revenueCountanalyse=pd.DataFrame({'category':revenueCountResult,'type':revenueCountResult2,'productName':[ i[0] for i in revenueCountnew],'provider':[ i[1] for i in revenueCountnew],'discountPrice':[ i[2] for i in revenueCountnew],'revenue':[ i[3] for i in revenueCountnew]},index=['%d'%i for i in range(1,len(revenueCountnew)+1)])
        namelist=list(revenueCountanalyse)
        data=np.array(revenueCountanalyse)
        for i in range(len(data[:,3])):
            if data[i,3]==0 or data[i,3]=='0':
                data[i,3]='NULL'
        #创建tkinter应用程序窗口
        root = tk.Tk()
        #root=tk.Tk()
        #设置窗口大小和位置
        root.geometry('800x540')
        #不允许改变窗口大小
        root.resizable(False, False)
        #设置窗口标题
        root.title('收入排名')
        #使用Treeview组件实现表格功能
        frame = Frame(root)
        frame.place(x=0, y=10, width=800, height=540)
        #滚动条
        scrollBar = tk.Scrollbar(frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        #Treeview组件，6列，显示表头，带垂直滚动条'a4'tree.column('a4', width=100, anchor='center')tree.heading('a4', text='作品编号')
        tree = Treeview(frame,
        columns=('a1', 'a2', 'a3', 'a5', 'a6','a7','a8'),
        show="headings",
        yscrollcommand=scrollBar.set)
        #设置每列宽度和对齐方式
        tree.column('a1', width=40, anchor='center')
        tree.column('a2', width=100, anchor='center')
        tree.column('a3', width=100, anchor='center')
        tree.column('a5', width=240, anchor='center')
        tree.column('a6', width=130, anchor='center')
        tree.column('a7', width=80, anchor='center')
        tree.column('a8', width=100, anchor='center')
        #设置每列表头标题文本
        tree.heading('a1', text='排名')
        tree.heading('a2', text='类别')
        tree.heading('a3', text='小类')
        tree.heading('a5', text='名称')
        tree.heading('a6', text='作者')
        tree.heading('a7', text='价格')
        tree.heading('a8', text='收入')
        tree.pack(side=tk.LEFT, fill=tk.Y)
        #Treeview组件与垂直滚动条结合
        scrollBar.config(command=tree.yview)
        #定义并绑定Treeview组件的鼠标单击事件
        tree.bind('<Button-1>', treeviewClick)
        #插入演示数据
        for i in range(len(data)):
            tree.insert('', i, values=[str(i+1)]+[str(data[i,j]) for j in range(len(namelist))])
        #运行程序，启动事件循环
        root.mainloop()
def get_daysdata(kind,opt,num,dataDraw,dataTime):
    days=0
    while days<365:
        try:
                oneday=datetime.timedelta(days=days)
                today=datetime.date.today()
                day=(today-oneday).strftime("%Y_%m_%d")
                file_cat='./data/'+day+'.csv'
                data=pd.read_csv(file_cat)
                data_category = pd.read_csv('./category/categorydata.csv')
                data=np.array(data)[:,1:]
                cate=np.array(data_category)[:,1:]
                if int(num)!=0:
                    if opt==1:
                        if kind==0:
                            dataDraw.append(data[:,8].mean())
                            dataTime.append(day)
                        else:
                            dataDraw.append(data_classification(data,cate,data_class(kind))[:,8].astype(float).mean())
                            dataTime.append(day)
                    elif opt==2:
                        if kind==0:
                            dataDraw.append(data[:,9].mean())
                            dataTime.append(day)
                        else:
                            data=data_classification(data,cate,data_class(kind))
                            dataDraw.append(data[:,9].astype(float).mean())
                            dataTime.append(day)
                    else:
                        if kind==0:
                            dataDraw.append((data[:,7].astype(float)*data[:,8].astype(float)).mean())
                            dataTime.append(day)
                        else:
                            data=data_classification(data,cate,data_class(kind))
                            dataDraw.append((data[:,7].astype(float)*data[:,8].astype(float)).mean())
                            dataTime.append(day)
                    num-=1
                if num==0:
                    days=400
        except:
            pass
        days+=1
    if days<400:
        QMessageBox.information(None, "提示", "读取数据出错，可能是没有储存足够多的数据，将打印所有您拥有的全部数据", QMessageBox.Yes)
#利用三次条样插值制作趋势图
def trend_days(kind,opt,num):
    dataDraw=[]
    dataTime=[]
    get_daysdata(kind,opt,num,dataDraw,dataTime)
    dataDraw.reverse()
    dataTime.reverse()
    plt.rcParams['font.sans-serif']='SimHei'
    plt.figure(num='CCourse云课程管家',figsize=(10,8))#
    if opt==1:
        if kind==0:
            plt.xlabel('日期',size=15)
            plt.ylabel('总人数/课程数',size=15)
            plt.title('课程平均学习人数随时间变化图',size=20)#不同类别的课程数量
        else:
            plt.xlabel('日期',size=15)
            plt.ylabel('总人数/课程数',size=15)
            plt.title('{}类课程平均学习人数随时间变化图'.format(data_class(kind)),size=20)#不同类别的课程数量
    elif opt==2:
        if kind==0:
            plt.xlabel('日期',size=15)
            plt.ylabel('当日平均得分',size=15)
            plt.title('课程平均得分随时间变化图，课程评分满分为5',size=20)#不同类别的课程数量
        else:
            plt.xlabel('日期',size=15)
            plt.ylabel('当日平均得分',size=15)
            plt.title('{}类课程平均得分随时间变化图，课程评分满分为5'.format(data_class(kind)),size=20)#不同类别的课程数量
    else:
        if kind==0:
            plt.xlabel('日期',size=15)
            plt.ylabel('总收入/课程数',size=15)
            plt.title('课程平均收入随时间变化图',size=20)#不同类别的课程数量
        else:
            plt.xlabel('日期',size=15)
            plt.ylabel('总收入/课程数',size=15)
            plt.title('{}类课程平均收入随时间变化图'.format(data_class(kind)),size=20)#不同类别的课程数量
    number=range(len(dataDraw))
    x=np.array(number)
    y=np.array(dataDraw)
    x_shift,y_shift=0,0
    if num>3:
        y_smooth = interp1d(x, y, kind='cubic')
        x_new = np.linspace(min(x),max(x),num*10)
        plt.plot(x_new,y_smooth(x_new),linewidth = '3')
        if opt==2:
            x_shift,y_shift=0.00001,0.00001
        else:
            x_shift,y_shift=0.1,0.1
    else:
        plt.plot(x,y,linewidth = '3')
    plt.xticks(x,dataTime)
    plt.scatter(x, y)
    if opt==1:
        for i in range(len(x)):
            plt.annotate('%.1f人'%dataDraw[i], xy = (x[i], y[i]), xytext = (x[i]+x_shift, y[i]+y_shift))
    elif opt==2:
        for i in range(len(x)):
            plt.annotate('%.4f分'%dataDraw[i], xy = (x[i], y[i]), xytext = (x[i]+x_shift, y[i]+y_shift))
    else:
        for i in range(len(x)):
            plt.annotate('%.1f元'%dataDraw[i], xy = (x[i], y[i]), xytext = (x[i]+x_shift, y[i]+y_shift))
    plt.show()
    #plt.plot(number,dataDraw)
    #plt.xticks(number,dataTime)
    #plt.show()
#输入天数
def input_days(kind,opt):
    root=tk.Tk(className='请输入天数')
    root.geometry('300x80')
    def com():
        try:
            day=int(e1.get())#获取e1的值，转为浮点数，如果不能转捕获异常
            trend_days(kind,opt,day)
        except:
            messagebox.showwarning('警告','请输入数字')
    e1=tk.Entry(root)
    e1.pack()
    Button(root,text='确认',command=com).pack()
    root.mainloop()
#课程情况预测
def course_forecasting(data,x_t,steps):
    if steps==0:
        QMessageBox.information(None, "提示", "正在训练预测模型，请稍候！", QMessageBox.Yes)
        try:
            x=[]
            for i in range(len(data[:,1])):
                x.append([SnowNLP(data[i,1]).sentiments,SnowNLP(data[i,2]).sentiments,SnowNLP(data[i,4]).sentiments,float(data[i,6]),float(data[i,7])])
            y1=[]
            y2=[]
            for i in range(len(data[:,1])):
                y1.append(float(data[i,8]))
                y2.append(float(data[i,9]))
            model1 = xgb.XGBRegressor(max_depth=5, learning_rate=0.1, n_estimators=160, silent=False)
            model1.fit(np.array(x), np.array(y1),verbose=True)
            model2 = xgb.XGBRegressor(max_depth=5, learning_rate=0.1, n_estimators=160, silent=False)
            model2.fit(np.array(x), np.array(y2),verbose=True)
            model1.save_model('./prediction_model/learners.model')
            model2.save_model('./prediction_model/star.model')
        except:
            pass
    model1 = xgb.XGBRegressor()
    model2 = xgb.XGBRegressor()
    model1.load_model(path+'/prediction_model/learners.model')
    model2.load_model(path+'/prediction_model/star.model')
    x1=[]
    x1.append([SnowNLP(x_t[0]).sentiments,SnowNLP(x_t[1]).sentiments,SnowNLP(x_t[2]).sentiments,float(x_t[3]),float(x_t[4])])
    return model1.predict(np.array(x1))[0],model1.predict(np.array(x1))[0]*float(x_t[4]),5.0 if model2.predict(np.array(x1))[0]>5 else model2.predict(np.array(x1))[0]
#图形界面编程
# coding:utf-8
class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.data,self.cate=get_pastdata(0)
        self.init_ui()
 
    def init_ui(self):
        self.setFixedSize(960,730)
        self.setWindowTitle('CCourse云课程管家')#self.setWindowTitle('CCourse云课程管家')
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
 
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格
 
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格
 
        self.main_layout.addWidget(self.left_widget,0,0,14,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,2,14,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        
        self.left_close = QtWidgets.QPushButton("") # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("") # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_label_0 = QtWidgets.QPushButton("数据获取")
        self.left_label_0.setObjectName('left_label')
        self.left_label_1 = QtWidgets.QPushButton("课程分析")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("教师开课")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')
        
        self.left_button_0 = QtWidgets.QPushButton(qtawesome.icon('fa.download',color='white'),"实时数据")#
        self.left_button_0.clicked.connect(lambda :self.download())
        self.left_button_0.setObjectName('left_button')
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.fire',color='white'),"焦点信息")#change_trend
        self.left_button_1.clicked.connect(lambda :self.important_information())
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.thermometer-full',color='white'),"热门课程")
        self.left_button_2.clicked.connect(lambda :self.popular_courses())
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.book',color='white'),"课程报告")
        self.left_button_3.clicked.connect(lambda :self.report())
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.magic',color='white'),"课程预测")#.tripadvisorfeedback
        self.left_button_4.clicked.connect(lambda :self.predict())
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.line-chart',color='white'),"变化趋势")
        self.left_button_5.clicked.connect(lambda :self.change_trend())
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.pie-chart',color='white'),"课程分布")
        self.left_button_6.clicked.connect(lambda :self.distribution_of_courses())
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment',color='white'),"反馈建议")
        self.left_button_7.clicked.connect(lambda :self.feedback())
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"关注我们")
        self.left_button_8.clicked.connect(lambda :self.join_us())
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question',color='white'),"遇到问题")
        self.left_button_9.clicked.connect(lambda :self.face_problem())
        self.left_button_9.setObjectName('left_button')
        self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_mini, 0, 0,1,1)
        self.left_layout.addWidget(self.left_close, 0, 2,1,1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)   
        self.left_layout.addWidget(self.left_label_0,1,0,1,3)
        self.left_layout.addWidget(self.left_button_0, 2, 0,1,3)
        self.left_layout.addWidget(self.left_label_1,3,0,1,3)
        self.left_layout.addWidget(self.left_button_1, 4, 0,1,3)
        self.left_layout.addWidget(self.left_button_2, 5, 0,1,3)
        self.left_layout.addWidget(self.left_button_3, 6, 0,1,3)
        self.left_layout.addWidget(self.left_label_2, 7, 0,1,3)
        self.left_layout.addWidget(self.left_button_4, 8, 0,1,3)
        self.left_layout.addWidget(self.left_button_5, 9, 0,1,3)
        self.left_layout.addWidget(self.left_button_6, 10, 0,1,3)
        self.left_layout.addWidget(self.left_label_3, 11, 0,1,3)
        self.left_layout.addWidget(self.left_button_7, 12, 0,1,3)
        self.left_layout.addWidget(self.left_button_8, 13, 0,1,3)
        self.left_layout.addWidget(self.left_button_9, 14, 0, 1, 3)
        self.left_close.setFixedSize(15,15) # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15) # 设置最小化按钮大小
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
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
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.important_information()
        self.steps=0
    def ui(self):
        sip.delete(self.right_widget)
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格
        self.main_layout.addWidget(self.right_widget,0,2,14,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
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
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
    def download(self):
        self.data,self.cate=get_data()
    def important_information(self):
        self.ui()
        
        self.right_recommend_label = QtWidgets.QLabel("课程名称关键词")
        self.right_recommend_label.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("AI/数据科学") # 设置按钮文本
        self.recommend_button_1.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(1)),1,0))
        self.recommend_button_1.setIcon(QtGui.QIcon('./picture/数据科学1.jpg')) # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(100,100)) # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("产品与运营")
        self.recommend_button_2.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(2)),1,0))
        self.recommend_button_2.setIcon(QtGui.QIcon('./picture/产品与运营1.jpg'))
        self.recommend_button_2.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("生活兴趣")
        self.recommend_button_3.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(3)),1,0))
        self.recommend_button_3.setIcon(QtGui.QIcon('./picture/生活兴趣1.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_4 = QtWidgets.QToolButton()
        self.recommend_button_4.setText("电商运营")
        self.recommend_button_4.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(4)),1,0))
        self.recommend_button_4.setIcon(QtGui.QIcon('./picture/电商运营1.jpg'))
        self.recommend_button_4.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_5 = QtWidgets.QToolButton()
        self.recommend_button_5.setText("编程与开发")
        self.recommend_button_5.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(5)),1,0))
        self.recommend_button_5.setIcon(QtGui.QIcon('./picture/编程与开发1.jpg'))
        self.recommend_button_5.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_6 = QtWidgets.QToolButton()
        self.recommend_button_6.setText("职业考试")
        self.recommend_button_6.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(6)),1,0))
        self.recommend_button_6.setIcon(QtGui.QIcon('./picture/职业考试1.jpg'))
        self.recommend_button_6.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.recommend_button_7 = QtWidgets.QToolButton()
        self.recommend_button_7.setText("职场提升")
        self.recommend_button_7.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(7)),1,0))
        self.recommend_button_7.setIcon(QtGui.QIcon('./picture/职场提升1.jpg'))
        self.recommend_button_7.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_7.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_8 = QtWidgets.QToolButton()
        self.recommend_button_8.setText("设计创意")
        self.recommend_button_8.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(8)),1,0))
        self.recommend_button_8.setIcon(QtGui.QIcon('./picture/设计创意1.jpg'))
        self.recommend_button_8.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_8.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_9 = QtWidgets.QToolButton()
        self.recommend_button_9.setText("语言学习")
        self.recommend_button_9.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(9)),1,0))
        self.recommend_button_9.setIcon(QtGui.QIcon('./picture/语言学习1.jpg'))
        self.recommend_button_9.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_9.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_10 = QtWidgets.QToolButton()
        self.recommend_button_10.setText("所有课程")
        self.recommend_button_10.clicked.connect(lambda :cloud(self.data,1,0))
        self.recommend_button_10.setIcon(QtGui.QIcon('./picture/所有课程1.jpg'))
        self.recommend_button_10.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_10.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.right_recommend_layout.addWidget(self.recommend_button_1,0,0)
        self.right_recommend_layout.addWidget(self.recommend_button_2,0,1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 0, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_5, 0, 4)
        self.right_recommend_layout.addWidget(self.recommend_button_6,1,0)
        self.right_recommend_layout.addWidget(self.recommend_button_7,1,1)
        self.right_recommend_layout.addWidget(self.recommend_button_8, 1, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_9, 1, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_10, 1, 4)
        
        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)
        
        
        
        self.right_recommend_label1 = QtWidgets.QLabel("课程描述关键词")
        self.right_recommend_label1.setObjectName('right_lable')

        self.right_recommend_widget1 = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout1 = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget1.setLayout(self.right_recommend_layout1)

        self.recommend_button_11 = QtWidgets.QToolButton()
        self.recommend_button_11.setText("AI/数据科学") # 设置按钮文本
        self.recommend_button_11.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(1)),2,1))
        self.recommend_button_11.setIcon(QtGui.QIcon('./picture/数据科学2.jpg')) # 设置按钮图标
        self.recommend_button_11.setIconSize(QtCore.QSize(100,100)) # 设置图标大小
        self.recommend_button_11.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_12 = QtWidgets.QToolButton()
        self.recommend_button_12.setText("产品与运营")
        self.recommend_button_12.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(2)),2,1))
        self.recommend_button_12.setIcon(QtGui.QIcon('./picture/产品与运营2.jpg'))
        self.recommend_button_12.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_12.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_13 = QtWidgets.QToolButton()
        self.recommend_button_13.setText("生活兴趣")
        self.recommend_button_13.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(3)),2,1))
        self.recommend_button_13.setIcon(QtGui.QIcon('./picture/生活兴趣2.jpg'))
        self.recommend_button_13.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_13.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_14 = QtWidgets.QToolButton()
        self.recommend_button_14.setText("电商运营")
        self.recommend_button_14.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(4)),2,1))
        self.recommend_button_14.setIcon(QtGui.QIcon('./picture/电商运营2.jpg'))
        self.recommend_button_14.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_14.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_15 = QtWidgets.QToolButton()
        self.recommend_button_15.setText("编程与开发")
        self.recommend_button_15.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(5)),2,1))
        self.recommend_button_15.setIcon(QtGui.QIcon('./picture/编程与开发2.jpg'))
        self.recommend_button_15.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_15.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_16 = QtWidgets.QToolButton()
        self.recommend_button_16.setText("职业考试")
        self.recommend_button_16.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(6)),2,1))
        self.recommend_button_16.setIcon(QtGui.QIcon('./picture/职业考试2.jpg'))
        self.recommend_button_16.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_16.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.recommend_button_17 = QtWidgets.QToolButton()
        self.recommend_button_17.setText("职场提升")
        self.recommend_button_17.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(7)),2,1))
        self.recommend_button_17.setIcon(QtGui.QIcon('./picture/职场提升2.jpg'))
        self.recommend_button_17.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_17.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_18 = QtWidgets.QToolButton()
        self.recommend_button_18.setText("设计创意")
        self.recommend_button_18.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(8)),2,1))
        self.recommend_button_18.setIcon(QtGui.QIcon('./picture/设计创意2.jpg'))
        self.recommend_button_18.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_18.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_19 = QtWidgets.QToolButton()
        self.recommend_button_19.setText("语言学习")
        self.recommend_button_19.clicked.connect(lambda :cloud(data_classification(self.data,self.cate,data_class(9)),2,1))
        self.recommend_button_19.setIcon(QtGui.QIcon('./picture/语言学习2.jpg'))
        self.recommend_button_19.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_19.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_20 = QtWidgets.QToolButton()
        self.recommend_button_20.setText("所有课程")
        self.recommend_button_20.clicked.connect(lambda :cloud(self.data,2,1))
        self.recommend_button_20.setIcon(QtGui.QIcon('./picture/所有课程2.jpg'))
        self.recommend_button_20.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_20.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.right_recommend_layout1.addWidget(self.recommend_button_11,0,0)
        self.right_recommend_layout1.addWidget(self.recommend_button_12,0,1)
        self.right_recommend_layout1.addWidget(self.recommend_button_13, 0, 2)
        self.right_recommend_layout1.addWidget(self.recommend_button_14, 0, 3)
        self.right_recommend_layout1.addWidget(self.recommend_button_15, 0, 4)
        self.right_recommend_layout1.addWidget(self.recommend_button_16,1,0)
        self.right_recommend_layout1.addWidget(self.recommend_button_17,1,1)
        self.right_recommend_layout1.addWidget(self.recommend_button_18, 1, 2)
        self.right_recommend_layout1.addWidget(self.recommend_button_19, 1, 3)
        self.right_recommend_layout1.addWidget(self.recommend_button_20, 1, 4)
        
        self.right_layout.addWidget(self.right_recommend_label1, 6, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget1, 7, 0, 2, 9)
        
        
        self.right_recommend_widget.setStyleSheet(
        '''
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')
        self.right_recommend_widget1.setStyleSheet(
        '''
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')
    def popular_courses(self):
        self.ui()
        learner=learnerRank(self.data,self.cate)
        revenue=revenueRank(self.data,self.cate)
        self.right_recommend_label = QtWidgets.QLabel("学习人数排名")
        self.right_recommend_label.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("AI/数据科学") # 设置按钮文本
        self.recommend_button_1.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(1))))
        self.recommend_button_1.setIcon(QtGui.QIcon('./picture/数据科学3.jpg')) # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(100,100)) # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("产品与运营")
        self.recommend_button_2.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(2))))
        self.recommend_button_2.setIcon(QtGui.QIcon('./picture/产品与运营3.jpg'))
        self.recommend_button_2.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("生活兴趣")
        self.recommend_button_3.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(3))))
        self.recommend_button_3.setIcon(QtGui.QIcon('./picture/生活兴趣3.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_4 = QtWidgets.QToolButton()
        self.recommend_button_4.setText("电商运营")
        self.recommend_button_4.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(4))))
        self.recommend_button_4.setIcon(QtGui.QIcon('./picture/电商运营3.jpg'))
        self.recommend_button_4.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_5 = QtWidgets.QToolButton()
        self.recommend_button_5.setText("编程与开发")
        self.recommend_button_5.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(5))))
        self.recommend_button_5.setIcon(QtGui.QIcon('./picture/编程与开发3.jpg'))
        self.recommend_button_5.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_6 = QtWidgets.QToolButton()
        self.recommend_button_6.setText("职业考试")
        self.recommend_button_6.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(6))))
        self.recommend_button_6.setIcon(QtGui.QIcon('./picture/职业考试3.jpg'))
        self.recommend_button_6.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.recommend_button_7 = QtWidgets.QToolButton()
        self.recommend_button_7.setText("职场提升")
        self.recommend_button_7.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(7))))
        self.recommend_button_7.setIcon(QtGui.QIcon('./picture/职场提升3.jpg'))
        self.recommend_button_7.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_7.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_8 = QtWidgets.QToolButton()
        self.recommend_button_8.setText("设计创意")
        self.recommend_button_8.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(8))))
        self.recommend_button_8.setIcon(QtGui.QIcon('./picture/设计创意3.jpg'))
        self.recommend_button_8.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_8.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_9 = QtWidgets.QToolButton()
        self.recommend_button_9.setText("语言学习")
        self.recommend_button_9.clicked.connect(lambda :learner.data_hand(data_classification(self.data,self.cate,data_class(9))))
        self.recommend_button_9.setIcon(QtGui.QIcon('./picture/语言学习3.jpg'))
        self.recommend_button_9.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_9.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_10 = QtWidgets.QToolButton()
        self.recommend_button_10.setText("所有课程")
        self.recommend_button_10.clicked.connect(lambda :learner.data_hand(self.data))
        self.recommend_button_10.setIcon(QtGui.QIcon('./picture/所有课程3.jpg'))
        self.recommend_button_10.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_10.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.right_recommend_layout.addWidget(self.recommend_button_1,0,0)
        self.right_recommend_layout.addWidget(self.recommend_button_2,0,1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 0, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_5, 0, 4)
        self.right_recommend_layout.addWidget(self.recommend_button_6,1,0)
        self.right_recommend_layout.addWidget(self.recommend_button_7,1,1)
        self.right_recommend_layout.addWidget(self.recommend_button_8, 1, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_9, 1, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_10, 1, 4)
        
        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)
        
        
        
        self.right_recommend_label1 = QtWidgets.QLabel("课程收入排名")
        self.right_recommend_label1.setObjectName('right_lable')

        self.right_recommend_widget1 = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout1 = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget1.setLayout(self.right_recommend_layout1)

        self.recommend_button_11 = QtWidgets.QToolButton()
        self.recommend_button_11.setText("AI/数据科学") # 设置按钮文本
        self.recommend_button_11.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(1))))
        self.recommend_button_11.setIcon(QtGui.QIcon('./picture/数据科学4.jpg')) # 设置按钮图标
        self.recommend_button_11.setIconSize(QtCore.QSize(100,100)) # 设置图标大小
        self.recommend_button_11.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_12 = QtWidgets.QToolButton()
        self.recommend_button_12.setText("产品与运营")
        self.recommend_button_12.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(2))))
        self.recommend_button_12.setIcon(QtGui.QIcon('./picture/产品与运营4.jpg'))
        self.recommend_button_12.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_12.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_13 = QtWidgets.QToolButton()
        self.recommend_button_13.setText("生活兴趣")
        self.recommend_button_13.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(3))))
        self.recommend_button_13.setIcon(QtGui.QIcon('./picture/生活兴趣4.jpg'))
        self.recommend_button_13.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_13.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_14 = QtWidgets.QToolButton()
        self.recommend_button_14.setText("电商运营")
        self.recommend_button_14.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(4))))
        self.recommend_button_14.setIcon(QtGui.QIcon('./picture/电商运营4.jpg'))
        self.recommend_button_14.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_14.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_15 = QtWidgets.QToolButton()
        self.recommend_button_15.setText("编程与开发")
        self.recommend_button_15.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(5))))
        self.recommend_button_15.setIcon(QtGui.QIcon('./picture/编程与开发4.jpg'))
        self.recommend_button_15.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_15.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_16 = QtWidgets.QToolButton()
        self.recommend_button_16.setText("职业考试")
        self.recommend_button_16.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(6))))
        self.recommend_button_16.setIcon(QtGui.QIcon('./picture/职业考试4.jpg'))
        self.recommend_button_16.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_16.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.recommend_button_17 = QtWidgets.QToolButton()
        self.recommend_button_17.setText("职场提升")
        self.recommend_button_17.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(7))))
        self.recommend_button_17.setIcon(QtGui.QIcon('./picture/职场提升4.jpg'))
        self.recommend_button_17.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_17.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_18 = QtWidgets.QToolButton()
        self.recommend_button_18.setText("设计创意")
        self.recommend_button_18.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(8))))
        self.recommend_button_18.setIcon(QtGui.QIcon('./picture/设计创意4.jpg'))
        self.recommend_button_18.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_18.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_19 = QtWidgets.QToolButton()
        self.recommend_button_19.setText("语言学习")
        self.recommend_button_19.clicked.connect(lambda :revenue.data_hand(data_classification(self.data,self.cate,data_class(9))))
        self.recommend_button_19.setIcon(QtGui.QIcon('./picture/语言学习4.jpg'))
        self.recommend_button_19.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_19.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_20 = QtWidgets.QToolButton()
        self.recommend_button_20.setText("所有课程")
        self.recommend_button_20.clicked.connect(lambda :revenue.data_hand(self.data))
        self.recommend_button_20.setIcon(QtGui.QIcon('./picture/所有课程4.jpg'))
        self.recommend_button_20.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_20.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.right_recommend_layout1.addWidget(self.recommend_button_11,0,0)
        self.right_recommend_layout1.addWidget(self.recommend_button_12,0,1)
        self.right_recommend_layout1.addWidget(self.recommend_button_13, 0, 2)
        self.right_recommend_layout1.addWidget(self.recommend_button_14, 0, 3)
        self.right_recommend_layout1.addWidget(self.recommend_button_15, 0, 4)
        self.right_recommend_layout1.addWidget(self.recommend_button_16,1,0)
        self.right_recommend_layout1.addWidget(self.recommend_button_17,1,1)
        self.right_recommend_layout1.addWidget(self.recommend_button_18, 1, 2)
        self.right_recommend_layout1.addWidget(self.recommend_button_19, 1, 3)
        self.right_recommend_layout1.addWidget(self.recommend_button_20, 1, 4)
        
        self.right_layout.addWidget(self.right_recommend_label1, 5, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget1, 6, 0, 2, 9)
        
        
        self.right_recommend_widget.setStyleSheet(
        '''
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')
        self.right_recommend_widget1.setStyleSheet(
        '''
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')
    def report(self):
        report()
    def change_trend(self):
        self.ui()
        learner=learnerRank(self.data,self.cate)
        self.right_recommend_label = QtWidgets.QLabel("课程平均收入")
        self.right_recommend_label.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("AI/数据科学") # 设置按钮文本
        self.recommend_button_1.clicked.connect(lambda :input_days(1,3))
        self.recommend_button_1.setIcon(QtGui.QIcon('./picture/数据科学5.jpg')) # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(100,60)) # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("产品与运营")
        self.recommend_button_2.clicked.connect(lambda :input_days(2,3))
        self.recommend_button_2.setIcon(QtGui.QIcon('./picture/产品与运营5.jpg'))
        self.recommend_button_2.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("生活兴趣")
        self.recommend_button_3.clicked.connect(lambda :input_days(3,3))
        self.recommend_button_3.setIcon(QtGui.QIcon('./picture/生活兴趣5.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_4 = QtWidgets.QToolButton()
        self.recommend_button_4.setText("电商运营")
        self.recommend_button_4.clicked.connect(lambda :input_days(4,3))
        self.recommend_button_4.setIcon(QtGui.QIcon('./picture/电商运营5.jpg'))
        self.recommend_button_4.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_5 = QtWidgets.QToolButton()
        self.recommend_button_5.setText("编程与开发")
        self.recommend_button_5.clicked.connect(lambda :input_days(5,3))
        self.recommend_button_5.setIcon(QtGui.QIcon('./picture/编程与开发5.jpg'))
        self.recommend_button_5.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_6 = QtWidgets.QToolButton()
        self.recommend_button_6.setText("职业考试")
        self.recommend_button_6.clicked.connect(lambda :input_days(6,3))
        self.recommend_button_6.setIcon(QtGui.QIcon('./picture/职业考试5.jpg'))
        self.recommend_button_6.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.recommend_button_7 = QtWidgets.QToolButton()
        self.recommend_button_7.setText("职场提升")
        self.recommend_button_7.clicked.connect(lambda :input_days(7,3))
        self.recommend_button_7.setIcon(QtGui.QIcon('./picture/职场提升5.jpg'))
        self.recommend_button_7.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_7.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_8 = QtWidgets.QToolButton()
        self.recommend_button_8.setText("设计创意")
        self.recommend_button_8.clicked.connect(lambda :input_days(8,3))
        self.recommend_button_8.setIcon(QtGui.QIcon('./picture/设计创意5.jpg'))
        self.recommend_button_8.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_8.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_9 = QtWidgets.QToolButton()
        self.recommend_button_9.setText("语言学习")
        self.recommend_button_9.clicked.connect(lambda :input_days(9,3))
        self.recommend_button_9.setIcon(QtGui.QIcon('./picture/语言学习5.jpg'))
        self.recommend_button_9.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_9.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_10 = QtWidgets.QToolButton()
        self.recommend_button_10.setText("所有课程")
        self.recommend_button_10.clicked.connect(lambda :input_days(0,3))
        self.recommend_button_10.setIcon(QtGui.QIcon('./picture/所有课程5.jpg'))
        self.recommend_button_10.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_10.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.right_recommend_layout.addWidget(self.recommend_button_1,0,0)
        self.right_recommend_layout.addWidget(self.recommend_button_2,0,1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 0, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_5, 0, 4)
        self.right_recommend_layout.addWidget(self.recommend_button_6,1,0)
        self.right_recommend_layout.addWidget(self.recommend_button_7,1,1)
        self.right_recommend_layout.addWidget(self.recommend_button_8, 1, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_9, 1, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_10, 1, 4)
        
        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)
        
        
        
        self.right_recommend_label1 = QtWidgets.QLabel("课程平均得分")
        self.right_recommend_label1.setObjectName('right_lable')

        self.right_recommend_widget1 = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout1 = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget1.setLayout(self.right_recommend_layout1)

        self.recommend_button_11 = QtWidgets.QToolButton()
        self.recommend_button_11.setText("AI/数据科学") # 设置按钮文本
        self.recommend_button_11.clicked.connect(lambda :input_days(1,2))
        self.recommend_button_11.setIcon(QtGui.QIcon('./picture/数据科学6.jpg')) # 设置按钮图标
        self.recommend_button_11.setIconSize(QtCore.QSize(100,60)) # 设置图标大小
        self.recommend_button_11.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_12 = QtWidgets.QToolButton()
        self.recommend_button_12.setText("产品与运营")
        self.recommend_button_12.clicked.connect(lambda :input_days(2,2))
        self.recommend_button_12.setIcon(QtGui.QIcon('./picture/产品与运营6.jpg'))
        self.recommend_button_12.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_12.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_13 = QtWidgets.QToolButton()
        self.recommend_button_13.setText("生活兴趣")
        self.recommend_button_13.clicked.connect(lambda :input_days(3,2))
        self.recommend_button_13.setIcon(QtGui.QIcon('./picture/生活兴趣6.jpg'))
        self.recommend_button_13.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_13.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_14 = QtWidgets.QToolButton()
        self.recommend_button_14.setText("电商运营")
        self.recommend_button_14.clicked.connect(lambda :input_days(4,2))
        self.recommend_button_14.setIcon(QtGui.QIcon('./picture/电商运营6.jpg'))
        self.recommend_button_14.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_14.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_15 = QtWidgets.QToolButton()
        self.recommend_button_15.setText("编程与开发")
        self.recommend_button_15.clicked.connect(lambda :input_days(5,2))
        self.recommend_button_15.setIcon(QtGui.QIcon('./picture/编程与开发6.jpg'))
        self.recommend_button_15.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_15.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_16 = QtWidgets.QToolButton()
        self.recommend_button_16.setText("职业考试")
        self.recommend_button_16.clicked.connect(lambda :input_days(6,2))
        self.recommend_button_16.setIcon(QtGui.QIcon('./picture/职业考试6.jpg'))
        self.recommend_button_16.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_16.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.recommend_button_17 = QtWidgets.QToolButton()
        self.recommend_button_17.setText("职场提升")
        self.recommend_button_17.clicked.connect(lambda :input_days(7,2))
        self.recommend_button_17.setIcon(QtGui.QIcon('./picture/职场提升6.jpg'))
        self.recommend_button_17.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_17.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_18 = QtWidgets.QToolButton()
        self.recommend_button_18.setText("设计创意")
        self.recommend_button_18.clicked.connect(lambda :input_days(8,2))
        self.recommend_button_18.setIcon(QtGui.QIcon('./picture/设计创意2.jpg'))
        self.recommend_button_18.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_18.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_19 = QtWidgets.QToolButton()
        self.recommend_button_19.setText("语言学习")
        self.recommend_button_19.clicked.connect(lambda :input_days(9,2))
        self.recommend_button_19.setIcon(QtGui.QIcon('./picture/语言学习6.jpg'))
        self.recommend_button_19.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_19.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_20 = QtWidgets.QToolButton()
        self.recommend_button_20.setText("所有课程")
        self.recommend_button_20.clicked.connect(lambda :input_days(0,2))
        self.recommend_button_20.setIcon(QtGui.QIcon('./picture/所有课程6.jpg'))
        self.recommend_button_20.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_20.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.right_recommend_layout1.addWidget(self.recommend_button_11,0,0)
        self.right_recommend_layout1.addWidget(self.recommend_button_12,0,1)
        self.right_recommend_layout1.addWidget(self.recommend_button_13, 0, 2)
        self.right_recommend_layout1.addWidget(self.recommend_button_14, 0, 3)
        self.right_recommend_layout1.addWidget(self.recommend_button_15, 0, 4)
        self.right_recommend_layout1.addWidget(self.recommend_button_16,1,0)
        self.right_recommend_layout1.addWidget(self.recommend_button_17,1,1)
        self.right_recommend_layout1.addWidget(self.recommend_button_18, 1, 2)
        self.right_recommend_layout1.addWidget(self.recommend_button_19, 1, 3)
        self.right_recommend_layout1.addWidget(self.recommend_button_20, 1, 4)
        
        self.right_layout.addWidget(self.right_recommend_label1, 5, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget1, 6, 0, 2, 9)
        
        
        
        self.right_recommend_label2 = QtWidgets.QLabel("平均学习人数")
        self.right_recommend_label2.setObjectName('right_lable')

        self.right_recommend_widget2 = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout2 = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget2.setLayout(self.right_recommend_layout2)

        self.recommend_button_21 = QtWidgets.QToolButton()
        self.recommend_button_21.setText("AI/数据科学") # 设置按钮文本
        self.recommend_button_21.clicked.connect(lambda :input_days(1,1))
        self.recommend_button_21.setIcon(QtGui.QIcon('./picture/数据科学7.jpg')) # 设置按钮图标
        self.recommend_button_21.setIconSize(QtCore.QSize(100,60)) # 设置图标大小
        self.recommend_button_21.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_22 = QtWidgets.QToolButton()
        self.recommend_button_22.setText("产品与运营")
        self.recommend_button_22.clicked.connect(lambda :input_days(2,1))
        self.recommend_button_22.setIcon(QtGui.QIcon('./picture/产品与运营7.jpg'))
        self.recommend_button_22.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_22.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_23 = QtWidgets.QToolButton()
        self.recommend_button_23.setText("生活兴趣")
        self.recommend_button_23.clicked.connect(lambda :input_days(3,1))
        self.recommend_button_23.setIcon(QtGui.QIcon('./picture/生活兴趣7.jpg'))
        self.recommend_button_23.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_23.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_24 = QtWidgets.QToolButton()
        self.recommend_button_24.setText("电商运营")
        self.recommend_button_24.clicked.connect(lambda :input_days(4,1))
        self.recommend_button_24.setIcon(QtGui.QIcon('./picture/电商运营7.jpg'))
        self.recommend_button_24.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_24.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_25 = QtWidgets.QToolButton()
        self.recommend_button_25.setText("编程与开发")
        self.recommend_button_25.clicked.connect(lambda :input_days(5,1))
        self.recommend_button_25.setIcon(QtGui.QIcon('./picture/编程与开发7.jpg'))
        self.recommend_button_25.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_25.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_26 = QtWidgets.QToolButton()
        self.recommend_button_26.setText("职业考试")
        self.recommend_button_26.clicked.connect(lambda :input_days(6,1))
        self.recommend_button_26.setIcon(QtGui.QIcon('./picture/职业考试7.jpg'))
        self.recommend_button_26.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_26.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.recommend_button_27 = QtWidgets.QToolButton()
        self.recommend_button_27.setText("职场提升")
        self.recommend_button_27.clicked.connect(lambda :input_days(7,1))
        self.recommend_button_27.setIcon(QtGui.QIcon('./picture/职场提升7.jpg'))
        self.recommend_button_27.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_27.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_28 = QtWidgets.QToolButton()
        self.recommend_button_28.setText("设计创意")
        self.recommend_button_28.clicked.connect(lambda :input_days(8,1))
        self.recommend_button_28.setIcon(QtGui.QIcon('./picture/设计创意7.jpg'))
        self.recommend_button_28.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_28.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_29 = QtWidgets.QToolButton()
        self.recommend_button_29.setText("语言学习")
        self.recommend_button_29.clicked.connect(lambda :input_days(9,1))
        self.recommend_button_29.setIcon(QtGui.QIcon('./picture/语言学习7.jpg'))
        self.recommend_button_29.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_29.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_30 = QtWidgets.QToolButton()
        self.recommend_button_30.setText("所有课程")
        self.recommend_button_30.clicked.connect(lambda :input_days(0,1))
        self.recommend_button_30.setIcon(QtGui.QIcon('./picture/所有课程7.jpg'))
        self.recommend_button_30.setIconSize(QtCore.QSize(100,60))
        self.recommend_button_30.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.right_recommend_layout2.addWidget(self.recommend_button_21,0,0)
        self.right_recommend_layout2.addWidget(self.recommend_button_22,0,1)
        self.right_recommend_layout2.addWidget(self.recommend_button_23, 0, 2)
        self.right_recommend_layout2.addWidget(self.recommend_button_24, 0, 3)
        self.right_recommend_layout2.addWidget(self.recommend_button_25, 0, 4)
        self.right_recommend_layout2.addWidget(self.recommend_button_26,1,0)
        self.right_recommend_layout2.addWidget(self.recommend_button_27,1,1)
        self.right_recommend_layout2.addWidget(self.recommend_button_28, 1, 2)
        self.right_recommend_layout2.addWidget(self.recommend_button_29, 1, 3)
        self.right_recommend_layout2.addWidget(self.recommend_button_30, 1, 4)
        
        self.right_layout.addWidget(self.right_recommend_label2, 9, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget2, 10, 0, 2, 9)
        
        
        
        self.right_recommend_widget.setStyleSheet(
        '''
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')
        self.right_recommend_widget1.setStyleSheet(
        '''
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')  
        self.right_recommend_widget2.setStyleSheet(
        '''
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''') 
    def distribution_of_courses(self):
        self.ui()
        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("数量分布") # 设置按钮文本
        self.recommend_button_1.clicked.connect(lambda :couseNumber(self.data,self.cate))
        self.recommend_button_1.setIcon(QtGui.QIcon('./picture/课程数量分布.jpg')) # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(140,140)) # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("收入占比")
        self.recommend_button_2.clicked.connect(lambda :revenueDistribution(self.data,self.cate))
        self.recommend_button_2.setIcon(QtGui.QIcon('./picture/课程收入占比.jpg'))
        self.recommend_button_2.setIconSize(QtCore.QSize(140, 140))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("学习人数占比")
        self.recommend_button_3.clicked.connect(lambda :learnerDistribution(self.data,self.cate))
        self.recommend_button_3.setIcon(QtGui.QIcon('./picture/学习人数占比.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(140, 140))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        
        
        self.right_recommend_layout.addWidget(self.recommend_button_1,0,0)
        self.right_recommend_layout.addWidget(self.recommend_button_2,0,1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)

        self.right_layout.addWidget(self.right_recommend_widget, 1, 0, 1, 9)
        self.right_recommend_widget.setStyleSheet(
        '''
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')
        
    def feedback(self):
        self.ui()
        self.right_recommend_label = QtWidgets.QLabel("若您有任何指导性的建议，请反馈到我们的邮箱:2102735991@qq.com，谢谢合作!")
        self.right_recommend_label.setObjectName('right_lable')
        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
    def join_us(self):
        self.ui()
        self.right_recommend_label = QtWidgets.QLabel("我们的QQ公众号为:2707571796，里面会发布一些关于这个软件的有趣小故事。\n欢迎并期待您加入我们这个大家庭。")
        self.right_recommend_label.setObjectName('right_lable')
        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
    def face_problem(self):
        self.ui()
        self.right_recommend_label = QtWidgets.QLabel("1.若您点击\"实时数据\"按钮，此时软件系统正在网上爬取信息，在短时间内点击系统无反馈属于正常现象。\n2.生成\"课程报告\"需要一定的时间，请耐心等待。\n3.data文件夹下储存有您的往期数据，您查看课程的变化趋势时与之密切相关。\n若您有其它问题，请及时通知我们，我们将第一时间为您解决。\n联系电话:\n小助手1:18856359800\n小助手2:18856301011\n小助手3:17356379709\n我们随时欢迎您来电咨询。")
        self.right_recommend_label.setObjectName('right_lable')
        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
    def predict(self):
        self.ui()
        self.label1 = QtWidgets.QLabel("课程名称:")
        self.label1.setObjectName('right_lable')
        self.right_layout.addWidget(self.label1, 1, 3, 1, 3)
        self.text1 = QtWidgets.QLineEdit()
        self.text1.setPlaceholderText("若您想要开设新课程，请在这里输入该课程名称")
        self.text1.setObjectName('right_lable')
        self.right_layout.addWidget(self.text1, 1, 4, 1, 4)
        
        self.label2 = QtWidgets.QLabel("课程描述:")
        self.label2.setObjectName('right_lable')
        self.right_layout.addWidget(self.label2, 2, 3, 1, 3)
        self.text2 = QtWidgets.QLineEdit()
        self.text2.setPlaceholderText("请输入课程描述页的内容")
        self.text2.setObjectName('right_lable')
        self.right_layout.addWidget(self.text2, 2, 4, 1, 7)
        
        self.label3 = QtWidgets.QLabel("课程作者:")
        self.label3.setObjectName('right_lable')
        self.right_layout.addWidget(self.label3, 3, 3, 1, 3)
        self.text3 = QtWidgets.QLineEdit()
        self.text3.setPlaceholderText("请输入课程提供者")
        self.text3.setObjectName('right_lable')
        self.right_layout.addWidget(self.text3, 3, 4, 1, 3)
        
        self.label4 = QtWidgets.QLabel("课程原价:")
        self.label4.setObjectName('right_lable')
        self.right_layout.addWidget(self.label4, 4, 3, 1, 3)
        self.text4 = QtWidgets.QLineEdit()
        self.text4.setPlaceholderText("请输入初始价格，仅数字")
        self.text4.setObjectName('right_lable')
        self.right_layout.addWidget(self.text4, 4, 4, 1, 2)
        
        self.label5 = QtWidgets.QLabel("折扣价:")
        self.label5.setObjectName('right_lable')
        self.right_layout.addWidget(self.label5, 5, 3, 1, 3)
        self.text5 = QtWidgets.QLineEdit()
        self.text5.setPlaceholderText("请输入课程折后价，仅数字")
        self.text5.setObjectName('right_lable')
        self.right_layout.addWidget(self.text5, 5, 4, 1, 2)
        
        self.sure= QtWidgets.QPushButton()
        self.sure.setText("确定")
        self.sure.clicked.connect(lambda :self.certain())
        self.right_layout.addWidget(self.sure, 6, 4, 1, 1)
    def certain(self):
        try:
            self.root.destroy()
        except:
            pass
        try:
            message=np.array([self.text1.text(),self.text2.text(),self.text3.text(),float(self.text4.text()),float(self.text5.text())])
            learners,revenue,stars=course_forecasting(self.data,message,self.steps)
            self.root = tk.Tk()  
            w=self.root.winfo_screenwidth()
            h=self.root.winfo_screenheight()
            x = (w-320) / 2
            y = (h-200) / 2
            self.root.geometry("320x200+{}+{}".format(int(x),int(y)))
            self.root.title("预测结果")
            self.root.resizable(False, False)
            text = tk.Text(self.root,font=('华文隶书', 14, "normal"))
            text.pack(anchor='center')
            text.insert("insert", "预测您新开设课程最终情况为\n学习人数:%d人\n总收入:%d元\n评分:%.2f分"%(abs(int(learners)),abs(int(revenue)),abs(stars)))
            self.steps=1
            self.root.mainloop()
        except:
            QMessageBox.information(None, "提示", "预测失败，可能是您输入格式错误！", QMessageBox.Yes)
    def closeEvent(self, event):
        sys.exit(0)
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()