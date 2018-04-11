 #https://github.com/rianrajagede/flask-mongodb

#https://gist.github.com/cuppster/5145500

#MongoImport mongoimport --db records --collection outfits --type csv --file outfit.csv --headerline 
from flask import Flask, render_template,request,redirect,url_for,jsonify,Response,send_file
from pymongo import MongoClient
import json
import base64
from bson.json_util import dumps,loads
import similar_images_AE
from PIL import Image
from bson import json_util
from werkzeug import secure_filename
import glob
import requests
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
import scipy.misc
from urllib.request import urlopen
from io import StringIO,BytesIO
from shutil import copyfile
import random
#https://stackoverflow.com/questions/41708892/storing-some-small-files-with-mongodb-in-flask-without-gridfs
# config system
app = Flask(__name__)
#app.config.update(dict(SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))
client = MongoClient('localhost:27017')

mongo = client.records



#https://stackoverflow.com/questions/20718251/how-to-retrieve-image-files-from-mongodb-to-html-page


#@app.route('/', methods=['GET','POST'])        
#def main():

@app.route('/encodeImages')
def encodeImages():
    data = mongo.bottom.find()
    i=0
    for val in data:
        content=requests.get(val['product_image']).content
        encoded_string =  base64.b64encode(content)
        #print(encoded_string)
        #update all document we add {}
        
        mongo.bottom.update({'_id' : val['_id']}, {'$set' : {'image' : encoded_string }})
        i=i+1
        print(i)

    return 'encoded ok '    


    
@app.route('/insert', methods=['POST','GET'])
def insert():
    if request.method=='POST' :
        input_file = request.files['inputFile'] 
        filename=secure_filename(input_file.filename)
        print('filename')
        print(filename)
        encoded_string =  base64.b64encode(input_file.read())
        print(type(encoded_string))
        files_collection = mongo.files_collection  # connect to mongodb collection
        files_collection.insert_one({"id":filename,"image":encoded_string})

    return render_template('index.html')    

@app.route('/insertTops/<event>', methods=['POST','GET'])
def insertTops(event):
    if request.method=='POST' :
        input_file = request.files.getlist("inputFile")
        print(type(input_file))
        col='top_'+event
        files_collection = mongo[col] # connect to mongodb collection
        for file in input_file:
            filename=secure_filename(file.filename)
            print(filename)
            encoded_string =  base64.b64encode(file.read())
           #print(type(encoded_string))
            
            files_collection.insert_one({"id":filename,"image":encoded_string})

    return render_template('insertManyFiles.html')  
    
@app.route('/retrieve')
def retrieve():       
    #data = mongo.bottom.find({"product_occasion":"casual"})
    #data = mongo.top_casual.find()
    data = mongo.output.find()
    images = []
    ids=[]
    for val in data:
        for i in range(0,4):
            img= val['image'+str(i)]
            decode=img.decode()
            print(type(decode))
            images.append(decode)
       
    return render_template('image.html',imagedecod=images)   


@app.route('/wardrobe')
def wardrobe():       
    data =mongo.wardrobe.find()
    
    return jsonify(dumps(data))      
               
        
@app.route('/retrieveSimilar/<type>')
def retrieveSimilar(type):       
   #data = mongo.top.find({'product_occasion':'casual'})
    ''' response = Response(
        response=[json.dumps(doc, default=json_util.default) for doc in data],
        status=200,
        mimetype='application/json'
    )
    return response '''
    images = []
    print('aaaa')
   
    
    data =mongo[type].find({'product_occasion':'casual'})
    ''' for val in data:
        img= val['image']
        
        
        decode=img.decode()
        mongo[type].update({'_id' : val['_id']}, {'$set' : {'imageDecoded' : decode}}) '''
    return jsonify(dumps(data))    
    #return render_template('imageSimilar.html',imagedecod=images)    
    '''
    content=requests.get(q['product_image']).content
    content= Image.open(BytesIO(content))
        content.save('C:/Users/utilisateur/Documents/GitHub/flask-mongodb/test/'+str(q['product_id'])+'.jpg')            
       return send_file(Image.open(BytesIO(content)),
                     attachment_filename='C:/Users/utilisateur/Documents/GitHub/flask-mongodb/test/logo.jpg',
                     mimetype='image/jpeg') 
        '''  

