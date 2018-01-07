# -*- coding: utf-8 -*-
import pymysql

# 返回账户表中账号为userid的账户个数
def JudgeUserId(cur, userid):
    cur.execute("select COUNT(账号) from 账户 where 账号 = '" + userid + "';");
    number = int(cur.fetchall()[0][0])
    return number

# 返回普通用户表中用户名为username的账户个数
def JudgeUserName(cur, username):
    cur.execute("select COUNT(用户名) from 普通用户 where 用户名 = '" + username + "';");
    number = int(cur.fetchall()[0][0])
    return number

# 处理注册过程
def HandleRegister(db, cur, userid, userpass, userpremission, username):
    cur.callproc('insertuser', args=(userid, userpass, userpremission, username))
    db.commit()

# 处理添加失物记录
def HandleRecord(db, cur, name, time, place, brief, detail, userid):
    cur.callproc('insertrecord', args=(name, time, place, brief, detail, userid))
    db.commit()

# 修改失物记录
def UpdateRecord(db, cur, ind, name, time, place, brief, detail):
    cur.callproc('updaterecord', args=(ind,name, time, place, brief, detail))
    db.commit()

# 根据账户表判断账号和密码是否匹配，若匹配输出权限，若不匹配输出0
def JudgeUserPass(cur, userid, userpass):
    cur.execute("select 密码,权限 from 账户 where 账号 = '" + userid + "';");
    message = cur.fetchall();
    if (len(message)==0):
        return(0)
    elif (userpass == message[0][0]):
        return(int(message[0][1]))
    else:
        return(0)

# 返回所有招领处地点，返回值为一个list
def GetAllLostAndFound(cur):
    cur.execute("select 招领处地点 from 失物招领处;")
    res = []
    message = cur.fetchall()
    for line in message:
        res.append(line[0])
    return res

# 根据条件，查询失物信息，返回值为list。用于失物查询。
def GetLostMessage(cur, NowName, NowPlace, NowDate1, NowDate2):
    sqlorder = "select 物品名称, 拾到时间, 拾到地点, 简要描述, 招领处地点 from 失物信息 where 物品名称 like '%" + NowName + "%' "
    if (len(NowPlace) > 0):
        sqlorder = sqlorder + "and 拾到地点 like '%" + NowPlace + "%' "
    if (len(NowDate1) > 0):
        sqlorder = sqlorder + "and 拾到时间 >= '" + NowDate1 + "' "
    if (len(NowDate2) > 0):
        sqlorder = sqlorder + "and 拾到时间 <= '" + NowDate2 + "' "
    sqlorder = sqlorder + ";"
    #print(sqlorder)
    cur.execute(sqlorder)
    res = []
    message = cur.fetchall()
    for line in message:
        res.append(line[:])
    #print(res)
    return res

# 根据条件，查询失物信息，返回值为list。用于失物招领处用户查询所管理的所有信息。
def GetLostMessageForLostAndFound(cur, NowId):
    sqlorder = "select 物品名称,拾到时间,拾到地点,简要描述,详细描述,失物编号 from 失物信息 where 招领处地点 = (select 招领处地点 from 失物招领处 where 账号 ='" + NowId + "');"
    cur.execute(sqlorder)
    message = cur.fetchall()
    res = []
    for line in message:
        res.append(line[:])
    return res

# 根据失物信息的编号删除该信息。用于失物招领处用户删除所管理的信息记录。
def DeleteMessageForLostAndFound(db, cur, NowMessageId):
    sqlorder = "delete from 失物信息 where 失物编号 = '" + str(NowMessageId) + "';"
    cur.execute(sqlorder)
    db.commit()

# 取得统计信息，内容为失物信息中的拾到日期和其对应的出现次数。返回值为list。
def GetDateCountTable(cur):
    sqlorder = "select distinct 拾到时间 from 失物信息;"
    cur.execute(sqlorder)
    datelist = cur.fetchall()
    #print(datelist)
    res = []
    for line in datelist:
        sqlorder = "select DateNum('" + line[0] + "');"
        cur.execute(sqlorder)
        number = cur.fetchall()
        res.append(line + number[0])
    list.sort(res, key=lambda everyline: everyline[0], reverse=False)
    return res

# 取得统计信息，内容为失物信息中的物品名称和其对应的出现次数。返回值为list。
def GetThingCountTable(cur):
    sqlorder = "select distinct 物品名称 from 失物信息;"
    cur.execute(sqlorder)
    thinglist = cur.fetchall()
    #print(thinglist)
    res = []
    for line in thinglist:
        sqlorder = "select ThingNum('" + line[0] + "');"
        cur.execute(sqlorder)
        number = cur.fetchall()
        res.append(line + number[0])
    return res

#  取得用户账号对应的用户名（普通用户）或者招领处地点（失物招领处）
def Id2Name(cur, NowId):
    sqlorder = "select Id2Name('" + NowId + "');"
    cur.execute(sqlorder)
    data=cur.fetchall()
    data=data[0][0]
    return data