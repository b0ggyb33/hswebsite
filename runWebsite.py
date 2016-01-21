from flask import Flask, request,jsonify,render_template
from RNG import rng
import rethinkdb as r


app = Flask(__name__)

@app.route("/")
def hello():
    randomNameGenerator = rng()
    r.connect().repl()
    results = r.table("authors").order_by(r.desc("score")).limit(10).run()
    for idx,result in enumerate(results):
        try:
            result['username']=getNameOfWatch(randomNameGenerator,result['username'])
        except KeyError:
            pass
        result['index']=idx

    return render_template('bshighScores.html', scores=results)


@app.route('/json', methods=['POST'])
def json():
		
    data=request.get_json()
    print data
    r.connect().repl()
    try:
        r.db("test").table_create("authors").run()
    except r.ReqlOpFailedError:
        pass
    
    r.table("authors").insert(data).run()
    
    return jsonify(data)

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
        print "in here!"
        newData={'username':name,'friendly':randomNameGenerator.getName()}
        r.table("nameMapping").insert(newData).run()
        return newData['friendly']


if __name__ == "__main__":
    #r.connect().repl()
    #r.db("test").table_create("authors").run()
    app.debug = True
    app.run('0.0.0.0')
