from flask import Flask, request,jsonify,render_template

import rethinkdb as r


app = Flask(__name__)

@app.route("/")
def hello():
    r.connect().repl()
    results = r.table("authors").order_by(r.desc("score")).limit(10).run()

    return render_template('highScores.html', scores=results)


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



if __name__ == "__main__":
    #r.connect().repl()
    #r.db("test").table_create("authors").run()
    app.debug = True
    app.run()
