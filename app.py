from flask import Flask , render_template , request , redirect , session

app = Flask(__name__)

@app.route("/logout")
def logout():
    session.pop('user_id',None)
    # ログアウト後はログインページにリダイレクトさせる
    return redirect("/login")


  if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run()