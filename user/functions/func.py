import pymysql
# 这个函数的作用是对数据库里的id重新排序

#输入参数为cursor（游标）
def IdSort(db,cursor):#输入参数为db和cursor
    sql = "select count(*) from mission_published"
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    for i in range(0,result):
        sql = 'select id from mission_published limit {},1'.format(i)
        cursor.execute(sql)
        id = cursor.fetchone()[0]# 得到本行的id
        if (id != i+1):
            sql1 = 'update mission_published set id={} where id ={}'.format(i+1,id)
            cursor.execute(sql1)
            db.commit()
