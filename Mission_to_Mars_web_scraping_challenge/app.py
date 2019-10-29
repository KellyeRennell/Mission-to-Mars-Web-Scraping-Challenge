from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars")

# Creating root route, that will query mongo db and pass the compiled mars data into the html template(index.html) for displaying the data
@app.route("/")
def home():

    news_data = mongo.db.mars.find_one()
    
    return render_template("index.html", mars = news_data)


@app.route("/scrape")
def scrape():
    
    news_data = scrape_mars.scrape()
    mongo.db.mars.update({}, news_data, upsert = True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
