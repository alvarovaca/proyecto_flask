from flask import Flask, render_template, request
import requests
import os
app = Flask(__name__)
app.config["key"]=os.environ["key"]
app.config["URL_BASE"]="https://euw1.api.riotgames.com/lol/"

@app.route('/status',methods=["GET"])
def status():
    payload = {'api_key':app.config["key"]}
    r=requests.get(app.config["URL_BASE"]+"status/v3/shard-data", params=payload)
    if r.status_code == 200:
        return render_template("status.html", peticion=r.json())
    else:
        return render_template("status.html")

@app.route('/top',methods=["GET","POST"])
def top():
    tiers=["CHALLENGER","GRANDMASTER","MASTER","DIAMOND","PLATINUM","GOLD","SILVER","BRONZE","IRON"]
    tierstr=["CHALLENGER","GRAN MAESTRO","MAESTRO","DIAMANTE","PLATINO","ORO","PLATA","BRONCE","HIERRO"]
    divisions=["I","II","III","IV"]
    if request.method=="GET":
        return render_template("top.html", tiers=tiers, tierstr=tierstr, divisions=divisions)
    else:
        tier=request.form.get("tier")
        division=request.form.get("division")
        page=request.form.get("page")
        payload = {'api_key':app.config["key"], 'page':page}
        r=requests.get(app.config["URL_BASE"]+"league-exp/v4/entries/RANKED_SOLO_5x5/"+tier+"/"+division+"", params=payload)
        if r.status_code == 200 and r.json():
            return render_template("top.html", tiers=tiers, tierstr=tierstr, divisions=divisions, peticion=r.json(), tier=tierstr[tiers.index(tier)], division=division, page=page)
        #url=r.url.replace("page="+str(payload["page"])+"","page="+str(payload["page"]+1)+"")
        else:
            return render_template("top.html", tiers=tiers, tierstr=tierstr, divisions=divisions, fallo=True, tier=tierstr[tiers.index(tier)], division=division, page=page)

#port=os.environ["PORT"]
#app.run('0.0.0.0', int(port), debug=False)
app.run(debug=True)