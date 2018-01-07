# -*- coding: utf-8 -*-

#   库的引用1
from tkinter import *
import pymysql
from tkinter.scrolledtext import ScrolledText
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import ImageTk

#   库的引用2
import tool
import data2csv

#   全局变量定义
global nowidnumber
global nowpermission

#   变量的约束性条件定义
IdMaxLength = 20
PassMaxLength = 20
NameMaxLength = 20
PlaceMaxLength = 40
BriefMaxLength = 50
DetailMaxLength = 255

#   连接到数据库
conn = pymysql.connect(host='localhost', user='root', passwd='447329', db='flss',use_unicode=True, charset="utf8")
cur = conn.cursor()

#   绘图库相关设置，设计颜色以及允许使用中文
sns.set(color_codes=True)
plt.rcParams['font.sans-serif'] = ['SimHei']

#   绘制失物种类统计图。图形类型为饼状图。
def DrawThingTable():
    data = tool.GetThingCountTable(cur)
    datalist = []
    countlist = []
    for line in data:
        datalist.append(line[0])
        countlist.append(line[1])
    plt.axis('equal')
    plt.pie(countlist, labels=datalist, autopct='%1.1f%%')
    plt.title('失物种类统计图')
    plt.show()

#   绘制失物情况统计图。图形类型为条形图。
def DrawDateTable():
    data = tool.GetDateCountTable(cur)
    datalist=[]
    countlist=[]
    for line in data:
        for i in range(0, line[1]):
            datalist.append(line[0][:-3])
            if line[0][:-3] not in countlist:
                countlist.append(line[0][:-3])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(datalist, bins=len(countlist)*2-1)
    plt.title('失物情况统计图')
    plt.xlabel('月份')
    plt.ylabel('次数')
    plt.show()

#   普通用户操作界面
def MainWindowForNormalUser():
    def LogOut():
        window.destroy()
    window = Tk()
    window.geometry("190x295")
    window.title("失物寻回系统 For 普通用户")
    Label(window, text="  您好!", font="微软雅黑").grid(row=0, column=0, columnspan=2)
    k = tool.Id2Name(cur, nowidnumber)
    Label(window, text=" ").grid(row=1)
    Label(window, text=k).grid(row=2, column=1, columnspan=2)
    Label(window, text=" ").grid(row=3)
    Button(window, text="      失物查询      ", command=LostSearch, font="微软雅黑").grid(row=4, column=1, columnspan=2)
    Label(window, text=" ").grid(row=5)
    Button(window, text=" 失物招领处查询 ", command=AllLostAndFound, font="微软雅黑").grid(row=6, column=1, columnspan=2)
    Label(window, text=" ").grid(row=7)
    Button(window, text="          退出          ", command=LogOut, font="微软雅黑").grid(row=8, column=1, columnspan=2)
    window.mainloop()

#   失物招领处操作界面
def MainWindowForLostAndFound():
    def LogOut():
        window.destroy()
    window = Tk()
    window.geometry("220x365")
    window.title("失物寻回系统 For 失物招领处")
    Label(window, text=" 您好!",font="微软雅黑").grid(row=0,column=0,columnspan=2)
    Label(window, text=" ").grid(row=1)
    k=tool.Id2Name(cur, nowidnumber)
    Label(window, text=k).grid(row=2,column=1,columnspan=2)
    Label(window, text=" ").grid(row=3)
    Button(window, text="失物查询",font="微软雅黑", command=LostSearch).grid(row=4,column=1)
    Button(window, text="失物管理",font="微软雅黑", command=LostManage).grid(row=4,column=2)
    Label(window, text=" ").grid(row=5)
    Button(window, text="查看失物情况统计图",font="微软雅黑", command=DrawDateTable).grid(row=6,column=1,columnspan=2)
    Label(window, text=" ").grid(row=7)
    Button(window, text="查看失物种类统计图",font="微软雅黑", command=DrawThingTable).grid(row=8,column=1,columnspan=2)
    Label(window, text=" ").grid(row=9)
    Button(window, text="          退出          ", command=LogOut, font="微软雅黑").grid(row=10, column=1, columnspan=2)

    window.mainloop()

