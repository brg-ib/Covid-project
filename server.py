from flask import Flask, render_template
from pymongo import MongoClient

mongoURL = "mongodb+srv://ynov:ynov@cluster0-dfkq3.azure.mongodb.net/covid?retryWrites=true&w=majority"

client = MongoClient(mongoURL)


try:
    print("MongoDB version is %s" % client.server_info()["version"])
except pymongo.errors.OperationFailure as error:
    print(error)
    quit(1)

db = client.covid


def get_country(db):
    return db.data.find()


# fivestar = db.data.find()

# for o in fivestar:
#     print(o)


recuperationParDate = db.world.aggregate(
    [{"$group": {"_id": {"day": "$Date"}, "inf_sum": {"$sum": "$Infections"}}}]
)


for date in recuperationParDate:
    print(date)


app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

