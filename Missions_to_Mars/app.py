#import project dependencies

import numpy as np
import os
from flask import Flask, jsonify,render_template
import scrape_mars as scrape

# Flask Setup
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# add the default route
@app.route("/")
def index():
    resultCode, data = scrape.GetData()
    if (resultCode == "-1")
    return (f"{data}")

    return render_template('index.html', data=data)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scrape():

    # scrape.scrape() is a custom function that we've defined in the scrape_mars.py file within this directory
    resultCode, result = scrape.scrape()
    if (resultCode == "-1") :
        return(f"{result}")
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)