#   普通用户注册
def RegisterNormalUser():
    Reg = Toplevel()
    Reg.geometry("300x180")
    Reg.title("注册")

    # “确认提交”对应的判定和创建账号操作
    def RegisterJudge():

        # 对一些不规范的注册信息进行回应，不予以注册。
        if len(IdNumberTible.get()) == 0:
            message.set("请输入账号")
            return
        if len(IdNumberTible.get()) > IdMaxLength:
            message.set("账号长度不得超过"+str(IdMaxLength)+"位")
            return
        UserId = IdNumberTible.get()
        if (tool.JudgeUserId(cur, UserId) != 0):
            message.set("该账号已存在")
            return
        if len(NameTible.get()) == 0:
            message.set("请输入用户名")
            return
        if len(NameTible.get()) > NameMaxLength:
            message.set("用户名长度不得超过"+str(NameMaxLength)+"位")
            return
        UserName = NameTible.get()
        if (tool.JudgeUserName(cur, UserName) != 0):
            message.set("该用户名已存在")
            return
        if len(PassTible.get()) == 0:
            message.set("请输入密码")
            return
        if len(PassTible.get()) > PassMaxLength:
            message.set("密码长度不得超过"+str(PassMaxLength)+"位")
            return
        if PassTible.get() != RepassTible.get():
            message.set("两次输入的密码不同，请重新输入")
            PassTible.delete(0, len(PassTible.get()))
            RepassTible.delete(0, len(RepassTible.get()))
            return
        UserPass = PassTible.get()
        tool.HandleRegister(conn, cur, UserId, UserPass, 1, UserName)
        Reg.destroy()
        # 构建小窗口来提示“注册成功”
        Suc = Tk()
        Suc.title("Successfully!")

        def CloseWindow():
            Suc.destroy()

        Label(Suc, text="注册成功!快去登录您的账号吧!", font="微软雅黑").grid(row=1)
        Close = Button(Suc, text="关闭", command=CloseWindow).grid(row=2)
        Suc.mainloop()

    # “清空信息”对应的文本框清空操作。
    def RegisterClear():
        IdNumberTible.delete(0, len(IdNumberTible.get()))
        NameTible.delete(0, len(NameTible.get()))
        PassTible.delete(0, len(PassTible.get()))
        RepassTible.delete(0, len(RepassTible.get()))

    # 设置GUI的文本显示和按钮等组件，并采用grid进行布局
    Label(Reg, text="请填写如下信息，完成注册操作", font='微软雅黑').grid(row=1, column=1, columnspan=3)
    Label(Reg, text="　请输入您的账号：").grid(row=2, column=1)
    IdNumberTible = Entry(Reg)
    IdNumberTible.grid(row=2, column=2, columnspan=3)
    Label(Reg, text="　请输入您的用户名：").grid(row=3, column=1)
    NameTible = Entry(Reg)
    NameTible.grid(row=3, column=2, columnspan=3)
    Label(Reg, text="　请输入您的密码：").grid(row=4, column=1)
    PassTible = Entry(Reg, show='*')
    PassTible.grid(row=4, column=2, columnspan=3)
    Label(Reg, text="　请再次输入密码：").grid(row=5, column=1)
    RepassTible = Entry(Reg, show='*')
    RepassTible.grid(row=5, column=2, columnspan=3)
    Submit = Button(Reg, text=" 确认提交 ", command=RegisterJudge).grid(row=6, column=2)
    Clear = Button(Reg, text=" 清空信息 ", command=RegisterClear).grid(row=6, column=3)
    message = StringVar();
    message.set("*账号、密码以及用户名的长度不能超过20位")
    Warm = Label(Reg, textvariable = message ,width=40)
    Warm.grid(row=7, column=1, columnspan=3)

    Reg.mainloop()

#   失物招领处注册
def RegisterLostAndFound():
    Reg = Toplevel()
    Reg.geometry("380x180")
    Reg.title("注册")

    # “确认提交”对应的判定和创建账号操作
    def RegisterJudge():

        # 对一些不规范的注册信息进行回应，不予以注册。
        if len(IdNumberTible.get()) == 0:
            message.set("请输入账号")
            return
        if len(IdNumberTible.get()) > IdMaxLength:
            message.set("账号长度不得超过" + str(IdMaxLength) + "位")
            return
        UserId = IdNumberTible.get()
        if (tool.JudgeUserId(cur, UserId) != 0):
            message.set("该账号已存在")
            return
        if len(NameTible.get()) == 0:
            message.set("请输入地址")
            return
        if len(NameTible.get()) > PlaceMaxLength:
            message.set("地址长度不得超过" + str(PlaceMaxLength) + "位")
            return
        UserName = NameTible.get()
        if (tool.JudgeUserName(cur, UserName) != 0):
            message.set("该地址已存在")
            return
        if len(PassTible.get()) == 0:
            message.set("请输入密码")
            return
        if len(PassTible.get()) > PassMaxLength:
            message.set("密码长度不得超过" + str(PassMaxLength) + "位")
            return
        if PassTible.get() != RepassTible.get():
            message.set("两次输入的密码不同，请重新输入")
            PassTible.delete(0, len(PassTible.get()))
            RepassTible.delete(0, len(RepassTible.get()))
            return
        UserPass = PassTible.get()
        tool.HandleRegister(conn, cur, UserId, UserPass, 2, UserName)
        Reg.destroy()
        # 构建小窗口来提示“注册成功”
        Suc = Tk()
        Suc.title("Successfully!")

        def CloseWindow():
            Suc.destroy()

        Label(Suc, text="注册成功!快去登录您的账号吧!", font="微软雅黑").grid(row=1)
        Close = Button(Suc, text="关闭", command=CloseWindow).grid(row=2)
        Suc.mainloop()

    # “清空信息”对应的文本框清空操作。
    def RegisterClear():
        IdNumberTible.delete(0, len(IdNumberTible.get()))
        NameTible.delete(0, len(NameTible.get()))
        PassTible.delete(0, len(PassTible.get()))
        RepassTible.delete(0, len(RepassTible.get()))
        message.set("*账号、密码的长度不能超过20位，地址的长度不能超过40位")

    # 设置GUI的文本显示和按钮等组件，并采用grid进行布局
    Label(Reg, text="请填写如下信息，完成注册操作", font='微软雅黑').grid(row=1, column=1, columnspan=3)
    Label(Reg, text="　请输入您的账号：").grid(row=2, column=1)
    IdNumberTible = Entry(Reg, width=30)
    IdNumberTible.grid(row=2, column=2, columnspan=3)
    Label(Reg, text="　请输入您的地址：").grid(row=3, column=1)
    NameTible = Entry(Reg, width=30)
    NameTible.grid(row=3, column=2, columnspan=3)
    Label(Reg, text="　请输入您的密码：").grid(row=4, column=1)
    PassTible = Entry(Reg, show='*', width=30)
    PassTible.grid(row=4, column=2, columnspan=3)
    Label(Reg, text="　请再次输入密码：").grid(row=5, column=1)
    RepassTible = Entry(Reg, show='*', width=30)
    RepassTible.grid(row=5, column=2, columnspan=3)
    Clear = Button(Reg, text=" 清空信息 ", command=RegisterClear).grid(row=6, column=1)
    Submit = Button(Reg, text=" 确认提交 ", command=RegisterJudge).grid(row=6, column=3)
    message = StringVar();
    message.set("*账号、密码的长度不能超过20位，地址的长度不能超过40位")
    Warm = Label(Reg, textvariable=message, width=50)
    Warm.grid(row=7, column=1, columnspan=3)

    Reg.mainloop()

