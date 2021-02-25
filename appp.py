import os

import sqlite3 #pythonから直接呼び出せる

from flask import Flask , render_template ,request ,redirect ,session


app = Flask(__name__)

#シークレットキーの設定。本来乱数を入れる（pythonのsecret機能を使うと尚よし)
app.secret_key = "sunabacokoza"

from detetime import detetime
    
@app.route('/')
def index():
    return render_template('index.html')

# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
@app.route('/register',methods=["GET", "POST"])
def register():
    #  登録ページを表示させる
    if request.method == "GET":
        if 'user_id' in session :
            return redirect ('/bbs')
        else:
            return render_template("register.html")

    # ここからPOSTの処理
    else:
        # 登録ページで登録ボタンを押した時に走る処理
        name = request.form.get("name")
        password = request.form.get("password")

        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # 課題4の答えはここ
        c.execute("insert into user values(null,?,?,'no_img.png')", (name,password))
        conn.commit()
        conn.close()
        return redirect('/login')


# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'user_id' in session :
            return redirect("/bbs")
        else:
            return render_template("login.html")
    else:
        # ブラウザから送られてきたデータを受け取る
        name = request.form.get("name")
        password = request.form.get("password")

        # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
        # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("select id from user where name = ? and password = ?", (name, password) )
        user_id = c.fetchone()
        conn.close()
        # DBから取得してきたuser_id、ここの時点ではタプル型
        print(type(user_id))
        # user_id が NULL(PythonではNone)じゃなければログイン成功
        if user_id is None:
            # ログイン失敗すると、ログイン画面に戻す
            return render_template("login.html")
        else:
            session['user_id'] = user_id[0]
            return redirect("/bbs")


@app.route("/logout")
def logout():
    session.pop('user_id',None)
    # ログアウト後はログインページにリダイレクトさせる
    return redirect("/login")


@app.route('/bbs')
def bbs():
    if 'user_id' in session :
        user_id = session['user_id']
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
        # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
        c.execute("select name,prof_img from user where id = ?", (user_id,))
        # fetchoneはタプル型
        user_info = c.fetchone()
        # user_infoの中身を確認

        # 課題1の答えはここ del_flagが0のものだけ表示する
        # 課題2の答えはここ 保存されているtimeも表示する
        c.execute("select id,comment,time from bbs where userid = ? and del_flag = 0 order by id", (user_id,))
        comment_list = []
        for row in c.fetchall():
            comment_list.append({"id": row[0], "comment": row[1], "time":row[2]})

        c.close()
        return render_template('bbs.html' , user_info = user_info , comment_list = comment_list)
    else:
        return redirect("/login")



@app.route('/add', methods=["POST"])
def add():
    user_id = session['user_id']

    # 課題2の答えはここ 現在時刻を取得
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    # POSTアクセスならDBに登録する
    # フォームから入力されたアイテム名の取得(Python2ならrequest.form.getを使う)
    comment = request.form.get("comment")
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # 現在の最大ID取得(fetchoneの戻り値はタプル)

    # 課題1の答えはここ null,?,?,0の0はdel_flagのデフォルト値
    # 課題2の答えはここ timeを新たにinsert
    c.execute("insert into bbs values(null,?,?,0,?)", (user_id, comment,time))
    conn.commit()
    conn.close()
    return redirect('/bbs')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' in session :
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("select comment from bbs where id = ?", (id,) )
        comment = c.fetchone()
        conn.close()

        if comment is not None:
            # None に対しては インデクス指定できないので None 判定した後にインデックスを指定
            comment = comment[0] # "りんご" ○   ("りんご",) ☓
            # fetchone()で取り出したtupleに 0 を指定することで テキストだけをとりだす
        else:
            return "アイテムがありません" # 指定したIDの name がなければときの対処

        item = { "id":id, "comment":comment }

        return render_template("edit.html", comment=item)
    else:
        return redirect("/login")


# /add ではPOSTを使ったので /edit ではあえてGETを使う
@app.route("/edit")
def update_item():
    if 'user_id' in session :
        # ブラウザから送られてきたデータを取得
        item_id = request.args.get("item_id") # id
        print(item_id)
        item_id = int(item_id) # ブラウザから送られてきたのは文字列なので整数に変換する
        comment = request.args.get("comment") # 編集されたテキストを取得する

        # 既にあるデータベースのデータを送られてきたデータに更新
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("update bbs set comment = ? where id = ?",(comment,item_id))
        conn.commit()
        conn.close()

        # アイテム一覧へリダイレクトさせる
        return redirect("/bbs")
    else:
        return redirect("/login")

@app.route('/del' , methods=["POST"])
def del_task():
    id = request.form.get("comment_id")
    id = int(id)
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # 指定されたitem_idを元にDBデータを削除せずにdel_flagを1にして一覧からは表示しないようにする
    # 課題1の答えはここ del_flagを1にupdateする
    c.execute("update bbs set del_flag = 1 where id=?", (id,))
    conn.commit()
    conn.close()
    # 処理終了後に一覧画面に戻す
    return redirect("/bbs")

#課題4の答えはここ
@app.route('/upload', methods=["POST"])
def do_upload():
    # bbs.tplのinputタグ name="upload" をgetしてくる
    upload = request.files['upload']
    # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'png,jpg,jpeg形式のファイルを選択してください'
    
    # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
    save_path = get_save_path()
    # パスが取得できているか確認
    print(save_path)
    # ファイルネームをfilename変数に代入
    filename = upload.filename
    # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
    upload.save(os.path.join(save_path,filename))
    # ファイル名が取れることを確認、あとで使うよ
    print(filename)
    
    # アップロードしたユーザのIDを取得
    user_id = session['user_id']
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # update文
    # 上記の filename 変数ここで使うよ
    c.execute("update user set prof_img = ? where id=?", (filename,user_id))
    conn.commit()
    conn.close()

    return redirect ('/bbs')

#課題4の答えはここも
def get_save_path():
    path_dir = "./static/img"
    return path_dir


@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound(code):
    return "404だよ！！見つからないよ！！！"


# __name__ というのは、自動的に定義される変数で、現在のファイル(モジュール)名が入ります。 ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になります。
if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run( host='0.0.0.0', port=80 , debug=False)













@app.route("/")
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
  

@app.route("/login" , methods =["get"])
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

@app.route("/logout")
def logput():
    session.pop("user_id",None)
    return redirect("/login")



@app.errorhandler(404)
def notfound(code):
    return "404エラーです。このページはすでに消されてしまったか存在していません。"



if __name__ == "__main__":
    app.run(debug=True)