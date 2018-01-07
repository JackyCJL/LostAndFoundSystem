import random

thingList = ['雨伞','校园卡','钱包','水杯','笔记本','钥匙串','手机'];
placeList = ['田径场','篮球场','足球场','网球场','新主楼','主楼','主楼北楼','主楼南楼']
lostAndFoundPlaceList = ['校内3号学生公寓','校内7号学生公寓','合一食堂3楼','学二食堂']
colorList = ['金色','白色','粉色','黑色','银色','蓝色','紫色']

print(random.randint(0,2));

for T in range(0, 200):
    a = random.randint(0,len(thingList)-1)
    b = random.randint(0,len(placeList)-1)
    c = random.randint(0,len(lostAndFoundPlaceList)-1)
    d = 10 + random.randint(0,2)
    e = random.randint(0,30)
    s = "INSERT INTO 失物信息(物品名称,拾到时间,拾到地点,简要描述,招领处地点) VALUES ("
    s = s + "'" + thingList[a] + "',"
    s = s + "'2017-" + str(d) + "-"
    if (e<10):
        s = s + "0" + str(e)
    else:
        s = s + str(e)
    s = s + "','" + placeList[b]
    if (b > 3):
        f = random.randint(1,5)
        s = s + str(f) + "楼"
    s = s + "','"
    if (a == 1):
        f = random.randint(14000001,17319999)
        s = s + "学号是" + str(f)
    else:
        f = random.randint(0,len(colorList)-1)
        s = s + colorList[f]
    s = s + "','" + lostAndFoundPlaceList[c] + "');"
    print(s)
