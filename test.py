import mysql.connector
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'anna901228',
    'database': 'human_computer',
}

connection = mysql.connector.connect(**db_config)

cursor = connection.cursor()
for i in (1,8):
    for j in (1,4):
        cursor.execute("insert into real_next_week values(null,%s,%s);",(i,j,))



cursor.close()
connection.close()

