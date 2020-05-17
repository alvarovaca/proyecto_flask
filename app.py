from flask import Flask, render_template, request
import requests
import os
app = Flask(__name__)

@app.route('/status',methods=["GET"])
def status():
    URL_BASE="https://euw1.api.riotgames.com/lol/"
    key=os.environ["key"]
    payload = {'api_key':key}
    r=requests.get(URL_BASE+"status/v3/shard-data", params=payload)
    if r.status_code == 200:
        return render_template("status.html", peticion=r.json())
    return render_template("status.html")

@app.route('/top',methods=["GET","POST"])
def top():
    tiers=["CHALLENGER","GRANDMASTER","MASTER","DIAMOND","PLATINUM","GOLD","SILVER","BRONZE","IRON"]
    tierstr=["CHALLENGER","GRAN MAESTRO","MAESTRO","DIAMANTE","PLATINO","ORO","PLATA","BRONCE","HIERRO"]
    divisions=["I","II","III","IV"]
    if request.method=="GET":
        return render_template("top.html",tiers=tiers,tierstr=tierstr,divisions=divisions)
    else:
        URL_BASE="https://euw1.api.riotgames.com/lol/"
        key=os.environ["key"]
        payload = {'api_key':key, 'page':1}
        r=requests.get(URL_BASE+"status/v3/shard-data", params=payload)
        if r.status_code == 200:
            return render_template("status.html", peticion=r.json())
        return render_template("status.html")

#port=os.environ["PORT"]
#app.run('0.0.0.0', int(port), debug=False)
app.run(debug=True)