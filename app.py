from flask import Flask, render_template
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars
collection = db.mars_data

db.collection.insert( scrape())



@app.route("/")
def echo():
    mars_dict = list(db.collection.find())[0]
    return render_template("index.html", main_image = mars_dict["featured_image_url"], headline = mars_dict["headline"], teaser = mars_dict["teaser"], weather =mars_dict["mars_weather"]) 

@app.route("/scrape")
def pull_data():
    db.collection.remove()
    db.collection.insert( scrape())
    mars_dict = list(db.collection.find())[0]
    return render_template("index.html", main_image = mars_dict["featured_image_url"], headline = mars_dict["headline"], teaser = mars_dict["teaser"], weather =mars_dict["mars_weather"]) 


if __name__ == "__main__":
    app.run(debug=True)