@app.route('/script/<type>', methods=['GET', 'POST'])
def script(type):
    if request.method=='POST' :
        req_data = request.get_json()
        id = req_data['id']
        print('id')
        print(id)
    q = mongo[type].find_one({'_id':ObjectId(id)})
    
    
    #query=mongo.top.find( {'product_id':66936498})
    images=[]
    
    
    
        
    path='C:/Users/utilisateur/Desktop/scraping/images/'+q['product_occasion']+'/'+q['type']+'/'
    
    copyfile(path+str(q['product_id'])+'.jpg', 'C:/Users/utilisateur/Documents/GitHub/flask-mongodb/test/'+str(q['product_id'])+'.jpg')
       
    with open(path+str(q['product_id'])+'.jpg', "rb") as imageFile:
        encoded_string =  base64.b64encode(imageFile.read())
    images.append(encoded_string.decode())
    val='db'    
    similar_images_AE.main(q,val)
        
    #top= mongo.top.find_one({'_id':ObjectId(q['_id'])})
    outfit=mongo.outfits.find()
        
        
    
        

    
    for out in outfit:
        if(q['type']=='top'):
            if(out['top_id'] == q['product_id']):
                #complete a query=top
                id=out['bottom_id']
                data = mongo.bottom.find() 
                
        elif(q['type']=='bottom'):
            #complete query=bottom
            if(out['bottom_id'] == q['product_id']):
                id=out['top_id']
                data=mongo.top.find()
                
    item=''    
    for d in data :
        if(id == d['product_id']) :
            item=d
            
           
            
            
    #similiar_images=mongo.output.find_one({'_id':q['_id']})
   # for i in range(5):
       # images.append(similiar_images['image'+str(i)].decode())
           
    
    #item similar
    src= 'C:/Users/utilisateur/Desktop/scraping/images/'+item['product_occasion']+'/'+item['type']+'/'+ str(item['product_id'])+'.jpg'
    dest='C:/Users/utilisateur/Documents/GitHub/flask-mongodb/test/'+ str(item['product_id'])+'.jpg'
    
    copyfile(src,dest)
    ''' content=requests.get(bottom['product_image']).content
    content= Image.open(BytesIO(content))
    content.save('C:/Users/utilisateur/Documents/GitHub/flask-mongodb/test/'+str(bottom['product_id'])+'.jpg')            
   '''  
    val='wardrobe'
    similar_images_AE.main(item,val)

    
    item_sim= mongo.output.find_one({'_id':item['_id']})
    
    for j in range (5):
        images.append(item_sim['image'+str(j)].decode()) 
   
        

    return jsonify({"outfit":images})     
           

#goooood https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
@app.route('/send', methods=['POST'])  
def send():
    if request.method=='POST' :
        req_data = request.get_json()
        firstParam = req_data['id']
        type=req_data['type']
        print(firstParam)
       
        item= mongo[type].find_one({'_id':ObjectId(firstParam)})
        path='C:/Users/utilisateur/Desktop/scraping/images/'+item['product_occasion']+'/'+item['type']+'/'
    
        copyfile(path+str(item['product_id'])+'.jpg', 'C:/Users/utilisateur/Documents/GitHub/flask-mongodb/wardrobe/'+item['product_occasion']+'/'+item['type']+'/'+str(item['product_id'])+'.jpg')
    
        entry = mongo.wardrobe # connect to mongodb collection
        entry.insert(item)
     
    
    return jsonify(dumps(item))

@app.route('/combine', methods=['POST'])  
def combine():
    if request.method=='POST' :
        req_data = request.get_json()
        occasion = req_data['occasion']
        print('occasion')
        print(occasion)
       
       
        
        count = mongo.wardrobe.count()
        q=mongo.wardrobe.find({'product_occasion':occasion})[random.randrange(count)]
        print("hooo")
        print(q)
       
    
        images=[]
        
        
        path='C:/Users/utilisateur/Desktop/scraping/images/'+q['product_occasion']+'/'+q['type']+'/'
        
        copyfile(path+str(q['product_id'])+'.jpg', 'C:/Users/utilisateur/Documents/GitHub/flask-mongodb/test/'+str(q['product_id'])+'.jpg')
        
        with open(path+str(q['product_id'])+'.jpg', "rb") as imageFile:
            encoded_string =  base64.b64encode(imageFile.read())
        images.append(encoded_string.decode())
        val='db'    
        similar_images_AE.main(q,val)
                
        
        outfit=mongo.outfits.find()
        
        for out in outfit:
            if(q['type']=='top'):
                if(out['top_id'] == q['product_id']):
                    #complete a query=top
                    id=out['bottom_id']
                    data = mongo.bottom.find() 
                    
            elif(q['type']=='bottom'):
                #complete query=bottom
                if(out['bottom_id'] == q['product_id']):
                    id=out['top_id']
                    data=mongo.top.find()
                    
        item=''    
        for d in data :
            if(id == d['product_id']) :
                item=d
                
            
        print('item')        
        print(item['type'])        
        #similiar_images=mongo.output.find_one({'_id':q['_id']})
    # for i in range(5):
        # images.append(similiar_images['image'+str(i)].decode())
            
        
        #item similar
        src= 'C:/Users/utilisateur/Desktop/scraping/images/'+item['product_occasion']+'/'+item['type']+'/'+ str(item['product_id'])+'.jpg'
        dest='C:/Users/utilisateur/Documents/GitHub/flask-mongodb/test/'+ str(item['product_id'])+'.jpg'
        
        copyfile(src,dest)
        ''' content=requests.get(bottom['product_image']).content
        content= Image.open(BytesIO(content))
        content.save('C:/Users/utilisateur/Documents/GitHub/flask-mongodb/test/'+str(bottom['product_id'])+'.jpg')            
    '''  
        val='wardrobe'
        similar_images_AE.main(item,val)

        
        item_sim= mongo.output.find_one({'_id':item['_id']})
        
        for j in range (5):
            images.append(item_sim['image'+str(j)].decode()) 
    
            

        return jsonify({"outfit":images})     
               
       
if __name__=='__main__':
    app.run(debug=True)