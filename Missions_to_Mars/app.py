#import project dependencies

import numpy as np
import os
from flask import Flask, jsonify,render_template, redirect

import scrape_mars


# Flask Setup
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# add the default route
@app.route("/")
def index():
    mars_data = scrape_mars.GetData()
   
    return render_template('index.html', my_string="Wheeeee!", data=mars_data)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scrape():

    try :
        # scrape.scrape() is a custom function that we've defined in the scrape_mars.py file within this directory
        scrape_mars.scrape()

        # Use Flask's redirect function to send us to a different route once this task has completed.
        return redirect("/")
    except Exception as ex :
        print (ex)
        

if __name__ == '__main__':
    app.run(debug=True)
