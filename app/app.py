"""importing the following modules"""
from flask import Flask, jsonify, request, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = 'super_secret_key'  # Secret key for session management

# In-memory database to store items
items_db = {}

# User authentication credentials (dummy data for demonstration)
valid_cred = {
    'user': 'admin',
    'pwd': 'password'
}

def generate_item_id():
    """Generate a unique item ID."""
    return str(len(items_db) + 1)


@app.route('/login', methods=['POST'])
def login():
    """Authenticate user."""
    data = request.json
    if 'user' in data and 'pwd' in data:
        if data['user'] == valid_cred['user'] and data['pwd'] == valid_cred['pwd']:
            session['logged_in'] = True
            return jsonify({'message': 'Login successful'}), 200
        return jsonify({'message': 'Invalid user or password'}), 401
    return jsonify({'message': 'user and password are required'}), 400

@app.route('/logout', methods=['POST'])
def logout():
    """Logout user."""
    if session.get('logged_in'):
        session.pop('logged_in', None)
        return jsonify({'message': 'Logged out successfully'}), 200
    return jsonify({'message': 'Unauthorized access'}), 401

@app.route('/', methods=['GET'])
def get_items():
    """Get all items."""
    return jsonify(list(items_db.values()))

@app.route('/<item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID."""
    item = items_db.get(item_id)
    if item:
        return jsonify(item)
    return jsonify({'message': 'Item not found'}), 404

@app.route('/', methods=['POST'])
def create_item():
    """Create a new item."""
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized access'}), 401
    data = request.json
    if 'name' in data:
        item_id = generate_item_id()
        item = {'id': item_id, 'name': data['name']}
        items_db[item_id] = item
        return jsonify(item), 201
    return jsonify({'message': 'Name is required'}), 400

@app.route('/<item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item."""
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized access'}), 401
    data = request.json
    item = items_db.get(item_id)
    if item:
        item['name'] = data.get('name', item['name'])
        items_db[item_id] = item
        return jsonify(item)
    return jsonify({'message': 'Item not found'}), 404

@app.route('/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item."""
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized access'}), 401
    if item_id in items_db:
        del items_db[item_id]
        return jsonify({'message': 'Item deleted'})
    return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
