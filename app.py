from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

#Create route that renders index.html tempalte
@app.route("/")
def echo():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
	app.run(debug=True)
