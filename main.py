from flask import Flask
import pymongo


app = Flask(__name__)

# db
client = pymongo.MongoClient("test-sep-mongo", 27017)
db = client["app"]
col = db["log"]

@app.route("/")
def hello():
    col.insert_one({})
    items = col.find().count()
    return f"Total items in db: {items}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)