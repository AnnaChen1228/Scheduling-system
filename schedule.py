import mysql.connector
import math
from random import shuffle

def schedule():
    # 連接到 MySQL
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='anna901228',
        database='human_computer'
    )

    cursor = connection.cursor()

    # 清空排班表
    cursor.execute("UPDATE real_next_week SET id=null where day_id is not null;")
    cursor.execute("UPDATE choose SET is_choose=false where id is not null;")
    # 獲取員工的自主排班意願
    cursor.execute("SELECT* FROM next_week ORDER BY input_time;")
    preferences = cursor.fetchall()


    # 生成排班表
    for preference in preferences:
        id, day_id, time_id, _ = preference
        cursor.execute("SELECT COUNT(*) FROM next_week WHERE day_id = %s AND time_id = %s;", (day_id, time_id))
        count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM next_week WHERE day_id = %s AND id = %s;", (day_id, id))
        same = cursor.fetchone()[0]
        #print(same)
        if same==0:
            if count <= 2:  # 如果班次未滿
                cursor.execute("INSERT INTO real_next_week VALUES (%s, %s, %s);", (id,day_id, time_id))
            elif count > 2:  # 如果班次已滿
                time_count=cursor.execute("SELECT COUNT(*) FROM real_next_week WHERE day_id = %s AND time_id = %s AND id is not null;", (day_id, time_id))
                if time_count<=2:
                    cursor.execute("INSERT INTO real_next_week VALUES (%s, %s, %s);", (id,day_id, time_id))
            #pass

    # 將未滿班次的地方進行隨機排班
    cursor.execute("SELECT day_id, time_id FROM real_next_week WHERE id IS NULL;")
    unfilled_shifts = cursor.fetchall()

    cursor.execute("SELECT id FROM id_pw where id!=0;")
    all_staff = cursor.fetchall()

    #-- 打亂未滿班次的順序，確保隨機分配
    shuffle(unfilled_shifts)
    shuffle(all_staff)
    for day_id, time_id in unfilled_shifts:
        for id_tuple in all_staff:
            id = id_tuple[0]
            cursor.execute("SELECT COUNT(*) FROM real_next_week WHERE day_id = %s AND id = %s;", (day_id, id))
            same = cursor.fetchone()[0]
            #print(same)
            if same==0:#那一天沒有工作
                cursor.execute("SELECT COUNT(*) FROM real_next_week WHERE id = %s;", (id,))#那一週工作的總天數
                id_count = cursor.fetchone()[0]
                
                if id_count < math.ceil(35/len(all_staff)):
                    cursor.execute("UPDATE real_next_week SET id = %s WHERE day_id = %s AND time_id = %s AND id IS NULL LIMIT 1;", (id, day_id, time_id))




    # 提交變更
    connection.commit()
    cursor.execute("TRUNCATE TABLE next_week")
    # 關閉連接
    cursor.close()
    connection.close()
