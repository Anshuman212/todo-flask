import os
from flask import Flask,Response,request,render_template
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)
MONGO_URI = os.environ.get('MONGO_URI')
#connecting to the database
try:
    mongo = pymongo.MongoClient(MONGO_URI)
    db=mongo.todoFlask
    mongo.server_info() #triggers the exception if cannot connect to database
except:
    print('cannot connect to the database')


####updating the user in the database
@app.route('/api/v1/<id>',methods=["PATCH"])
def update_task_status(id):
    try:
        dbResponse=db.tasks.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"status":request.args.get("status")}}
            )
        return Response(
            response=json.dumps({"message":"user updated"})   ,
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
        response=json.dumps({"message":"cannot update user"}),
        status=500,
        mimetype="application/json"
        )
        

#### getting all the tasks from the database
@app.route('/api/v1',methods=["GET"])
def get_task():
    try:
        data = list(db.tasks.find())
        for tsk in data:
            tsk["_id"]=str(tsk["_id"])
        return Response(
            response=json.dumps(data)   ,
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)
        return Response(
        response=json.dumps({"message":"cannot get user"}),
        status=500,
        mimetype="application/json"
        )


##### creating a new task
@app.route('/api/v1',methods=["POST"])
def create_task():
    try:
        task = {
        "task":request.args.get("task"),
        "status":request.args.get("status")
        }
        dbResponse = db.tasks.insert_one(task)
        print(dbResponse.inserted_id)
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            #response data
            response=json.dumps({"message":"user-created",
            "id":f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex: 
        #allows to print the exception
        return ex
        return Response(
            response=json.dumps({"message":"cannot create user"}),
            status=500,
            mimetype="application/json"
        )

####deleting the user 
@app.route('/api/v1/<id>',methods=["DELETE"])
def delete_task(id):
    try:
        dbResponse=db.tasks.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count==1:
            return Response(
            #response data
            response=json.dumps({"message":"user-deleted",
            "id":f"{id}"}),
            status=200,
            mimetype="application/json"
        )
        return Response(
            #response data
            response=json.dumps({"message":"user-not-found",
            "id":f"{id}"}),
            status=404,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message":"cannot delete user"}),
            status=500,
            mimetype="application/json"
        )



if __name__=="__main__":
    app.run(port=5000,debug=True)