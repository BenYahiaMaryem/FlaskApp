''' #https://github.com/rianrajagede/flask-mongodb
from flask import Flask, render_template, redirect
from pymongo import MongoClient
from classes import *

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))
client = MongoClient('localhost:27017')
db = client.TaskManager

if db.settings.find({'name': 'task_id'}).count() <= 0:
    print("task_id Not found, creating....")
    db.settings.insert_one({'name':'task_id', 'value':0})

def updateTaskID(value):
    task_id = db.settings.find_one()['value']
    task_id += value
    db.settings.update_one(
        {'name':'task_id'},
        {'$set':
            {'value':task_id}
        })

def createTask(form):
    title = form.title.data
    priority = form.priority.data
    shortdesc = form.shortdesc.data
    task_id = db.settings.find_one()['value']
    
    task = {'id':task_id, 'title':title, 'shortdesc':shortdesc, 'priority':priority}

    db.tasks.insert_one(task)
    updateTaskID(1)
    return redirect('/')
 def deleteTask(form):
    key = form.key.data
    title = form.title.data

    if(key):
        print(key, type(key))
        db.tasks.delete_many({'id':int(key)})
    else:
        db.tasks.delete_many({'title':title})

    return redirect('/')

def updateTask(form):
    key = form.key.data
    shortdesc = form.shortdesc.data
    
    db.tasks.update_one(
        {"id": int(key)},
        {"$set":
            {"shortdesc": shortdesc}
        }
    )

    return redirect('/')

def resetTask(form):
    db.tasks.drop()
    db.settings.drop()
    db.settings.insert_one({'name':'task_id', 'value':0})
    return redirect('/')
 
@app.route('/', methods=['GET','POST'])
def main():
    # create form
    cform = CreateTask(prefix='cform')
    dform = DeleteTask(prefix='dform')
    uform = UpdateTask(prefix='uform')
    reset = ResetTask(prefix='reset') 

    # response
    if cform.validate_on_submit() and cform.create.data:
        return createTask(cform)
    if dform.validate_on_submit() and dform.delete.data:
        return deleteTask(dform)
    if uform.validate_on_submit() and uform.update.data:
        return updateTask(uform)
    if reset.validate_on_submit() and reset.reset.data:
        return resetTask(reset)

    # read all data
    docs = db.tasks.find()
    data = []
    for i in docs:
        data.append(i)

    return render_template('home.html', cform = cform, dform = dform, uform = uform, \
            data = data, reset = reset)

if __name__=='__main__':
    app.run(debug=True)
 '''
''' from flask import Flask, Response, send_file
from pymongo import MongoClient
import argparse
import cStringIO
import mimetypes
import requests
from PIL import Image

from pymongo import Connection
import gridfs
 
# creating connectioons for communicating with Mongo DB
# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))
client = MongoClient('localhost:27017')

db = client.EmployeeData



# Function to insert data into mongo db
def insert():
    try:
       
        
        db.Employees.insert_one(
            {
            "id": 2,
                "name":'Maaa',
            "age":20,
            "country":'Tunis'
            })
        print('\nInserted data successfully\n')
       
	
    except Exception:
        print('exception')
        
	
# Function to update record to mongo db
def update():
    try:
        criteria = raw_input('\nEnter id to update\n')
        name = raw_input('\nEnter name to update\n')
        age = raw_input('\nEnter age to update\n')
        country = raw_input('\nEnter country to update\n')

        db.Employees.update_one(
            {"id": criteria},
            {
            "$set": {
                "name":name,
                "age":age,
                "country":country
            }
            }
        )
        print("\nRecords updated successfully\n")	
        
    except Exception:
        print('exception')
	

# function to read records from mongo db
def read():
    try:
        empCol = db.Employees.find()
        print ('\n All data from EmployeeData Database \n')
        for emp in empCol:
            print (emp)

    except Exception:
	    print('exception')

# Function to delete record from mongo db
def delete():
    try:
        criteria = raw_input('\nEnter employee id to delete\n')
        db.Employees.delete_many({"id":criteria})
        print('\nDeletion successful\n')	
    except Exception:
	    print('exception')
@app.route('/', methods=['GET','POST'])        
def main():

    for i in range(1,2) :
        insert()
    return Response("{'a':'b'}", status=201, mimetype='application/json')    
	# chossing option to do CRUD operations
       
if __name__=='__main__':
    app.run(debug=True)
 '''

