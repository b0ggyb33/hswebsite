from flask import Flask, request,jsonify,render_template
from RNG import rng
import rethinkdb as r

app = Flask(__name__)

randomNameGenerator = rng()

@app.route("/")
def hello():
    return render_template('index.html')

def tabifyResult(scores):
    for idx,score in enumerate(scores):
        try:
            score['username']=getNameOfWatch(randomNameGenerator,score['username'])
        except KeyError:
            pass
        score['index']=idx+1


def renderScores(nameOfTable, GameName):
    r.connect().repl()

    try:
        r.db("test").table_create(nameOfTable).run()
    except r.ReqlOpFailedError:
        pass

    bestScorePerPlayer = r.table(nameOfTable).group("username").max("score").run()
    topscoresPerPlayer = r.expr(bestScorePerPlayer.values()).order_by(r.desc("score")).limit(10).run()
    topscoresofalltime = r.table(nameOfTable).order_by(r.desc("score")).limit(10).run()
    
    tabifyResult(topscoresPerPlayer)
    tabifyResult(topscoresofalltime)
    
    return render_template('bshighScores.html',gameName=GameName, topscoresByPlayerTable=topscoresPerPlayer,topscoresalltimeTable=topscoresofalltime)


@app.route("/ballscores")
def ball():
    return renderScores("authors","Ball")

@app.route("/firescores")
def fire():
    return renderScores("fire","Fire")

@app.route('/about')
def aboutPage():
    return render_template('about.html')

def submitJson(tableName,data):
    r.connect().repl()
    try:
        r.db("test").table_create(tableName).run()
    except r.ReqlOpFailedError:
        pass
    try:
        r.db("test").table_create("nameMapping").run()
    except r.ReqlOpFailedError:
        pass
    if request.method == 'POST':
        if data['type']=="username":
            data=getNameOfWatch(randomNameGenerator,data['username'])
            return data
        elif data['type']=="score":
            r.table(tableName).insert(data).run()
            return "submitted"
    return "xx"

@app.route('/json', methods=['POST'])
def json():
    return submitJson("authors",request.get_json())
    
@app.route('/jsonFire', methods=['POST'])
def jsonFire():
    return submitJson("fire",request.get_json())
    

def getNameOfWatch(randomNameGenerator,name):
    try:
        r.db("test").table_create("nameMapping").run()
    except r.ReqlOpFailedError:
        pass
    results = r.table("nameMapping").filter(r.row['username']==name).run()
    for item in results:
        return item['friendly']
    else:
	#add to database
        print "New player!"
        newData={'username':name,'friendly':randomNameGenerator.getName()}
        r.table("nameMapping").insert(newData).run()
        return newData['friendly']


if __name__ == "__main__":
    #r.connect().repl()
    #r.db("test").table_create("authors").run()
    app.debug = False
    app.run('0.0.0.0')