#   “注册”界面的构建
def Register():
    def NextStep():
        if (v.get() == 1):
            Select.destroy()
            RegisterNormalUser()
        else:
            Select.destroy()
            RegisterLostAndFound()
        return
    Select = Toplevel()
    Select.geometry("200x100")
    Select.title("选择用户类型")
    Label(Select, text="请选择您的用户类型", font="微软雅黑").grid(row=1, column=1, columnspan=3)
    v = IntVar()
    v.set(1)
    Radiobutton(Select, text="普通用户", variable=v, value=1).grid(row=2, column=1)
    Radiobutton(Select, text="失物招领处", variable=v, value=2).grid(row=2, column=2)
    Button(Select, text="下一步", command=NextStep).grid(row=3, column=2)

#   “登录”界面的构建
def SignIn():
    Sig = Toplevel()
    Sig.geometry("290x140")
    Sig.title("登录")

    # “确认提交”对应的判定和登录操作
    def SignInJudge():

        # 用户名或密码为空，则登录操作不合法
        if len(NameTible.get()) == 0:
            s.set( "请输入账号。")
            return
        if len(PassTible.get()) == 0:
            s.set( "请输入密码。")
            return

        UserName = NameTible.get()
        UserPass = PassTible.get()
        Value = tool.JudgeUserPass(cur, UserName, UserPass)
        if (Value == 0):
            s.set("账号或密码错误。")
            PassTible.delete(0, len(PassTible.get()))
            return
        #登录成功
        global nowidnumber
        nowidnumber = UserName
        global nowpermission
        nowpermission = Value
        Sig.destroy()
        Root.destroy()
        if nowpermission == 1:
            MainWindowForNormalUser()
        elif nowpermission == 2:
            MainWindowForLostAndFound()

    def SignInClear():
        NameTible.delete(0, len(NameTible.get()))
        PassTible.delete(0, len(PassTible.get()))
        s.set("请填写登录信息。")

    Label(Sig, text="登录", font='微软雅黑').grid(row=1, column=1, columnspan=3)
    Label(Sig, text="请输入您的账号：").grid(row=2, column=1)
    #e = StringVar()
    #e.set('input your text here')
    #NameTible = Entry(Sig, textvariable = e)
    NameTible = Entry(Sig)
    NameTible.grid(row=2, column=2, columnspan=3)
    Label(Sig, text="请输入您的密码：").grid(row=3, column=1)
    PassTible = Entry(Sig, show='*')
    PassTible.grid(row=3, column=2, columnspan=3)
    Submit = Button(Sig, text=" 确认提交 ", command=SignInJudge).grid(row=4, column=2)
    Clear = Button(Sig, text=" 清空信息 ", command=SignInClear).grid(row=4, column=3)
    s = StringVar()
    s.set("请填写登录信息。")
    Warm = Label(Sig, textvariable=s, anchor='w', width=40)
    Warm.grid(row=5, column=1, columnspan=3)
    Sig.mainloop()