''' if request.method == 'POST':
        files_collection = mongo.files_collection  # connect to mongodb collection
        input_file = request.files['input_file']  # get file from front-end
        files_collection.insert_one({'data': input_file.read() })  # error occurs here
        #return 'File uploaded'
        return render_template('index.html')
    else
        files_collection = mongo.files_collection.find()  # connect to mongodb collection
        print ('\n All data from EmployeeData Database \n')
        for file in files_collection:
            print (file)
            return render_template('image.html') 
            //gooooood
     if request.method == 'POST':
        input_file = request.files['input_file'] 
        encoded_string =  base64.b64encode(input_file.read())
        print(encoded_string)
        files_collection = mongo.files_collection  # connect to mongodb collection
        files_collection.insert_one({"image":encoded_string})
        return render_template('index.html')

    else :
        #https://stackoverflow.com/questions/5368669/convert-base64-to-image-in-python
        #https://stackoverflow.com/questions/35415483/displaying-an-image-from-base64-encoded-mongodb-field-in-flask
        #https://stackoverflow.com/questions/15320221/how-to-get-a-single-value-from-a-pymongo-query-of-a-mongodb-in-python
        #https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
        #https://www.pythonanywhere.com/forums/topic/5017/
        
        data = mongo.files_collection.find()
        images = [];
        for val in data:
            img= val['image']
            print(img)
            print('aaaa')
            decode=img.decode()
            images.append(decode)
           # print(decode)
           # img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
            print('ok')
            
        return render_template('image.html',imagedecod=images)     
                  ''' 

#https://gist.github.com/cuppster/5145500


from flask import Flask, render_template,request,redirect,url_for,jsonify,Response
from pymongo import MongoClient
import json
import base64
from bson.json_util import dumps,loads
import similar_images_AE
from PIL import Image
from bson import json_util
#https://stackoverflow.com/questions/41708892/storing-some-small-files-with-mongodb-in-flask-without-gridfs
# config system
app = Flask(__name__)
#app.config.update(dict(SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))
client = MongoClient('localhost:27017')

mongo = client.records



#https://stackoverflow.com/questions/20718251/how-to-retrieve-image-files-from-mongodb-to-html-page


#@app.route('/', methods=['GET','POST'])        
#def main():
    
@app.route('/insert', methods=['POST','GET'])
def insert():
    if request.method=='POST' :
        input_file = request.files['inputFile'] 
        print(type(input_file))
        encoded_string =  base64.b64encode(input_file)
        print(type(encoded_string))
        files_collection = mongo.files_collection  # connect to mongodb collection
        files_collection.insert_one({"image":encoded_string})

    return render_template('index.html')    


@app.route('/retrieve')
def retrieve():       
    data = mongo.files_collection.find()
    
    images = []
    for val in data:
        img= val['image']
        
        print('aaaa')
        decode=img.decode()
        print(type(decode))
        images.append(decode)
        # print(decode)
        # img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
        print('ok')
        
    return render_template('image.html',imagedecod=images)      
        
@app.route('/retrieveSimilar')
def retrieveSimilar():       
    data = mongo.files_inventory.find()
    ''' response = Response(
        response=[json.dumps(doc, default=json_util.default) for doc in data],
        status=200,
        mimetype='application/json'
    )
    return response '''
    images = []
    for val in data:
        img= val['image']
        
        print('aaaa')
        decode=img.decode()
        print(type(decode))
        images.append(decode)
    return jsonify({'image': images})    
    #return render_template('imageSimilar.html',imagedecod=images)      

@app.route('/script', methods=['GET', 'POST'])
def script():
    similar_images_AE.main()   
    return redirect(url_for('retrieveSimilar'))         

#goooood https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
@app.route('/send', methods=['POST'])  
def send():
    if request.method=='POST' :
        req_data = request.get_json()
        firstParam = req_data['name']
        print(firstParam)
        entry = mongo.entry # connect to mongodb collection
        entry.insert_one({"obj":req_data})
    else:
        print(request)    
    
    return "ok" 
       
if __name__=='__main__':
    app.run(debug=True)