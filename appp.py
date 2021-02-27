
from flask import Flask , render_template ,request ,redirect ,session
import sqlite3 #pythonから直接呼び出せる

app = Flask(__name__)

#シークレットキーの設定。本来乱数を入れる（pythonのsecret機能を使うと尚よし)
app.secret_key = "sunabacokoza"

from datetime import datetime
    
@app.route('/')
def index():
    return render_template('index.html')

# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
@app.route("/login")
def login_get():
    
    if "user_id" in session :
        return redirect("/list")
    else:
        return render_template("/login.html")

@app.route("/login" , methods = ["post"])
def login_post():
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    conn = sqlite3.connect("style.db")
    c = conn.cursor()
    
    c.execute("SELECT id FROM users WHERE user_name = ? and password = ?" , (user_name, password))
    user_id = c.fetchone()
    #DB接続終了
    conn.close()
    #会員情報があればログイン、なければ表示される
    if user_id is None:
        return "ログイン情報が正しくありません"
    else:
        #user_id野中のデータだけ取りたいからインデックスで指定してsessionに代入
        session["user_id"] = user_id[0]  
         
        return redirect("/list")


# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
@app.route('/myp')
def register():
    #  登録ページを表示させる  
    return render_template("myp.html")

@app.route('/zzz')
def register2():
    #  登録ページを表示させる  
    return render_template("zzz.html")


    

@app.route("/staff")
def staff_info():
    #DBと接続開始
    conn = sqlite3.connect("style.db")
    c = conn.cursor()
    #SQL文を実行してデータの参照
    c.execute("SELECT  name , age , address FROM staff WHERE id = 2;")
    #pythonでデータとして使えるようにする
    user_info = c.fetchone()
    print(user_info)
    #DB接続終了
    conn.close()
    return render_template("staff.html",html_staff = user_info)



@app.route("/add" , methods = ["GET"])
def add_get():
    if "user_id" in session :
        return render_template("add.html")
    else:
        return redirect("/login")


@app.route("/add" , methods = ["post"])
def add_post():
    if "user_id" in session :
        user_id = session["user_id"]#cookieに保存されているidをuser_idに代入
        task = request.form.get("task")

        #DBと接続開始
        conn = sqlite3.connect("style.db")
        c = conn.cursor()
        #SQL文を実行してデータの参照
        c.execute("insert into tasks values(null, ?,?);" , (task,user_id)) 
        #書き込み完了
        conn.commit()
        #DB接続終了
        conn.close()
        return redirect("/list")
    else:
        return redirect("/login")

    # 課題2の答えはここ 現在時刻を取得
    time = datetime.now().strftime('%m/%d')

@app.route("/list")
def task_list():
    if "user_id" in session :
        user_id = session["user_id"] 

        conn = sqlite3.connect("style.db")
        c = conn.cursor()
        #SQL文を実行してデータの参照
        c.execute("SELECT * FROM tasks WHERE user_id = ?;" ,(user_id,)) 
        task_list = []
        for task in c.fetchall():
            task_list.append(
                {"id":task[0],"task":task[1]}
            )

       
        #DB接続終了
        conn.close()
        return render_template("task_list.html" , task_list = task_list, user_id = user_id)
    else:
        return redirect("/login")


@app.route("/edit/<id>" , methods = ["get"])
def edit(id):
    if "user_id" in session :
        conn = sqlite3.connect("style.db")
        c = conn.cursor()
        
        c.execute("select task from tasks where id = ?" ,(id,))
        task = c.fetchone()
        print(task)
        task = task[0] #()と’’を取る為にインデックス番号で指定して中身だけ取って再代入している

        py_task = {"dic_id":id,"dic_task":task}

        conn.close()
        return render_template("edit.html" ,html_task = py_task)
    else:
        return redirect("/login")

@app.route("/edit" , methods =["post"])
def edit_post():
    if "user_id" in session :
        task_id = request.form.get("task_id")
        task_id = int(task_id)
        task_input = request.form.get("task_input")

        conn = sqlite3.connect("style.db")
        c = conn.cursor()
        c.execute("update tasks SET task = ? WHERE id = ?", (task_input,task_id))
        #データの変更が行われたので保存する
        conn.commit()
        conn.close()
        return redirect("/list")
    else:
        return redirect("/login")


@app.route("/del/<id>")
def del_task(id):
    if "user_id" in session :
        conn = sqlite3.connect("style.db")
        c = conn.cursor()
        
        c.execute("delete from tasks where id = ?" ,(id,))

        conn.commit()
        
        conn.close()
        return redirect("/list")
    else:
        return redirect("/login")

@app.route("/regist" , methods =["get"])
def regist_get():
    if "user_id" in session :
        return redirect("/list")
    else:
        return render_template("regist.html")

@app.route("/regist" , methods = ["post"])
def regist_post():
    
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    conn = sqlite3.connect("style.db")
    c = conn.cursor()

    c.execute("insert into users values(null,?,?)" , (user_name,password))

    conn.commit()

    conn.close()
    return "登録が完了しました"
  


@app.route("/logout")
def logput():
    session.pop("user_id",None)
    return redirect("/login")



@app.errorhandler(404)
def notfound(code):
    return "404エラーです。このページはすでに消されてしまったか存在していません。"



if __name__ == "__main__":
    app.run(debug=True)