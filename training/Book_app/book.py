import json
from datetime import datetime , timedelta
from flask import Flask , render_template , request,redirect
import requests
from collections import OrderedDict
application = Flask(__name__)
now= datetime.now()
DATA_FILE= 'books.json'


def save_data(name,pic,pages,deadline,pace):
    """bookデータからjsonファイルにデータを保存する。
    :param id:書籍番号(順番)
    :type id: int
    :param name:書籍名
    :type name: str
    :param pic:画像
    :type pic: url str
    :param pages:ページ数
    :pages type: int
    :param deadline:期限
    :deadline type:datetime.datetime.now()
    :param bookmark:進捗
    :param type: 年ー月ー日
    :param pace: ペース
    :param type: int
    """
    try:
        database=json.load(open(DATA_FILE,mode="r",encoding="utf-8"))
    except FileNotFoundError :
        database=[]
    if len(database)==0:
        id=1
    else:
        ids=[]
        for i in database:
            ids.append(i["id"])
        id=max(ids)+1
    database.insert(id-1,{
        "id":id,
        "name":name,
        "pic":pic,
        "pages":pages,
        "deadline":deadline,
        "bookmark":0,
        "pace":pace,
        })
    json.dump(database,open(DATA_FILE,mode="w",encoding="utf-8"),indent=4,ensure_ascii=False)

def import_data(name,days):
    """書籍スクレイプ
    amazonサイトにアクセスする。
    入力された書籍名で検索し、商品ページの情報から
    画像、ページ数をとってくる。
    IDつきBOOKデータを生成し、返す。
    save_data関数を呼び出す。
    """
    api="https://www.googleapis.com/books/v1/volumes?q={}".format(name)
    r=requests.get(api)
    dic=json.loads(r.text)
    book=dic["items"][0]['volumeInfo']
    name=book['title']
    pages=book['pageCount']
    pic=book['imageLinks']['thumbnail']
    deadline=(now+timedelta(days=10)).strftime('%Y-%m-%d')
    pace=pages/days
    save_data(name,pic,pages,deadline,pace)

def load_data():
    """jsonデータを返す。"""
    try:
        database=json.load(open(DATA_FILE,mode="r",encoding="utf-8"))
    except FileNotFoundError:
        database=[]
    return database

@application.route('/schedule',methods=['POST'])
def schedule():
    """場所は各書籍編集ページ
    入力された現在のページを用いて、書籍データを更新する。
    bookの名前と現在のページを使う。
    現在ページ、ペースを更新"""
    id=int(request.form.get("id"))-1
    bookmark=request.form.get("bookmark")
    with open('books.json',"r") as f:
        d_update=json.load(f, object_pairs_hook=OrderedDict)
    d_update[id]['bookmark']=bookmark
    leftdays=(datetime.strptime(d_update[id]['deadline'],'%Y-%m-%d')-now).days
    d_update[id]['pace']=(d_update[id]['pages']-len(bookmark))/leftdays
    with open('books.json',"w") as f:
        json.dump(d_update,f,indent=4,ensure_ascii=False)
    return redirect("/")

@application.route('/')
def index():
    books=load_data()
    return render_template('index.html',books=books)

@application.route('/book',methods=['POST'])
def book_data():
    id=int(request.form.get('id'))-1
    books=load_data()
    book=books[id]
    return render_template('schedule.html',book=book)

@application.route('/save',methods=['POST'])
def mkbook():
    name=request.form.get("name")
    days=int(request.form.get("days"))
    import_data(name,days)
    return redirect("/")

if __name__=='__main__':
    application.run(debug=True)
