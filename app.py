from flask import Flask , render_template ,request ,redirect ,session
import sqlite3

app = Flask(__name__)

app.secret_key = "sunabacokoza"

from datetime import datetime

@app.route("/")
def index():
    return render_template("index.html")

# index→loginページ遷移
@app.route("/login",methods=["POST"])
def login():
    return redirect("/login")




@app.route('/new',methods=["GET"])
def new():
    #if request.method == "GET":
    if 'asunarostaff_id' in session :
        print("test1")
        return redirect ('/login')
    else:
        return render_template("new.html")

    #print(name)
    #print(password)        

@app.route('/new',methods=["POST"])
def new_post():
    print("test2")
    name = request.form.get("name")
    password = request.form.get("password")
    print(name)
    print(password)
    conn = sqlite3.connect('asunaro.db')
    c = conn.cursor()
    c.execute("insert into asunarostaff values(null,?,?)", (name,password))
    conn.commit()
    conn.close()
    return redirect('/login')




#ここからコピペ
# GET  /register => 登録画面を表示
# POST /register => 登録処理をする



# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
@app.route("/loginpage")
def login2():
    if 'asunarostaff_id' in session :
        return redirect("/list")
    else:
        return render_template("login.html")
   
        

@app.route("/path", methods=["POST"])
def login_post():
    print("loginpost")
    # ブラウザから送られてきたデータを受け取る
    name = request.form.get("name")
    password = request.form.get("password")

    # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
    # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
    conn = sqlite3.connect('asunaro.db')
    c = conn.cursor()
    c.execute("select id from asunarostaff where name = ? and password = ?", (name, password) )
    user_id = c.fetchone()
    conn.close()
    print("test")
    #print(type(asunarostaff_id))
    # user_id が NULL(PythonではNone)じゃなければログイン成功
    if user_id is None:
        # ログイン失敗すると、ログイン画面に戻す
        return render_template("login.html")
    else:
        print(user_id)
        session['asunarostaff_id'] = user_id[0]
        return redirect("/list")

@app.route("/logout")
def logout():
    session.pop('asunarostaff_id',None)
    # ログアウト後はログインページにリダイレクトさせる
    return redirect("/login")







#ここまでコピペ
  


#ここから元のやつ
#@app.route("/login")
#conn = sqlite3.connect("asunaro.db")
    #c = conn.cursor()
    #c.execute("SELECT id , name , password FROM asunarostaff WHERE id = 1;")
    #user_info = c.fetchone()
    #print(user_info)
    #conn.close()
    #return render_template("login.html" )
#ここまで元のやつ


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
    user_id = session['asunarostaff_id']
    # 投稿内容を保存するDBを指定
    conn = sqlite3.connect("asunaro.db")
    c = conn.cursor()
    # SQL文で情報（ID,投稿内容,日時,ユーザーID）を取得
    c.execute('INSERT INTO posts_test VALUES(null,?,?);' , (posting,user_id))
    # 投稿完了(悲観ロックなので)
    conn.commit()
    # DB接続終了
    conn.close()
    return redirect("/list")

# growth.htmlの投稿一覧・# 投稿数を表示

@app.route("/list" )
def posting_list():
    conn = sqlite3.connect("asunaro.db")
    c = conn.cursor()

    c.execute("SELECT count (posting) FROM posts_test")
    post_count = c.fetchone()
    print(post_count) 



    c.execute("SELECT * FROM posts_test")
    # 受け取ったデータの加工
    post_list = [] #空箱作ったよ
    # postという関数作った
    for post in c.fetchall():
        post_list.append(
            {"id":post[0],"posting":post[1]}
        )
    conn.close()
    # print(post_list)
    return  render_template("growth.html", post_list = post_list , post_count = post_count)



#投稿内容の編集
@app.route("/edit/<id>" , methods=["GET"])
def edit(id):
    conn = sqlite3.connect("asunaro.db")
    c = conn.cursor()
    # SQL文を実行してデータの参照
    c.execute("select posting from posts_test where id =?", (id,))
    task = c.fetchone()
    print(task) #このprintは任意、taskの中身の確認用
    task = task[0]

    py_task = {"dic_id":id,"dic_task":task}
    conn.close()
    return render_template("edit.html" ,html_task = py_task)


@app.route("/edit" , methods =["post"])
def edit_post():
        #フォームで編集された内容を受け取る
        task_id = request.form.get("post_id") #id
        task_id = int(task_id) #idを型変換する
        task_input = request.form.get("post_input") #タスクの変更後の内容
        conn = sqlite3.connect("asunaro.db")
        c = conn.cursor()
        #2:37
        c.execute("UPDATE posts_test SET posting = ? WHERE id = ?", (task_input,task_id))
        conn.commit()
        conn.close()
        return redirect("/list")
    # else:
    #     return  redirect("/login")

@app.route("/del/<id>")
def del_task(id):
        conn = sqlite3.connect("asunaro.db")
        c = conn.cursor()
        c.execute("DELETE FROM posts_test WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect("/list")
    # else:
    #     return  redirect("regist.html")

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





#@app.route("/logout", methods =["get"])
#def logout():
    session.pop("user_id",None)
    return  render_template("login.html")








@app.errorhandler(404)
def notfound(code):
    return "404エラーです。このページはすでに消されてしまったか存在していません。"




if __name__ == "__main__":
    app.run(debug=True)
