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


# add the route for drug abuse statistics
@app.route('/DrugDetails')
def DrugDeathStatistics():
    drugDeathStatistics = ds.AllDataStatistics()

    # if data result  is empty return 
    if (drugDeathStatisticsByState.empty) :
        return ("Data not found")

    # return the json dataset
    drugJson = json.dumps(json.loads(drugDeathStatistics.to_json(orient='records')), indent=0)
    return (drugJson)



# add the route for drug abuse statistics by state
@app.route('/DrugDetailsByState/<state>')
def DeathStatisticsByState(state):
    try :

        # parse the input parameter
        resultCode, result = ParseStateList(state)

        #if input parameter does not match the format return error message
        if (resultCode  == "-1" ):
            return (result)  
        
        # call the method to pull the statistics by state
        drugDeathStatisticsByState = ds.AllDataStatisticsByState(resultCode, result)

        # if data result  is empty return 
        if (drugDeathStatisticsByState.empty) :
            return ("Data not found for queried states")

        # return the json dataset
        drugJson = json.dumps(json.loads(drugDeathStatisticsByState.to_json(orient='records')), indent=0)
        return (drugJson)

    except Exception as ex :
        return (ex) 




if __name__ == '__main__':
    app.run(debug=True)
