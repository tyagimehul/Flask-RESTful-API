from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from flask_jsonpify import jsonpify
import pandas as pd
import json

app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello_world():
    return 'Welcome to Notes App.\n'

read_file=pd.read_csv(r"./notes_data.csv")
df = pd.DataFrame(read_file,columns=['name', 'color_code', 'message'])

@app.route('/see', methods=["GET"])
def seeNotes():
    if request.method=='GET':
        jsonfiles = json.loads(df.to_json(orient='records'))
        return jsonpify(jsonfiles)    
    else:
        return jsonify("Wrong METHOD!! ")

@app.route('/fetchnote', methods=["POST"])
def makeNotes():
    if request.method=='POST':
        posted_data = request.get_json() #to get data from post body
        data_name = posted_data['Name']
       
        df_display=(df.loc[df["name"]==data_name])
        jsonfiles = json.loads(df_display.to_json(orient='records'))
        return jsonpify(jsonfiles) 
    else:
        return jsonify("incorrect type of")


@app.route('/addnote', methods=["POST"])
def addNotes():
    if request.method=='POST':
        posted_data = request.get_json() #to get data from post body
        data_name = posted_data['Name']
        data_color = posted_data['Color']
        data_message = posted_data['Message']
        df.loc[len(df.index)] = [data_name,data_color,data_message]
        df.to_csv("./notes_data.csv")
        return  "Successfull"
    else:
        return "Unsuccessfull"

	

@app.route('/delete/<id>',methods=["DELETE"])
def deleteNotes(id):
    if request.method=='DELETE':
        df.drop(df.loc[df['name']==id].index, inplace=True)
        df.to_csv("./notes_data.csv")
        return ("Deleted entry for " + id + '\n')
    else:
        return ("SORRY")


@app.route('/updatecolor',methods=["PATCH"])
def updateNotes():
    if request.method=='PATCH':
        posted_data = request.get_json()
        updated_color = posted_data['color_code']
        data_name = posted_data['Name']
        get_index = df.loc[df.name==data_name].index
        df.iloc[get_index,[1]]=updated_color
        df.to_csv("./notes_data.csv")
        return ("Updated color of " + data_name + " to " + updated_color + '\n')
    else:
        return ("SORRY")




class HelloWorld(Resource):
    def get(self):
        return ("Hello kiddo!")

api.add_resource(HelloWorld, '/hello')


if __name__ == '__main__':
    app.run(debug=True)
