import mysql.connector

def update():
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='anna901228',
        database='human_computer'
    )

    cursor = connection.cursor()

    cursor.execute("select id from staff;")
    all_staff=cursor.fetchall()
    cursor.execute("delete from this_week where id>0;")
    cursor.execute("insert into this_week SELECT * FROM real_next_week;")
    for i in all_staff:
        cursor.execute("select working_hour from staff where id=%s;",(i[0],))
        temp=cursor.fetchone()
        cursor.execute("select count(*) from real_next_week where id=%s;",(i[0],))
        buf=cursor.fetchone()
        count=buf[0]+temp[0]
        print(count)
        cursor.execute("UPDATE staff SET salary=%s where id =%s;",(count*8*183,i[0],))
        cursor.execute("UPDATE staff SET working_hour=%s where id =%s;",(count,i[0],))

    cursor.execute("UPDATE real_next_week SET id=null where day_id is not null;")
    cursor.close()
    connection.close()