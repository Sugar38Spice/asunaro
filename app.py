from flask import Flask , render_template , request , redirect , session

app = Flask(__name__)

@app.route("/index")
def logout():
    session.pop('user_id',None)
    # ログアウト後はログインページにリダイレクトさせる
    return redirect("/index")


<<<<<<< HEAD

if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
=======
  if __name__ == "__main__":
     Flask が持っている開発用サーバーを、実行します。
>>>>>>> c97103102813e90be9d3c34b63c757908b61cc1f
    app.run()