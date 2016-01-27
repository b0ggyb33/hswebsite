from flask import Flask, request,jsonify,render_template
from RNG import rng
import rethinkdb as r

app = Flask(__name__)

randomNameGenerator = rng()

@app.route("/")
def hello():
    r.connect().repl()

    try:
        r.db("test").table_create("authors").run()
    except r.ReqlOpFailedError:
        pass

    bestScorePerPlayer = r.table("authors").group("username").max("score").run()
    results = r.expr(bestScorePerPlayer.values()).order_by(r.desc("score")).limit(10).run()


    for idx,result in enumerate(results):
        try:
            result['username']=getNameOfWatch(randomNameGenerator,result['username'])
        except KeyError:
            pass
        result['index']=idx+1

    return render_template('bshighScores.html', scores=results)


@app.route('/json', methods=['POST'])
def json():
    data=request.get_json()
    r.connect().repl()
    try:
        r.db("test").table_create("authors").run()
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
            r.table("authors").insert(data).run()
            return "submitted"
    return " "
    

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
