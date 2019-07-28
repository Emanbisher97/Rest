'''
Created on ١٤ ذو القعدة ١٤٤٠ هـ

@author: Eman Bisher
'''
import flask,json,os
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import abort

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config["DEBUG"] = True
auth = HTTPBasicAuth()

# Create object that contains dictionaries of content of member text file
team_members=[]
with open('member.txt') as f:
    for i in f:
        data = json.loads(i)
        team_members.append(data)

#data required for authentication user name and password
USER_DATA = {
    "eman": "1234"
}

#START ROUTE
#route for home or begin of rest
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Restful api</h1>
<p>A prototype API for member of team.</p>'''

#method to verify user name and password
@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

#This will return all the members we have in the object
@app.route('/team/members', methods=['GET'])
@auth.login_required
def api_all():
    return jsonify(team_members)

#This will return the information’s about the selected member
@app.route('/team/members/<int:id>', methods=['GET'])
@auth.login_required
def api_id(id):
   
    # Create an empty list for our results
    results = []
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for member in team_members:
        if member['id'] == id:
            results.append({"name":member['name'],"area":member['area']})
    
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

#this will add new member
@app.route('/team/members_add', methods=['POST'])
@auth.login_required
def api_addmember():
    namej=request.json['name']
    areaj=request.json['area']
    if type(areaj) != str or type(namej) != str :
        abort(400)
    else:
        
        id=0
        with open('member.txt') as f:
            lineList = f.readlines()
            lastline=json.loads(lineList[-1])
            id=lastline['id']
        id=int(id)+1    
        
        dict_ret = dict(id=id, name=namej, area=areaj)
        print(dict_ret)
        lstline=json.dumps(dict_ret)
        print(lstline)
        team_members.append(dict_ret)
        os.system("echo {lstline}>>member.txt".format(**locals()))
        return lstline

#his will delete specific member    
@app.route('/team/members/<int:id>', methods=['DELETE'])
@auth.login_required
def api_deletemember(id):
    data=[]
    for m in team_members:
        if(m['id']==id):
            print(m)
            team_members.remove(m)
        else:
            abort(400)
    with open('member.txt') as f:
        for i in team_members:
            data.append(json.dumps(i))
    f=open("member.txt","w")
    f.write("")
    for i in data:
        f=open("member.txt","a")
        f.write(i)
        f.write("\n")        
            
    return jsonify(team_members)

#his will update specific member
@app.route('/team/members/<int:id>', methods=['PUT'])
@auth.login_required
def api_updatemember(id):
    namej=request.json['name']
    areaj=request.json['area']
    data=[]
    if type(areaj) != str or type(namej) != str :
        abort(400)
    else:
        for m in team_members:
            if(m['id']==id):
                print(m)
                m['name']=namej
                m['area']=areaj
        with open('member.txt') as f:
            for i in team_members:
                data.append(json.dumps(i))
        f=open("member.txt","w")
        f.write("")
        for i in data:
            f=open("member.txt","a")
            f.write(i)
            f.write("\n")        
             
        return jsonify(team_members)

app.run()




