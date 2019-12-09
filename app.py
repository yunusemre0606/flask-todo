from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "Çok gizli key"
client = MongoClient("mongodb+srv://egitim:egitim48@cluster0-eqjet.mongodb.net/test?retryWrites=true&w=majority")
db = client.tododb.todos
@app.route('/')
def index():
    yapilacaklar=[]
    for yap in db.find():
        yapilacaklar.append({"_id":str(yap.get("_id")),
        "isim":yap.get("isim"), "durum":yap.get("durum")
        })

    return render_template('index.html',yapilacaklar = yapilacaklar)
@app.route('/guncelle/<id>')
def guncelle(id):
    yap=db.find({'_id':ObjectId(id)})
    durum=not yap.get('durum')
    db.find_one_and_update({'_id':ObjectId(id)},{'$set':{'durum':durum}})
    return redirect('/')
@app.route('/sil/<id>')
def sil(id):
    db.find_one_and_delete({'_id':ObjectId(id)})
    return redirect('/')
@app.route('/ekle', methods = ['POST'])
def ekle():
    isim=request.form.get('isim')
    db.insert_one({'isim':isim, 'durum':'False'})
    return redirect('/')

@app.errorhandler(404)
def hatali_url():
    return redirect('/')
   
   
@app.route('/user/<isim>')
def user(isim):

    return render_template('user.html', isim=isim)
    
@app.route('/kimiz')
def kimiz():
    return render_template('kimiz.html')

       
if __name__ == '__main__':
  app.run(debug=True)