#   失物查询
def LostSearch():
    LB = Toplevel()
    LB.geometry("1020x380")
    LB.title("查询失物")
    NowTitle = ['物品名称','拾到时间','拾到地点','简要描述','招领处地点']
    global NowData
    global NowPlace
    global NowName
    global NowDate1
    global NowDate2
    NowData = []
    NowName = ''
    NowPlace = ''
    NowDate1 = ''
    NowDate2 = ''

    # 清空多行文本框
    def ClearRes():
        Res.delete(0.0, END)

    # “清空信息”按钮所对应的清空函数
    def Clear():
        ClearRes()
        Place.delete(0, END)
        Name.delete(0, END)
        Year1.delete(0, END)
        Month1.delete(0, END)
        Day1.delete(0, END)
        Year2.delete(0, END)
        Month2.delete(0, END)
        Day2.delete(0, END)
        warm.set("请填写物品名称。")

    # “查询”按钮对应的函数
    def Find():
        global NowData
        global NowPlace
        global NowName
        global NowDate1
        global NowDate2
        if len(Name.get()) == 0:
            warm.set("请填写物品名称。")
            return
        if len(Name.get()) > NameMaxLength:
            warm.set("“物品名称”的长度应该小于等于"+str(NameMaxLength)+"位")
            return
        NowName = Name.get()
        if len(Place.get()) > PlaceMaxLength:
            warm.set("“遗失地点”的长度应该小于等于"+str(PlaceMaxLength)+"位")
            return
        NowPlace = Place.get()
        if len(Year1.get()) > 0 and Year1.get().isdigit() == False:
            warm.set("“遗失时间”应由数字填写")
            return
        if len(Year2.get()) > 0 and Year2.get().isdigit() == False:
            warm.set("“遗失时间”应由数字填写")
            return
        if len(Month1.get()) > 0 and Month1.get().isdigit() == False:
            warm.set("“遗失时间”应由数字填写")
            return
        if len(Month2.get()) > 0 and Month2.get().isdigit() == False:
            warm.set("“遗失时间”应由数字填写")
            return
        if len(Day1.get()) > 0 and Day1.get().isdigit() == False:
            warm.set("“遗失时间”应由数字填写")
            return
        if len(Day2.get()) > 0 and Day2.get().isdigit() == False:
            warm.set("“遗失时间”应由数字填写")
            return
        if len(Year1.get()) > 4 or len(Year2.get()) > 4:
            warm.set("“遗失时间”中，年份最多为4位数字")
            return
        if len(Month1.get()) > 2 or len(Month2.get()) > 2:
            warm.set("“遗失时间”中，月份最多为2位数字")
            return
        if len(Day1.get()) > 2 or len(Day2.get()) > 2:
            warm.set("“遗失时间”中，日期最多为2位数字")
            return
        if len(Year1.get()) > 0 or len(Month1.get()) > 0 or len(Day1.get()) > 0:
            if len(Year1.get()) == 0 or len(Month1.get()) == 0 or len(Day1.get()) == 0:
                warm.set("“遗失时间”的起始日期填写不完整")
                return
            else:
                NowYear = Year1.get()
                NowYear = "0" * (4-len(NowYear)) +  NowYear
                NowMonth = Month1.get()
                NowMonth = "0" * (2 - len(NowMonth)) + NowMonth
                NowDay = Day1.get()
                NowDay = "0" * (2 - len(NowDay)) + NowDay
                NowDate1 = NowYear + "-" + NowMonth + "-" + NowDay
        else:
            NowDate1 = ""
        if len(Year2.get()) > 0 or len(Month2.get()) > 0 or len(Day2.get()) > 0:
            if len(Year2.get()) == 0 or len(Month2.get()) == 0 or len(Day2.get()) == 0:
                warm.set("“遗失时间”的结束日期填写不完整")
                return
            else:
                NowYear = Year2.get()
                NowYear = "0" * (4 - len(NowYear)) + NowYear
                NowMonth = Month2.get()
                NowMonth = "0" * (2 - len(NowMonth)) + NowMonth
                NowDay = Day2.get()
                NowDay = "0" * (2 - len(NowDay)) + NowDay
                NowDate2 = NowYear + "-" + NowMonth + "-" + NowDay
        else:
            NowDate2 = ""
        Res.delete(0.0,END)
        NowData = tool.GetLostMessage(cur, NowName, NowPlace, NowDate1, NowDate2)
        list.sort(NowData, key=lambda everyline: everyline[1], reverse=True)
        for line in NowData:
            content = "物品名称：" + line[0] + "\t" + "拾到时间：" + line[1] + "\t" + "拾到地点：" + line[2] + "\t"
            content = content + "招领处地点：" + line[4] + "\t"
            if (len(line[3]) == 0):
                content = content + "简要描述：无" + '\n'
            else:
                content = content + "简要描述：" + line[3] + '\n'
            Res.insert(0.0,content)
        warm.set("共查询到 " + str(len(NowData)) + " 条失物信息")

    def PrintOut():
        global NowData
        global NowPlace
        global NowName
        global NowDate1
        global NowDate2
        NowData = tool.GetLostMessage(cur, NowName, NowPlace, NowDate1, NowDate2)
        list.sort(NowData, key=lambda everyline: everyline[1], reverse=True)
        data2csv.printf("失物信息", NowTitle, NowData)

    # 失物查询的GUI界面
    Label(LB, text="失物信息", font="微软雅黑").grid(row=0, column=1, columnspan=7)
    Label(LB, text="物品名称", font="微软雅黑").grid(row=1, column=1)
    Name = Entry(LB, width = 25)
    Name.grid(row=1, column=2, columnspan=7)
    Label(LB, text="遗失地点", font="微软雅黑").grid(row=2, column=1)
    Place = Entry(LB, width = 25)
    Place.grid(row=2, column=2, columnspan=7)
    Label(LB, text="遗失时间", font="微软雅黑").grid(row=3, column=1)
    Year1 = Entry(LB, width=8)
    Year1.grid(row=3, column=2)
    Label(LB, text="年").grid(row=3, column=3)
    Month1 = Entry(LB, width=4)
    Month1.grid(row=3, column=4)
    Label(LB, text="月").grid(row=3, column=5)
    Day1 = Entry(LB, width=4)
    Day1.grid(row=3, column=6)
    Label(LB, text="日   ").grid(row=3, column=7)
    Label(LB, text="至", font="微软雅黑").grid(row=4, column=1)
    Year2 = Entry(LB, width=8)
    Year2.grid(row=4, column=2)
    Label(LB, text="年").grid(row=4, column=3)
    Month2 = Entry(LB, width=4)
    Month2.grid(row=4, column=4)
    Label(LB, text="月").grid(row=4, column=5)
    Day2 = Entry(LB, width=4)
    Day2.grid(row=4, column=6)
    Label(LB, text="日   ").grid(row=4, column=7)
    Label(LB, text="注1：“物品名称”长度不得超过"+str(NameMaxLength)+"。").grid(row=5, column=1, columnspan=7)
    Label(LB, text="注2：“遗失地点”长度不得超过"+str(PlaceMaxLength)+"。").grid(row=6, column=1, columnspan=7)
    Label(LB, text="注3：对于“遗失时间”,请填写数字。").grid(row=7, column=1, columnspan=7)
    Button1 = Button(LB, text='导出结果', font="微软雅黑", command=PrintOut).grid(row=8, column=1, columnspan=1)
    Button2 = Button(LB, text='查询', font="微软雅黑", command=Find).grid(row=8, column=2, columnspan=3)
    Button3 = Button(LB, text='清空', font="微软雅黑", command=Clear).grid(row=8, column=4, columnspan=5)
    warm=StringVar()
    warm.set("请填写遗失物品的名称")
    Label(LB, textvariable=warm).grid(row=9, column=1, columnspan=7)
    Label(LB, text="查询结果", font="微软雅黑").grid(row=0, column=10, columnspan=10)
    Res = ScrolledText(LB, width = 100)
    Res.grid(row=1, column=10, columnspan=10, rowspan=9)
    LB.mainloop()

