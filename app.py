# Task Management Flask API by Aryan Bhan
from flask import Flask, jsonify, request
app = Flask(__name__)

# List Used to Store Tasks
todo = []

# Size of Page for Pagination
size = 5

# Creating a Task
@app.route('/todo', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    status = data.get('status', 'Incomplete')
    task_id = len(todo) + 1
    
    task = {
        'id': task_id,
        'title': title,
        'description': description,
        'due_date': due_date,
        'status': status
    }
    
    todo.append(task)
    print(todo)
    return jsonify(todo)
   

# Retrieving a Task by ID
@app.route('/todo/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in todo if task['id'] == task_id), None)
    
    if task:
        return jsonify(task)
    
    return jsonify({'error': 'Task not found'}), 404


# Updating a Task by ID
@app.route('/todo/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in todo if task['id'] == task_id), None)
    
    if task:
        data = request.get_json()
        task['title'] = data.get('title', task['title'])
        task['description'] = data.get('description', task['description'])
        task['due_date'] = data.get('due_date', task['due_date'])
        task['status'] = data.get('status', task['status'])
        
        return jsonify(task)
    
    return jsonify({'error': 'Task not found'}), 404


# Deleting a Task By ID
@app.route('/todo/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global todo
    todo = [task for task in todo if task['id'] != task_id]
    
    return jsonify({'message': 'Task deleted'})


# Retrieve all Tasks
@app.route('/todo', methods=['GET'])
def list_todo():
    #Pagination
    args = request.args
    page = args.get('page')
    
    if not page:
        return jsonify(todo)
    else:
        #Pagination Logic
        start_index = (int(page) - 1)* size
        if start_index > len(todo):
            start_index = 0
        end_index = start_index + size
        return jsonify(todo[start_index:end_index])  

# Main Function
if __name__ == '__main__':
    app.run()