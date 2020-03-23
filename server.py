import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymongo
from pymongo import MongoClient, DESCENDING, ASCENDING
from flask import Flask, render_template
from datetime import datetime

mongoURL = "mongodb+srv://ynov:ynov@cluster0-dfkq3.azure.mongodb.net/covid?retryWrites=true&w=majority"
client = MongoClient(mongoURL)

try:
    print("MongoDB version is %s" % client.server_info()["version"])
except pymongo.errors.OperationFailure as error:
    print("pymongo ERROR:", error)
    quit(1)

database_names = client.list_database_names()
for db_num, db in enumerate(database_names):
    print(f"Getting database : {db} -- {db_num} ")
    collection_names = client[db].list_collection_names()
    print(f"The MongoDB database {db} returned {len(collection_names)} collections.")
    for col_num, col in enumerate(collection_names):
        print(col, "--", col_num)

dbase = client.covid


app = Flask(__name__)


@app.route("/")
def homepage():
    InfeDays = list(
        dbase.world.aggregate(
            [{"$group": {"_id": "$Date", "total": {"$sum": "$Infections"}}}]
        )
    )

#Requetes
    deces = list(dbase.world.find({"Date": "2020-03-22"}, {"Deces": 1}))[0].get("Deces")
    Infections = list(dbase.world.find({"Date": "2020-03-22"}, {"Infections": 1}))[0].get("Infections")
    Gueris = list(dbase.world.find({"Date": "2020-03-22"}, {"Guerisons": 1}))[0].get("Guerisons")

    TauxDeces = list(dbase.world.find({"Date": "2020-03-22"}, {"TauxDeces": 1}))[0].get("TauxDeces")
    TauxGuerisons = list(dbase.world.find({"Date": "2020-03-22"}, {"TauxGuerisons": 1}))[0].get("TauxGuerisons")
    TauxInfections = list(dbase.world.find({"Date": "2020-03-22"}, {"TauxInfection": 1}))[0].get("TauxInfection")

    top10 = list(
        dbase.country.find({"Date": "2020-03-22"}, {"Pays": 1, "Infections": 1, "Deces":1, "_id": -1})
        .sort([("Deces", -1)])
        .limit(10)
    )

#Nbr de mort en une journée dans le monde
    lastday = list(dbase.world.find({"Date": "2020-03-21"}, {"Deces": 1}))[0].get("Deces");
    cmp = deces - lastday;

#currentDate
    datenow = datetime.today().strftime('%d/%m/%Y');

    return render_template(
        "index.html",
        InfeDays=InfeDays,
        deces=deces,
        Infections=Infections,
        Gueris=Gueris,
        TauxDeces=TauxDeces,
        TauxGuerisons=TauxGuerisons,
        TauxInfections=TauxInfections,
        top10=top10,
        cmp =cmp,
        datenow=datenow
    )


@app.route("/notebook")
def covidpage():
    return render_template("covid.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=True, debug=True)
