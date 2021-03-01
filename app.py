from flask import Flask , render_template ,request ,redirect ,session
import sqlite3

app = Flask(__name__)

app.secret_key = "sunabacokoza"

from datetime import datetime

@app.route("/")
def index():
    return render_template("index.html")





@app.route("/login")
def login_post():
    conn = sqlite3.connect("asunaro.db")
    c = conn.cursor()
    c.execute("SELECT id , name , password FROM asunarostaff WHERE id = 1;")
    user_info = c.fetchone()
    print(user_info)
    conn.close()
    return render_template("login.html" )
    # user_name = request.form.get("user_name")
#     password = request.form.get("password")
#     conn = sqlite3.connect("task.db")
#     c = conn.cursor()
#     c.execute("SELECT id FROM users WHERE user_name = ? and password = ?", (user_name, password) )
#     user_id = c.fetchone()

#     conn.close()

#     if user_id is None:
#         return "ログイン情報が正しくありません"
#     else:
#         session["user_id"] =user_id[0]
#         return redirect("/list")


@app.route("/myp")
def template():
    py_name = "name"
    # return name + "さん、こんにちは"
    return render_template("myp.html", name = py_name)

@app.route('/zzz')
def register2():
    #  登録ページを表示させる  
    return render_template("zzz.html")
# @app.route("/temptest")
# def temptest():
#     py_name = "にんじゃわんこ"
#     return  render_template("index.html", user_name = py_name)


@app.route("/staff")
def staff_info():
    conn = sqlite3.connect("asunaro.db")
    c = conn.cursor()
    c.execute("SELECT id , name , password , message FROM asunarostaff WHERE id = ?;")
    user_info = c.fetchone()
    print(user_info)
    conn.close()
    return  render_template("growth.html",html_staff = user_info)  

# 投稿ページ
@app.route("/post" , methods= ["GET"])
def post_get():
        return render_template("post.html")

# どんな情報をとるの
@app.route("/post" , methods= ["POST"])
def add_post():
    # text.areaから投稿内容を取得
    posting = request.form.get("posting")  
    # 投稿内容を保存するDBを指定
    conn = sqlite3.connect("asunaro.db")
    c = conn.cursor()
    # SQL文で情報（ID,投稿内容,日時,ユーザーID）を取得
    c.execute('INSERT INTO posts_test VALUES(null,?);' , (posting,))
    # 投稿完了(悲観ロックなので)
    conn.commit()
    # DB接続終了
    conn.close()
    return "書き込み完了しました。えらい！"


@app.route("/list" )
def task_list():
    if "user_id" in session :
        user_id = session["user_id"]
        conn = sqlite3.connect("task.db")
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE user_id = ?",(user_id,))
        task_list = []
        for task in c.fetchall():
            task_list.append(
                {"id":task[0],"task":task[1]}
            )
        conn.close()
        return  render_template("task_list.html" , task_list = task_list, user_id = user_id)
    else:
        return  redirect("/login")

@app.route("/edit/<id>" , methods = ["get"])
def edit(id):
    if "user_id" in session :
        conn = sqlite3.connect("task.db")
        c = conn.cursor()
        c.execute("SELECT task FROM tasks where id = ?" , (id,))
        task = c.fetchone()
        print(task)
        task = task[0]

        py_task = {"dic_id":id, "dic_task":task}
        conn.close()
        return  render_template("edit.html" ,html_task = py_task)
    else:
        return  redirect("/login")

@app.route("/edit" , methods =["post"])
def edit_post():
    if "user_id" in session :
        task_id = request.form.get("task_id")
        task_id = int(task_id)
        task_input = request.form.get("task_input")
        conn = sqlite3.connect("task.db")
        c = conn.cursor()
        c.execute("UPDATE tasks SET task = ? WHERE id = ?", (task_input,task_id))
        conn.commit()
        conn.close()
        return redirect("/list")
    else:
        return  redirect("/login")

@app.route("/del/<id>")
def del_task(id):
    if "user_id" in session :
        conn = sqlite3.connect("task.db")
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect("/list")
    else:
        return  redirect("regist.html")

@app.route("/regist", methods =["get"])
def regist_get():
    if "user_id" in session :
        return render_template("/list")
    else:
        return  render_template("regist.html")

@app.route("/regist", methods =["post"])
def regist_post():
    if "user_id" in session :
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        conn = sqlite3.connect("task.db")
        c = conn.cursor()
        c.execute("insert into users values(null,?,?)", (user_name, password) )
        conn.commit()
        conn.close()
        return "登録が完了しました！"
    else:
        return  render_template("/login")

# @app.route("/login", methods =["get"])
# def login_post():
#     if "user_id" in session :    
#         return redirect("/list")
#     else:
#         return  redirect("/login")

# @app.route("/login", methods =["post"])
# def login_posting():
#     user_name = request.form.get("user_name")
#     password = request.form.get("password")
#     conn = sqlite3.connect("task.db")
#     c = conn.cursor()
#     c.execute("SELECT id FROM users WHERE user_name = ? and password = ?", (user_name, password) )
#     user_id = c.fetchone()

#     conn.close()

#     if user_id is None:
#         return "ログイン情報が正しくありません"
#     else:
#         session["user_id"] =user_id[0]
#         return redirect("/list")

@app.route("/logout", methods =["get"])
def logout():
    session.pop("user_id",None)
    return  render_template("login.html")








@app.errorhandler(404)
def notfound(code):
    return "404エラーです。このページはすでに消されてしまったか存在していません。"




if __name__ == "__main__":
    app.run(debug=True)
