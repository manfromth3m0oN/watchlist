from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_cors import CORS
from mongoengine.fields import DictField, IntField, StringField
from mongoengine.connection import connect
from mongoengine import Document

# Define flask app
app = Flask(__name__)

#Enable crossorigin
CORS(app)

# Define jwt manager
app.config['JWT_SECRET_KEY'] = '\xc5U\xe8\xf5g\x12\x0b\xbc\xe2\xd78\xb1\x05\xa7\xce\xd5`~\xba\n-}\xb6'
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400

# Define mongo connection
connect('watchlist')

# Create the user class
class User(Document):
    email = StringField(required=True)
    username = StringField(required=True)
    passwordHash = StringField(required=True)

# Create a class to define watchlist properties
class List(Document):
    name = StringField(required=True, unique=True)
    owner = StringField(required=True)
    length = IntField(required=True, default=0)
    titles = DictField(default={})


# Registers a user
@app.route('/register', methods=['POST'])
def register():
    res = request.json
    if res['email'] and res['username'] and res['passwordHash']:
        User(email = res['email'], username=res['username'], passwordHash=res['passwordHash']).save()
        return 'User registered'
    else:
        return 'Registration missing attribute'

# Logs a user in
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    passwordHash = request.json.get('passwordHash', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not passwordHash:
        return jsonify({"msg": "Missing password parameter"}), 400

    if User.objects(username=username, passwordHash=passwordHash):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Incorrect password"})

# This route is just testing the JWT access system
@app.route('/test', methods=['GET'])
@jwt_required
def test():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# create a list for a user
@app.route('/createList', methods=['POST'])
@jwt_required
def createList():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    name = request.json.get('name', None)
    current_user = get_jwt_identity()
    if not name:
        return jsonify({"msg": "Missing name parameter"}), 400
    List(name=name, owner=current_user).save()
    return jsonify({"msg": "List "+name+" created successfully"}), 200

# Used to add a title or selection of titles to a list
@app.route('/addToList', methods=['POST'])
@jwt_required
def addToList():
    current_user = get_jwt_identity()
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    name = request.json.get('name', None)
    restitles = request.json.get('titles', None)
    if not restitles:
        return jsonify({"msg": "Missing titles parameter"}), 400
    if not name:
        return jsonify({"msg": "Missing name parameter"}), 400
    wlist = List.objects(name=name)
    if wlist:
        wlist = wlist.get(name=name)
        if wlist.owner == current_user:
            oldlist = wlist.titles
            newlist = {}
            for title in restitles:
                newlist.update({title: {"watched": False}})
            oldlist.update(newlist)
            wlist.titles = oldlist
            wlist.length = len(oldlist)
            wlist.save()
            return jsonify({"msg": "List "+name+" successfully updated with "+str(len(restitles))+" titles"})
        else:
            return jsonify({"msg": "you are not authenitcated as the correct user to edit this list"})

# Update the watched status for a given title within a list
@app.route('/updateWatchedStatus', methods=['POST'])
@jwt_required
def updateWatchedStatus():
    current_user = get_jwt_identity()
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    name = request.json.get('name', None)
    showTitle = request.json.get('showTitle', None)
    watchedStatus = request.json.get('watchedStatus', None)
    if not name:
        return jsonify({"msg": "Missing name parameter"}), 400
    if not showTitle:
        return jsonify({"msg": "Missing showTitle parameter"}), 400
    if not watchedStatus:
        return jsonify({"msg": "Missing watchedStatus parameter"}), 400
    wlist = List.objects(name=name)
    if wlist:
        wlist = wlist.get(name=name)
        if wlist.owner == current_user:
            oldlist = wlist.titles
            oldlist.update({showTitle: {"watched": watchedStatus}})
            wlist.titles = oldlist
            wlist.save()
            return jsonify({"msg": "List updated Successfully"})
        else:
            return jsonify({"msg": "You are not authenitcated as the correct user to edit this list"})

#gets the 3 top lists from the DB
@app.route('/head', methods=['GET'])
def head():
    objs = {}
    for obj in List.objects.limit(3):
        oid = str(obj.id)
        name = obj.name
        owner = obj.owner
        titles = obj.titles
        objs.update({oid: {"name": name, "owner": owner, "titles": titles}})
    return jsonify(objs)

# Gets a list with a certian name
@app.route('/get/<listName>', methods=['GET'])
def getList(listName):
    listobj = List.objects(name=listName)
    if listobj:
        listobj = listobj.get(name=listName)
        return jsonify(listobj.to_json())
    else:
        return jsonify({"msg": "no list with that name exists"})

@app.route('/removeTitle', methods=['POST'])
@jwt_required
def removeTitle():
    if not request.is_json:
        return jsonify({"msg": "no reqest data"})
    listname = request.json.get('list')
    title = request.json.get('title')
    if not listname:
        return jsonify({"msg": "Missing list parameter"})
    if not title:
        return jsonify({"msg": "Missing title parameter"})
    listobj = List.objects(name=listname)
    if listobj:
        listobj = listobj.get(name=listname)
        if title in listobj.titles:
            del listobj.titles[title]
            listobj.save()
            return jsonify({"msg": "title "+title+" removed from "+listname})
        else:
            return jsonify({"msg": "requested title not in list"})

@app.route('/getAll', methods=['GET'])
def getAll():
    return jsonify(List.objects().to_json())

@app.route('/getAll/<user>')
def getAllUser(user):
    return jsonify(List.objects(owner=user).to_json())

app.run(debug=True, host='0.0.0.0')