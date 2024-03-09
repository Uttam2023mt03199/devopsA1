from flask import Flask, jsonify, request, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = 'super_secret_key'  # Secret key for session management

# In-memory database to store items
items_db = {}

# User authentication credentials (dummy data for demonstration)
valid_credentials = {
    'username': 'admin',
    'password': 'password'
}

# Helper function to generate unique item ID
def generate_item_id():
    return str(len(items_db) + 1)

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'username' in data and 'password' in data:
        if data['username'] == valid_credentials['username'] and data['password'] == valid_credentials['password']:
            # Successful login
            session['logged_in'] = True
            return jsonify({'message': 'Login successful'}), 200
        else:
            # Invalid credentials
            return jsonify({'message': 'Invalid username or password'}), 401
    else:
        # Missing username or password
        return jsonify({'message': 'Username and password are required'}), 400

# Route for user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'message': 'Logged out successfully'}), 200

# Routes for CRUD operations

@app.route('/', methods=['GET'])
def get_items():
    return jsonify(list(items_db.values()))

@app.route('/<item_id>', methods=['GET'])
def get_item(item_id):
    item = items_db.get(item_id)
    if item:
        return jsonify(item)
    return jsonify({'message': 'Item not found'}), 404

@app.route('/', methods=['POST'])
def create_item():
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
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized access'}), 401
    
    if item_id in items_db:
        del items_db[item_id]
        return jsonify({'message': 'Item deleted'})
    return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