#   失物招领处查询
def AllLostAndFound():
    def message2string():
        placelist = tool.GetAllLostAndFound(cur)
        res = ""
        for i in placelist:
            res = res + i + "\n"
        return res
    def getFresh():
        s.set("共有   " + str(len(tool.GetAllLostAndFound(cur))) + "   处失物招领处   ")
        t.delete(0.0, END)
        t.insert(0.0, message2string())
    def getTable():
        getFresh()
        title = ['序号', '失物招领处地址']
        content = []
        message = tool.GetAllLostAndFound(cur)
        cnt = 1
        for line in message:
            content.append((str(cnt),line))
            cnt = cnt + 1
        data2csv.printf("失物招领处地址", title, content)
    window = Toplevel()
    window.geometry('305x360')
    window.title("失物招领处地址")
    s=StringVar()
    s.set("共有   "+str(len(tool.GetAllLostAndFound(cur)))+"   处失物招领处   ")
    Label(window, textvariable=s, font="微软雅黑").grid(row=1, column=1)
    Button(window, text="导出", command=getTable).grid(row=1, column=2)
    Button(window, text="刷新", command = getFresh).grid(row=1, column=3)
    t = ScrolledText(window, width= 40, background='#ffffff')
    t.grid(row=2, column=1,columnspan=3)
    t.insert(0.0,message2string())

