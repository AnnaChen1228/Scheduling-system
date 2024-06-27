from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL 資料庫連接設定
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'anna901228',
    'database': 'human_computer',
}

@app.route('/')
def index():
    session['id']=None
    return render_template('index.html')

@app.route('/boss_login', methods=['GET', 'POST'])
def boss_login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username != 'boss':
            message='Username or Password is Error!'
            return render_template('boss_login.html', message=message)

        conn = None  
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT pw FROM id_pw WHERE count=%s", (username,))
            result = cursor.fetchone()
            if result:
                if password == result[0]:
                    cursor.execute("SELECT id FROM id_pw WHERE count=%s", (username,))
                    res = cursor.fetchone()
                    session['id']=res[0]
                    print(session['id'])
                    # 登入成功
                    return redirect(url_for('boss_dashboard'))
        
            message='Username or Password is Error!'
            return render_template('boss_login.html', message=message)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
    return render_template('boss_login.html')

@app.route('/boss_dashboard')
def boss_dashboard():
    conn = None  # 初始化為 None，以確保在 finally 區塊中可以正確處理
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM this_week order by day_id;")
        result = cursor.fetchall()#id day_id time_id
        results=[]
        for i in result:
            cursor.execute("SELECT name FROM staff where id=%s;",(i[0],))
            name=cursor.fetchone()
            temp=i+name
            results.append(temp)
        #print(results)
        return render_template('boss.html',schedule=results)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/boss_nextweek')
def boss_nextweek():
    conn = None  # 初始化為 None，以確保在 finally 區塊中可以正確處理
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM real_next_week ORDER BY day_id;")
        result = cursor.fetchall()  # id day_id time_id
        results = []
        have=False
        current_day = datetime.now().strftime('%w')
        if current_day > '4':
            if result:
                have=True
                for i in result:
                    cursor.execute("SELECT name FROM staff WHERE id=%s;", (i[0],))
                    name = cursor.fetchone()
                    if name:
                        temp = i + name
                        results.append(temp)

            print(results)
        return render_template('boss_nextweek.html', is_next=have,schedule=results)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occurred while processing your request."

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def fetch_staff_info():
    conn = None
    staff = []
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM staff;")
        staff = cursor.fetchall()
        print(staff)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return staff

@app.route('/staff_list')
def staff_list():
    staffs = fetch_staff_info()
    return render_template('staff_info.html', staffs=staffs)

@app.route('/staff_info')
def staff_info():
    staffs = fetch_staff_info()
    return render_template('staff_info.html', staffs=staffs)

@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Received username: {username}")
        print(f"Received password: {password}")

        if username == 'boss':
            message='Username or Password is Error!'
            return render_template('staff_login.html', message=message)

        conn = None  # 初始化為 None，以確保在 finally 區塊中可以正確處理
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT pw FROM id_pw WHERE count=%s", (username,))
            result = cursor.fetchone()
            if result:
                if password == result[0]:
                    # 登入成功
                    cursor.execute("SELECT id FROM id_pw WHERE count=%s", (username,))
                    res = cursor.fetchone()
                    session['id']=res[0]
                    print(f"id: {session['id']}")
                    return redirect(url_for('staff_dashboard'))
            # 登入失敗
            message='Username or Password is Error!'
            return render_template('staff_login.html', message=message)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('staff_login.html')

@app.route('/staff_dashboard')
def staff_dashboard():
    conn = None  # 初始化為 None，以確保在 finally 區塊中可以正確處理
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM this_week where id=%s order by day_id;",(session['id'],))
        result = cursor.fetchall()#id day_id time_id
        results=[]
        for i in result:
            cursor.execute("SELECT name FROM staff where id=%s;",(i[0],))
            name=cursor.fetchone()
            temp=i+name
            results.append(temp)
        #print(results)
        temp = []
        day_index = 1
        result_index = 0

        # Iterate over 7 days
        for day_index in range(1, 8):
            if result_index < len(results) and results[result_index][1] == day_index:
                temp.append(results[result_index])
                result_index += 1
            else:
                temp.append((0, 0, 0, 0))
        return render_template('staff.html',schedule=temp)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/staff_nextweek_nochoose', methods=['GET', 'POST'])
def staff_nextweek_nochoose():
    if request.method == 'POST':
        selected_values = request.form.getlist('selected_values')
        print(selected_values)
        conn = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            for value in selected_values:
                day_id, time_id = map(int, value.split('-'))
                cursor.execute("INSERT INTO next_week VALUES (%s, %s, %s, NOW());",
                               (session.get('id'), day_id, time_id))
            cursor.execute("UPDATE choose SET is_choose=true WHERE id=%s;",
                           (session.get('id'),))
            conn.commit()
            return redirect(url_for('staff_nextweek'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn.rollback()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('staff_nextweek_nochoose.html')

@app.route('/staff_nextweek', methods=['GET', 'POST'])
def staff_nextweek():
    conn = None
    item = ['next_week', 'real_next_week']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        current_day = datetime.now().strftime('%w')
        if current_day > '4':
            schedule_item = item[1]
        else:
            cursor.execute("SELECT is_choose FROM choose WHERE id=%s;", (session['id'],))
            choose = cursor.fetchone()

            if not choose[0]:
                return redirect(url_for('staff_nextweek_nochoose'))
            else:
                schedule_item = item[0]

        cursor.execute(f"SELECT id, day_id, time_id FROM {schedule_item} WHERE id=%s ORDER BY day_id;", (session['id'],))
        result = cursor.fetchall()

        results = []
        for i in result:
            cursor.execute("SELECT name FROM staff WHERE id=%s;", (i[0],))
            name = cursor.fetchone()
            temp = i + name
            results.append(temp)

        temp = []
        day_index = 1
        time1_entries = []
        time2_entries = []
        time3_entries = []

        for day_index in range(1, 8):
            time1_entry = next((entry for entry in results if entry[1] == day_index and entry[2] == 1), (0, 0, 0, 0, 0))
            time2_entry = next((entry for entry in results if entry[1] == day_index and entry[2] == 2), (0, 0, 0, 0, 0))
            time3_entry = next((entry for entry in results if entry[1] == day_index and entry[2] == 3), (0, 0, 0, 0, 0))

            time1_entries.append(time1_entry)
            time2_entries.append(time2_entry)
            time3_entries.append(time3_entry)

        # Combine the three time slot lists into a single list
        temp = [time1_entries, time2_entries, time3_entries]

        return render_template('staff_nextweek.html', schedule=temp)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    

@app.route('/your_info')
def your_info():
    return your_list()

@app.route('/your_list')
def your_list():
    conn = None
    your = []
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT* FROM staff WHERE id=%s;",(int(session['id']),))
        your = cursor.fetchall()
        print(your)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return render_template('your_info.html', yours=your)

@app.route('/log_out', methods=['POST'])
def log_out():
    if 'id' in session:
        print('log in='+str(session['id']))
        session.pop('id')
    return render_template('index.html')

def run_schedule():
    subprocess.run(["python", "schedule.py"])

def run_update():
    subprocess.run(["python", "update.py"])

# 初始化背景排程器
scheduler = BackgroundScheduler()
scheduler.start()

# 每週五早晨 2 點執行 schedule.py
scheduler.add_job(run_schedule, trigger='cron', day_of_week='fri', hour=0, minute=0)

# 每週一早晨 2 點執行 update.py
scheduler.add_job(run_update, trigger='cron', day_of_week='mon', hour=0, minute=0)


if __name__ == '__main__':
    app.run(debug=True)