
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid 
from flask import Flask, request, jsonify, abort, render_template

# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'

todo_1_id = '651813d1-d979-4711-a245-dab1761dbe11'
todo_2_id = '24623c25-6b80-4365-bb6d-a7c865014c33'
todo_3_id = '11b04e00-03bc-457d-8d31-0c67e4866f56'
todo_4_id = '46b06e00-03bc-452d-8d11-0c67e2866ff3'

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

#landing page with rendered html template
@app.route('/')
def index():
    return render_template("index.html", todo_lists=todo_lists, todos=todos)


#Endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)

    if request.method == 'GET':
        # get todo list with the given id
        print('Returning todo list...')
        return jsonify(next(l for l in todo_lists if l["id"] == list_id )), 200
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200


#Endpoint for adding a new list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)

    #if the given list is invalid, return status code 400
    if not new_list:
        abort(400)

    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = str(uuid.uuid4()) #cast uuid to string
    todo_lists.append(new_list)
    return jsonify(new_list), 200


#Endpoint for getting all lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200


#Endpoint for getting all entries in a todo list
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_all_entries(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    elif request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning entries...')
        return jsonify([i for i in todos if i['list'] == list_id]), 200

  
# define endpoint for adding a new entry to a list
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)

    #if the given list is invalid, return status code 400
    if not list_item:
        abort(400)

    elif request.method == 'POST':
        # add new entry for the todo list with the given id
        new_entry = request.get_json(force=True)
        print('Got new entry to be added: {}'.format(new_entry))
        new_entry['id'] = str(uuid.uuid4()) #cast uuid to string
        new_entry['list'] = str(list_id) #cast list_id to string
        todos.append(new_entry)
        return jsonify(new_entry), 200


#Endpoint for updating an existing entry or to delete an existing entry in a todo list
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def handle_entry(list_id, entry_id):
    
    #find entry depending on given entry id
    entry_item = None
    for entry in todos:
        if entry['id'] == entry_id and entry['list'] == list_id:
            entry_item = entry
            break
    #if the given entry id is invalid, return status code 404
    if not entry_item:
        abort(404)

    if request.method == 'PUT':
        #update entry with the given object
        print('Updated given entry')
        todos.remove(entry_item)
        entry_item = request.get_json(force=True)
        entry_item['id'] = entry_id
        entry_item['list'] = list_id
        todos.append(entry_item)
        return jsonify(entry_item), 200
    elif request.method == 'DELETE':
        #delete entry with the given object
        print('Deleted given entry')
        todos.remove(entry_item)
        return '', 200

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)