#   失物信息管理
def LostManage():
    global nowidnumbers
    window = Toplevel()
    window.title("失物管理")
    window.geometry("1175x400")

    global message
    message = tool.GetLostMessageForLostAndFound(cur, nowidnumber)
    showlist = []
    for i in range(0,10):
        showlist.append(StringVar())
    showlistwidth = 150

    global messagenum
    messagenum = len(message)
    list.sort(message, key=lambda everyline: everyline[1], reverse=True)
    global firstnum
    firstnum = 0
    nowpagecnt = StringVar()
    nowpagecnt.set("第1页")
    totpagecnt = StringVar()
    if (messagenum == 0):
        totpagecnt.set("共1页")
    else:
        totpagecnt.set("共"+str((messagenum-1)//10+1)+"页")
    global off
    off = 0
    NowTitle = ['物品名称', '拾到时间', '拾到地点', '简要描述', '详细描述']
    #print(message)

    def freshcontent():
        global message
        global messagenum
        for i in range(0, 10):
            nowstring = "序号：" + str(i+1) + "\t"
            nownumber = i + firstnum
            if (nownumber <messagenum):
                nowstring = nowstring + "物品名称：" + message[nownumber][0] + "\t拾到时间：" + message[nownumber][1] + "\t拾到地点：" + message[nownumber][2] + "\t简要描述：" +message[nownumber][3]
            showlist[i].set(nowstring)
        nowpagecnt.set("第"+str(firstnum//10+1)+"页")

    def fresh():
        global message
        global messagenum
        message = tool.GetLostMessageForLostAndFound(cur, nowidnumber)
        global messagenum
        messagenum = len(message)
        global firstnum
        firstnum = 0
        nowpagecnt = StringVar()
        nowpagecnt.set("第1页")
        totpagecnt = StringVar()
        if (messagenum == 0):
            totpagecnt.set("共1页")
        else:
            totpagecnt.set("共" + str((messagenum - 1) // 10 + 1) + "页")
        list.sort(message, key=lambda everyline: everyline[1], reverse=True)
        freshcontent()

    def lastpage():
        global firstnum
        if (firstnum < 10):
            return
        firstnum = firstnum - 10
        freshcontent()

    def nextpage():
        global firstnum
        if (firstnum + 10 >= messagenum):
            return
        firstnum = firstnum + 10
        freshcontent()

    def seedetail1():
        global off
        off = 1
        seedetail()

    def seedetail2():
        global off
        off = 2
        seedetail()

    def seedetail3():
        global off
        off = 3
        seedetail()

    def seedetail4():
        global off
        off = 4
        seedetail()

    def seedetail5():
        global off
        off = 5
        seedetail()

    def seedetail6():
        global off
        off = 6
        seedetail()

    def seedetail7():
        global off
        off = 7
        seedetail()

    def seedetail8():
        global off
        off = 8
        seedetail()

    def seedetail9():
        global off
        off = 9
        seedetail()

    def seedetail10():
        global off
        off = 10
        seedetail()

    def delete1():
        global off
        off = 1
        deleterecord()

    def delete2():
        global off
        off = 2
        deleterecord()

    def delete3():
        global off
        off = 3
        deleterecord()

    def delete4():
        global off
        off = 4
        deleterecord()

    def delete5():
        global off
        off = 5
        deleterecord()

    def delete6():
        global off
        off = 6
        deleterecord()

    def delete7():
        global off
        off = 7
        deleterecord()

    def delete8():
        global off
        off = 8
        deleterecord()

    def delete9():
        global off
        off = 9
        deleterecord()

    def delete10():
        global off
        off = 10
        deleterecord()

    def seedetail():
        global firstnum
        global off
        global ind
        if (firstnum + off - 1 >= len(message)):
            return
        ind = firstnum + off - 1
        newwindow = Toplevel()
        newwindow.title("失物详细信息")
        newwindow.geometry("600x370")
        windowwidth=80
        s_name = StringVar()
        s_time = StringVar()
        s_place = StringVar()
        s_brief = StringVar()
        s_detail = StringVar()

        def closewindow():
            newwindow.destroy()

        def refreshshowmessage():
            global ind
            global message
            global nowidnumber
            message = tool.GetLostMessageForLostAndFound(cur, nowidnumber)
            list.sort(message, key=lambda everyline: everyline[1], reverse=True)
            s_name.set("物品名称：" + message[ind][0])
            s_time.set("拾到时间：" + message[ind][1])
            s_place.set("拾到地点：" + message[ind][2])
            s1 = "简要描述："
            nowind = 0
            while nowind < len(message[ind][3]):
                s1 = s1 + "\n" + message[ind][3][nowind:min(nowind + 40, len(message[ind][3]))]
                nowind = nowind + 40
            s_brief.set(s1)
            s2 = "详细描述："
            if message[ind][4] is None or len(message[ind][4]) == 0:
                s2 = s2 + "\n无"
            else:
                nowind = 0
                while nowind < len(message[ind][4]):
                    s2 = s2 + "\n" + message[ind][4][nowind:min(nowind + 40, len(message[ind][4]))]
                    nowind = nowind + 40
            s_detail.set(s2)

        def updatemessage():
            updatewindow = Toplevel()
            updatewindow.title("修改失物信息")
            updatewindow.geometry("285x420")

            def clearentry():
                Name.delete(0, END)
                Place.delete(0, END)
                Year.delete(0, END)
                Month.delete(0, END)
                Day.delete(0, END)
                Brief.delete(0, END)
                Detail.delete(0.0, END)
                warm.set("请修改遗失物品的相关信息。")

            def commitrecord():
                if len(Name.get()) == 0:
                    warm.set("请填写物品名称。")
                    return
                if len(Name.get()) > NameMaxLength:
                    warm.set("“物品名称”的长度应该小于等于" + str(NameMaxLength) + "位。")
                    return
                NowName = Name.get()
                if len(Place.get()) == 0:
                    warm.set("请填写拾到地点。")
                    return
                if len(Place.get()) > PlaceMaxLength:
                    warm.set("“拾到地点”的长度应该小于等于" + str(PlaceMaxLength) + "位。")
                    return
                NowPlace = Place.get()
                if len(Year.get()) == 0 or len(Month.get()) == 0 or len(Day.get()) == 0:
                    warm.set("请将“拾到时间”填写完整。")
                if len(Year.get()) > 0 and Year.get().isdigit() == False:
                    warm.set("“拾到时间”应由数字填写。")
                    return
                if len(Month.get()) > 0 and Month.get().isdigit() == False:
                    warm.set("“拾到时间”应由数字填写。")
                    return
                if len(Day.get()) > 0 and Day.get().isdigit() == False:
                    warm.set("“拾到时间”应由数字填写。")
                    return
                if len(Year.get()) > 4:
                    warm.set("“拾到时间”中，年份最多为4位数字。")
                    return
                if len(Month.get()) > 2:
                    warm.set("“拾到时间”中，月份最多为2位数字。")
                    return
                if len(Day.get()) > 2:
                    warm.set("“拾到时间”中，日期最多为2位数字。")
                    return
                NowYear = Year.get()
                NowYear = "0" * (4 - len(NowYear)) + NowYear
                NowMonth = Month.get()
                NowMonth = "0" * (2 - len(NowMonth)) + NowMonth
                NowDay = Day.get()
                NowDay = "0" * (2 - len(NowDay)) + NowDay
                NowDate = NowYear + "-" + NowMonth + "-" + NowDay
                if len(Brief.get()) > BriefMaxLength:
                    warm.set("“简要描述”的长度不得超过" + str(BriefMaxLength) + "位。")
                    return
                NowBrief = Brief.get()
                if (len(Detail.get(0.0, END)) > DetailMaxLength):
                    warm.set("“详细描述”的长度不得超过" + str(DetailMaxLength) + "位。")
                    return
                NowDetail = Detail.get(0.0, END)
                global ind
                tool.UpdateRecord(conn, cur, message[ind][5], NowName, NowDate, NowPlace, NowBrief, NowDetail)
                refreshshowmessage()
                fresh()
                updatewindow.destroy()

            Label(updatewindow, text="失物信息", font="微软雅黑").grid(row=0, column=1, columnspan=7)
            Label(updatewindow, text="物品名称", font="微软雅黑").grid(row=1, column=1)
            Name = Entry(updatewindow, width=25)
            Name.grid(row=1, column=2, columnspan=7)
            Name.insert(1,message[ind][0])
            Label(updatewindow, text="-“物品名称”不得为空，且长度不得超过" + str(NameMaxLength) + "。").grid(row=2, column=1, columnspan=7)
            Label(updatewindow, text="拾到地点", font="微软雅黑").grid(row=3, column=1)
            Place = Entry(updatewindow, width=25)
            Place.grid(row=3, column=2, columnspan=7)
            Place.insert(1, message[ind][2])
            Label(updatewindow, text="-“拾到地点”不得为空，且长度不得超过" + str(PlaceMaxLength) + "。").grid(row=4, column=1, columnspan=7)
            Label(updatewindow, text="拾到时间", font="微软雅黑").grid(row=5, column=1)
            Year = Entry(updatewindow, width=8)
            Year.grid(row=5, column=2)
            Year.insert(1,message[ind][1][0:4])
            Label(updatewindow, text="年").grid(row=5, column=3)
            Month = Entry(updatewindow, width=4)
            Month.grid(row=5, column=4)
            Month.insert(1, message[ind][1][5:7])
            Label(updatewindow, text="月").grid(row=5, column=5)
            Day = Entry(updatewindow, width=4)
            Day.grid(row=5, column=6)
            Day.insert(1, message[ind][1][8:])
            Label(updatewindow, text="日   ").grid(row=5, column=7)
            Label(updatewindow, text="-“拾到时间”不得为空，且请填写数字。").grid(row=6, column=1, columnspan=7)
            Label(updatewindow, text="简要描述", font="微软雅黑").grid(row=7, column=1)
            Brief = Entry(updatewindow, width=25)
            Brief.grid(row=7, column=2, columnspan=7)
            Brief.insert(1, message[ind][3])
            Label(updatewindow, text="-“简要描述”长度不得超过" + str(BriefMaxLength) + "。").grid(row=8, column=1, columnspan=7)
            Label(updatewindow, text="详细描述", font="微软雅黑").grid(row=9, column=1)
            Detail = ScrolledText(updatewindow, width=25, height=5, background='#ffffff')
            Detail.grid(row=9, column=2, columnspan=7)
            if (message[ind][4] is not None):
                Detail.insert(0.0, message[ind][4])
            Label(updatewindow, text="-“详细描述”长度不得超过" + str(DetailMaxLength) + "。").grid(row=10, column=1, columnspan=7)
            Button(updatewindow, text='确定', font="微软雅黑", command=commitrecord).grid(row=11, column=2, columnspan=3)
            Button(updatewindow, text='清空', font="微软雅黑", command=clearentry).grid(row=11, column=4, columnspan=5)
            warm = StringVar()
            warm.set("请修改遗失物品的相关信息。")
            Label(updatewindow, textvariable=warm).grid(row=12, column=1, columnspan=7)

        Label(newwindow, text="失物详细信息", font='微软雅黑').grid(row=1, column=1, columnspan=4)
        Label(newwindow, textvariable=s_name, anchor = 'w', width=windowwidth).grid(row=2, column=1, columnspan=4)
        Label(newwindow, textvariable=s_time, anchor = 'w', width=windowwidth).grid(row=3, column=1, columnspan=4)
        Label(newwindow, textvariable=s_place, anchor = 'w', width=windowwidth).grid(row=4, column=1, columnspan=4)
        Label(newwindow, textvariable=s_brief, width=windowwidth,  anchor = 'w',justify = 'left').grid(row=5, column=1, columnspan=4)
        Label(newwindow, textvariable=s_detail, width=windowwidth,  anchor = 'w',justify = 'left').grid(row=6, column=1, columnspan=4)
        Label(newwindow, text="                       ").grid(row=7, column=5)
        refreshshowmessage()

        Button(newwindow, text="   修改   ", command=updatemessage).grid(row=7, column=2)
        Button(newwindow, text="   确定   ", command=closewindow).grid(row=7, column=3)
        Label(newwindow, text="                       ").grid(row=7, column=4)

    def deleterecord():
        global firstnum
        global off
        if (firstnum + off - 1 >= len(message)):
            return
        nowmessageid = message[firstnum + off - 1][-1]
        tool.DeleteMessageForLostAndFound(conn, cur, nowmessageid)
        fresh()

    def addrecord():
        addwindow=Toplevel()
        addwindow.title("添加失物信息")
        addwindow.geometry("285x420")

        def clearentry():
            Name.delete(0,END)
            Place.delete(0, END)
            Year.delete(0, END)
            Month.delete(0, END)
            Day.delete(0, END)
            Brief.delete(0, END)
            Detail.delete(0.0, END)
            warm.set("请填写遗失物品的相关信息。")

        def commitrecord():
            if len(Name.get()) == 0:
                warm.set("请填写物品名称。")
                return
            if len(Name.get()) > NameMaxLength:
                warm.set("“物品名称”的长度应该小于等于" + str(NameMaxLength) + "位。")
                return
            NowName = Name.get()
            if len(Place.get()) == 0:
                warm.set("请填写拾到地点。")
                return
            if len(Place.get()) > PlaceMaxLength:
                warm.set("“拾到地点”的长度应该小于等于" + str(PlaceMaxLength) + "位。")
                return
            NowPlace = Place.get()
            if len(Year.get())==0 or len(Month.get())==0 or len(Day.get())==0:
                warm.set("请将“拾到时间”填写完整。")
            if len(Year.get()) > 0 and Year.get().isdigit() == False:
                warm.set("“拾到时间”应由数字填写。")
                return
            if len(Month.get()) > 0 and Month.get().isdigit() == False:
                warm.set("“拾到时间”应由数字填写。")
                return
            if len(Day.get()) > 0 and Day.get().isdigit() == False:
                warm.set("“拾到时间”应由数字填写。")
                return
            if len(Year.get()) > 4:
                warm.set("“拾到时间”中，年份最多为4位数字。")
                return
            if len(Month.get()) > 2:
                warm.set("“拾到时间”中，月份最多为2位数字。")
                return
            if len(Day.get()) > 2:
                warm.set("“拾到时间”中，日期最多为2位数字。")
                return
            NowYear = Year.get()
            NowYear = "0" * (4 - len(NowYear)) + NowYear
            NowMonth = Month.get()
            NowMonth = "0" * (2 - len(NowMonth)) + NowMonth
            NowDay = Day.get()
            NowDay = "0" * (2 - len(NowDay)) + NowDay
            NowDate = NowYear + "-" + NowMonth + "-" + NowDay
            if len(Brief.get()) > BriefMaxLength:
                warm.set("“简要描述”的长度不得超过" + str(BriefMaxLength) + "位。")
                return
            NowBrief = Brief.get()
            if (len(Detail.get(0.0,END)) > DetailMaxLength):
                warm.set("“详细描述”的长度不得超过" + str(DetailMaxLength) + "位。")
                return
            NowDetail = Detail.get(0.0,END)
            tool.HandleRecord(conn, cur, NowName, NowDate, NowPlace, NowBrief, NowDetail, nowidnumber)
            fresh()
            addwindow.destroy()

        Label(addwindow, text="失物信息", font="微软雅黑").grid(row=0, column=1, columnspan=7)
        Label(addwindow, text="物品名称", font="微软雅黑").grid(row=1, column=1)
        Name = Entry(addwindow, width=25)
        Name.grid(row=1, column=2, columnspan=7)
        Label(addwindow, text="-“物品名称”不得为空，且长度不得超过" + str(NameMaxLength) + "。").grid(row=2, column=1, columnspan=7)
        Label(addwindow, text="拾到地点", font="微软雅黑").grid(row=3, column=1)
        Place = Entry(addwindow, width=25)
        Place.grid(row=3, column=2, columnspan=7)
        Label(addwindow, text="-“拾到地点”不得为空，且长度不得超过" + str(PlaceMaxLength) + "。").grid(row=4, column=1, columnspan=7)
        Label(addwindow, text="拾到时间", font="微软雅黑").grid(row=5, column=1)
        Year = Entry(addwindow, width=8)
        Year.grid(row=5, column=2)
        Label(addwindow, text="年").grid(row=5, column=3)
        Month = Entry(addwindow, width=4)
        Month.grid(row=5, column=4)
        Label(addwindow, text="月").grid(row=5, column=5)
        Day = Entry(addwindow, width=4)
        Day.grid(row=5, column=6)
        Label(addwindow, text="日   ").grid(row=5, column=7)
        Label(addwindow, text="-“拾到时间”不得为空，且请填写数字。").grid(row=6, column=1, columnspan=7)
        Label(addwindow, text="简要描述", font="微软雅黑").grid(row=7, column=1)
        Brief = Entry(addwindow, width=25)
        Brief.grid(row=7, column=2, columnspan=7)
        Label(addwindow, text="-“简要描述”长度不得超过" + str(BriefMaxLength) + "。").grid(row=8, column=1, columnspan=7)
        Label(addwindow, text="详细描述", font="微软雅黑").grid(row=9, column=1)
        Detail = ScrolledText(addwindow, width=25, height=5, background='#ffffff')
        Detail.grid(row=9, column=2, columnspan=7)
        Label(addwindow, text="-“详细描述”长度不得超过" + str(DetailMaxLength) + "。").grid(row=10, column=1, columnspan=7)
        Button(addwindow, text='确定', font="微软雅黑", command=commitrecord).grid(row=11, column=2, columnspan=3)
        Button(addwindow, text='清空', font="微软雅黑", command=clearentry).grid(row=11, column=4, columnspan=5)
        warm = StringVar()
        warm.set("请填写遗失物品的相关信息。")
        Label(addwindow, textvariable=warm).grid(row=12, column=1, columnspan=7)

    def PrintOut():
        content = tool.GetLostMessageForLostAndFound(cur, nowidnumber)
        list.sort(content, key=lambda everyline: everyline[1], reverse=True)
        NowData = []
        for line in content:
            NowData.append(line[:-1])
        print(content)
        print(NowData)
        data2csv.printf("本招领处登记的所有失物信息", NowTitle, NowData)

    Label(window, text="失物信息管理", font='微软雅黑').grid(row=1, column=1, columnspan=8)
    Button(window, text="添加记录", command=addrecord).grid(row=1,column=9)
    Button(window, text="导出记录", command=PrintOut).grid(row=1,column=10)
    Button(window, text="   刷新   ", command=fresh).grid(row=2, column=10)
    for i in range(0,10):
        Label(window, textvariable=showlist[i], width=showlistwidth, anchor = 'w').grid(row=3+i,column=1, columnspan=8)

    Button(window, text="查看详情", command=seedetail1).grid(row=3, column=9)
    Button(window, text="删除记录", command=delete1).grid(row=3, column=10)
    Button(window, text="查看详情", command=seedetail2).grid(row=4, column=9)
    Button(window, text="删除记录", command=delete2).grid(row=4, column=10)
    Button(window, text="查看详情", command=seedetail3).grid(row=5, column=9)
    Button(window, text="删除记录", command=delete3).grid(row=5, column=10)
    Button(window, text="查看详情", command=seedetail4).grid(row=6, column=9)
    Button(window, text="删除记录", command=delete4).grid(row=6, column=10)
    Button(window, text="查看详情", command=seedetail5).grid(row=7, column=9)
    Button(window, text="删除记录", command=delete5).grid(row=7, column=10)
    Button(window, text="查看详情", command=seedetail6).grid(row=8, column=9)
    Button(window, text="删除记录", command=delete6).grid(row=8, column=10)
    Button(window, text="查看详情", command=seedetail7).grid(row=9, column=9)
    Button(window, text="删除记录", command=delete7).grid(row=9, column=10)
    Button(window, text="查看详情", command=seedetail8).grid(row=10, column=9)
    Button(window, text="删除记录", command=delete8).grid(row=10, column=10)
    Button(window, text="查看详情", command=seedetail9).grid(row=11, column=9)
    Button(window, text="删除记录", command=delete9).grid(row=11, column=10)
    Button(window, text="查看详情", command=seedetail10).grid(row=12, column=9)
    Button(window, text="删除记录", command=delete10).grid(row=12, column=10)
    Button(window, text="上一页", command=lastpage).grid(row=13, column=3)
    Label(window, textvariable=nowpagecnt).grid(row=13,column=4)
    Label(window, textvariable=totpagecnt).grid(row=13,column=5)
    Button(window, text="下一页", command=nextpage).grid(row=13, column=6)
    freshcontent()

if __name__ == '__main__':
    Root=Tk()
    Root.geometry('432x102')
    Root.title("高校失物寻回系统")

    Img = ImageTk.PhotoImage(file='logo1.jpg')
    background = Label(Root, image=Img).grid(row=1, column=0, rowspan=2)

    Label(Root, text="欢迎使用高校失物寻回系统", font='微软雅黑').grid(row=1, column=1, columnspan=4)
    #Label(Root, text="　　", font='微软雅黑').grid(row=2, column=1, columnspan=2)
    Button1 = Button(Root, text="　点击登录　", font='微软雅黑', command=SignIn).grid(row=2, column=3)
    Button2 = Button(Root, text="　立即注册　", font='微软雅黑', command=Register).grid(row=2, column=4)

    Root.mainloop()

