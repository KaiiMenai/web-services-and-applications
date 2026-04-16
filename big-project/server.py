from flask import Flask, jsonify, request, abort
#from flask_cors import CORS, cross_origin
app = Flask(__name__)
#cors = CORS(app) # allow CORS for all domains on all routes.
#app.config['CORS_HEADERS'] = 'Content-Type'

from taskDAO import taskDAO

app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

@app.route('/')
#@cross_origin()
def index():
    return "Let's, Do it!"

#curl "http://127.0.0.1:5000/tasks"
@app.route('/tasks')
#@cross_origin()
def getAll():
    #print("in getall")
    results = taskDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/tasks/2"
@app.route('/tasks/<int:id>')
#@cross_origin()
def findById(id):
    foundTask = taskDAO.findByID(id)

    return jsonify(foundTask)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Task Name\":\"hello\",\"Description\":\"someone\",\"Due Date\":22/05/2026}" http://127.0.0.1:5000/tasks
@app.route('/tasks', methods=['POST'])
#@cross_origin()
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    task = {
        "Task Name": request.json['task_name'],
        "Description": request.json['description'],
        "Due Date": request.json['due_date'],
    }
    addedtask = taskDAO.create(task)
    
    return jsonify(addedtask)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Task Name\":\"hello\",\"Description\":\"someone\",\"Due Date\":22/05/2026}" http://127.0.0.1:5000/tasks/1
@app.route('/tasks/<int:id>', methods=['PUT'])
#@cross_origin()
def update(id):
    foundTask = taskDAO.findByID(id)
    if not foundTask:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'due_date' in reqJson and type(reqJson['due_date']) is not int:
        abort(400)

    if 'task_name' in reqJson:
        foundTask['task_name'] = reqJson['task_name']
    if 'description' in reqJson:
        foundTask['description'] = reqJson['description']
    if 'due_date' in reqJson:
        foundTask['due_date'] = reqJson['due_date']
    taskDAO.update(id,foundTask)
    return jsonify(foundTask)
        

    

@app.route('/tasks/<int:id>' , methods=['DELETE'])
#@cross_origin()
def delete(id):
    taskDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)