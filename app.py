from flask import Flask, render_template, request, redirect
import requests
import os
app = Flask(__name__)
app.config["key"]=os.environ["key"]
app.config["mantenimiento"]=os.environ["mantenimiento"]
app.config["URL_BASE"]="https://euw1.api.riotgames.com/lol/"
app.config["URL_BASE_2"]="http://ddragon.leagueoflegends.com/cdn/10.10.3216176/"

@app.route('/',methods=["GET"])
def inicio():
    if app.config["mantenimiento"] != "1":
        return render_template("inicio.html")
    else:
        return render_template("mantenimiento.html")

@app.route('/status',methods=["GET"])
def status():
    if app.config["mantenimiento"] != "1":
        payload = {'api_key':app.config["key"]}
        r=requests.get(app.config["URL_BASE"]+"status/v3/shard-data", params=payload)
        if r.status_code == 200:
            return render_template("status.html", peticion=r.json())
        else:
            return render_template("status.html")
    else:
        return render_template("mantenimiento.html")

@app.route('/invocador',methods=["GET"])
def invocador():
    if app.config["mantenimiento"] != "1":
        return render_template("invocador.html")
    else:
        return render_template("mantenimiento.html")

@app.route('/procesar',methods=["POST"])
def procesar():
    summoner=request.form.get("invocador")
    radio=request.form.get("radio")
    return redirect("/invocador/"+radio+"/"+summoner)

@app.route('/invocador/historial/<summoner>',methods=["GET"])
def historial(summoner):
    if app.config["mantenimiento"] != "1":
        payload = {'api_key':app.config["key"]}
        r=requests.get(app.config["URL_BASE"]+"summoner/v4/summoners/by-name/"+summoner+"", params=payload)
        if r.status_code == 200:
            accountid1=r.json()["accountId"]
            history=requests.get(app.config["URL_BASE"]+"match/v4/matchlists/by-account/"+accountid1+"", params=payload)
            accountid2=r.json()["id"]
            ingame=requests.get(app.config["URL_BASE"]+"spectator/v4/active-games/by-summoner/"+accountid2+"", params=payload)
            if history.status_code == 200:
                champs=requests.get(app.config["URL_BASE_2"]+"data/en_US/champion.json")
                return render_template("historial.html", peticion=history.json(), nombre=summoner, champs=champs.json(), icono=r.json()["profileIconId"], nivel=r.json()["summonerLevel"], ingame=ingame.status_code)
            else:
                return render_template("historial.html", nombre=summoner, fallo2=True)
        else:
            return render_template("historial.html", nombre=summoner, fallo1=True)
    else:
        return render_template("mantenimiento.html")

@app.route('/invocador/partida/<summoner>',methods=["GET"])
def partida(summoner):
    if app.config["mantenimiento"] != "1":
        payload = {'api_key':app.config["key"]}
        r=requests.get(app.config["URL_BASE"]+"summoner/v4/summoners/by-name/"+summoner+"", params=payload)
        if r.status_code == 200:
            accountid=r.json()["id"]
            partida=requests.get(app.config["URL_BASE"]+"spectator/v4/active-games/by-summoner/"+accountid+"", params=payload)
            if partida.status_code == 200:
                champs=requests.get(app.config["URL_BASE_2"]+"data/en_US/champion.json")
                spells=requests.get(app.config["URL_BASE_2"]+"data/en_US/summoner.json")
                return render_template("partida.html", peticion=partida.json(), nombre=summoner, champs=champs.json(), spells=spells.json(), icono=r.json()["profileIconId"])
            else:
                return render_template("partida.html", nombre=summoner, fallo2=True)
        else:
            return render_template("partida.html", nombre=summoner, fallo1=True)
    else:
        return render_template("mantenimiento.html")

@app.route('/top',methods=["GET","POST"])
def top():
    if app.config["mantenimiento"] != "1":
        tiers=["CHALLENGER","GRANDMASTER","MASTER","DIAMOND","PLATINUM","GOLD","SILVER","BRONZE","IRON"]
        tierstr=["CHALLENGER","GRAN MAESTRO","MAESTRO","DIAMANTE","PLATINO","ORO","PLATA","BRONCE","HIERRO"]
        divisions=["I","II","III","IV"]
        if request.method=="GET":
            return render_template("top.html", tiers=tiers, tierstr=tierstr, divisions=divisions)
        else:
            tier=request.form.get("tier")
            division=request.form.get("division")
            page=int(request.form.get("page"))
            payload = {'api_key':app.config["key"], 'page':page}
            r=requests.get(app.config["URL_BASE"]+"league-exp/v4/entries/RANKED_SOLO_5x5/"+tier+"/"+division+"", params=payload)
            if r.status_code == 200 and r.json():
                return render_template("top.html", tiers=tiers, tierstr=tierstr, divisions=divisions, peticion=r.json(), tier=tierstr[tiers.index(tier)], division=division, page=page)
            else:
                return render_template("top.html", tiers=tiers, tierstr=tierstr, divisions=divisions, fallo=True, tier=tierstr[tiers.index(tier)], division=division, page=page)
    else:
        return render_template("mantenimiento.html")

port=os.environ["PORT"]
app.run('0.0.0.0', int(port), debug=False)