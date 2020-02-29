import pymysql
import heapq


def file_read(path):

    f = open(path, 'r')
    position = []
    for line in f.readlines():
        lng = line.split(',')[0]
        lat = line.split(',')[1].strip('\n')
        position.append((lng, lat))
    return position


dbparams = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '1234',
            'database': 'ditu',
            'charset': 'utf8'
        }   # 数据库的参数

path_p = 'C:/Users/Wang/Desktop/bdapi/'      # 起始坐标的文件路径
start_point = file_read(path_p + 'start.txt')
end_point = file_read(path_p + 'end.txt')

pos = []
for i in start_point:
    poss = []
    bg = []
    for j in end_point:
        lit = ((float(i[1])-float(j[1]))**2)+((float(i[0])-float(j[0]))**2)  # 起点到终点的距离
        bg.append(lit)
        params = (i[1], i[0], j[1], j[0])  # 起点到终点的坐标元组
        poss.append(params)
    re1 = map(bg.index, heapq.nsmallest(6, bg))  # 起点到终点的距离最小的6个坐标元组的索引
    for b in re1:
        pos.append(poss[b])        # 将距离最小的6个坐标元组添加到总数据表中


# 将结果写入数据库
conn = pymysql.connect(**dbparams)
cur = conn.cursor()  # 获取一个游标
# sql = """insert into result(slng,slat,elng,elat,distance,time) values (%s,%s,%s,%s,%s,%s)"""
sql = """insert into coordinate(slng,slat,elng,elat) values (%s,%s,%s,%s)"""
data = cur.executemany(sql, pos)  # 多条语句插入，
# data = cur.execute(sql,(1,1,151,1,15,1)) #单条插入
conn.commit()  # 提交
print(data)  # 打印返回结果
cur.close()  # 关闭游标
conn.close()  # 关闭连接
