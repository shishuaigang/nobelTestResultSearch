# coding=utf-8
import pymssql
import matplotlib.pyplot as plt
import pylab as pl


class Prepare:
    def __init__(self, bt, et, apiname):
        self.begintime = bt
        self.endtime = et
        self.apiname = apiname

    def sql_sentence(self):  # 拼接sql语句
        pre_condition = "use Inroad_Test_Result select Response_time,TestNo from Nobel_Crawler_Test where "
        condition1 = "API_URL='" + self.apiname + "'"
        condition2 = "TestNo >='" + self.begintime + "'"
        condition3 = "TestNo <='" + self.endtime + "'"
        condition4 = "order by TestNo asc"  # 时间升序进行排列
        SQL = pre_condition + condition1 + " AND " + condition2 + " AND " + condition3 + condition4
        return SQL

    def read_db(self):
        sql = self.sql_sentence()
        res = []
        conn = pymssql.connect(host="192.168.31.99\\sql2012", user="sgshi", password="ssg12345!",
                               database="Inroad_Test_Result")
        cur = conn.cursor()
        print u"连接数据库成功"
        cur.execute(sql)
        for row in cur:
            res.append(row)
        conn.commit()
        cur.close()
        conn.close()
        return res

    def detail(self):
        conn = pymssql.connect(host="192.168.31.99\\sql2012", user="sgshi", password="ssg12345!",
                               database="Inroad_Test_Result")
        cur = conn.cursor()
        cur.execute("use Inroad_Test_Result select distinct TestNo from Nobel_Crawler_Test order by TestNo asc")
        testNo = []
        APIname = []
        for row in cur:
            testNo.append(row[0])
        t1 = {"serial": testNo}
        conn.commit()
        cur.execute("use Inroad_Test_Result select distinct API_URL from Nobel_Crawler_Test")
        for row in cur:
            APIname.append(row[0])
        t2 = {"name": APIname}
        conn.commit()
        cur.close()
        conn.close()
        return {"res": [t1, t2]}

    def create_qushitu(self):
        all_list = self.read_db()
        time_list = [all_list[i][0] for i in range(len(all_list))]
        testNo_list = [all_list[i][1] for i in range(len(all_list))]
        fig, ax = plt.subplots()
        # 设置显示图片的大小
        plt.figure(figsize=(12.8, 8))
        plt.title(self.apiname + '  response time')
        plt.ylabel('Response time  (ms)')
        # 将x的刻度使用其他字符串来代替，x轴刻度30度弯曲
        x = [i for i in range(len(all_list))]
        plt.xticks(x, testNo_list, rotation=30)
        # 绘图
        pl.plot(x, time_list)
        plt.grid(True)
        plt.savefig('qushi.png')
