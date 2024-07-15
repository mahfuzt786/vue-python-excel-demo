from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, create_default_admin
from flask_bcrypt import Bcrypt
import os
import pandas as pd

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
bcrypt = Bcrypt()
jwt = JWTManager(app)
CORS(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"message": "Email already registered!", "value": "issues"}), 201
    # hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    hashed_password=data['password']

    new_user = User(
        name=data['name'],
        email=data['email'],
        address=data['address'],
        contact_number=data['contactNumber'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201
    

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    # hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    hashed_password = data['password']

    # if not user or not check_password_hash(user.password, data['password']):
    if not user or not (user.password == hashed_password):
        return jsonify({"message": "Invalid credentials!", "value": "issues"}), 201
    access_token = create_access_token(identity={'email': user.email, 'role': user.role})
    return jsonify({"access_token": access_token, "user": {"email": user.email, "role": user.role}})


@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        # Handle password reset logic here (e.g., send email with reset link)
        return jsonify({"message": "Password reset link sent!"})
    return jsonify({"message": "Email not found!"}), 404

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        users = User.query.all()
    else:
        users = User.query.filter_by(email=current_user['email']).all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'address': user.address,
        'contactNumber': user.contact_number,
        'role': user.role,
    } for user in users])

@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    # hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    hashed_password=data['password']

    new_user = User(
        name=data['name'],
        email=data['email'],
        address=data['address'],
        contact_number=data['contactNumber'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!", "value": "issues"})
    user.name = data['name']
    user.email = data['email']
    user.address = data['address']
    user.contact_number = data['contactNumber']
    # user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    user.password = user.password #data['password']
    db.session.commit()
    return jsonify({"message": "User updated successfully!"})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!", "value": "issues"})
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"})

@app.route('/api/excel-file', methods=['GET'])
def get_excel_file():
    file_path = os.path.join(os.path.dirname(__file__), 'Security_Transactions_Data.xlsx')
    return send_file(file_path, as_attachment=True)

# def load_excel_data(file_path):
#     xls = pd.ExcelFile(file_path)
#     data = {}
#     for sheet_name in xls.sheet_names:
#         df = pd.read_excel(xls, sheet_name=sheet_name)
#         df = df.where(pd.notnull(df), None)  # Replace NaN with None
#         df = df.fillna('')  # Replace None with empty strings
#         data[sheet_name] = df.to_dict(orient='records')
#     return data
def load_excel_data(file_path):
    xls = pd.ExcelFile(file_path)
    data = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Convert all columns to strings
        df = df.applymap(str)

        data[sheet_name] = df.to_dict(orient='records')
    return data

def convert_to_numeric(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return value

@app.route('/api/data', methods=['GET'])
def get_data():
    sheet = request.args.get('sheet', 'SECURITY_TRANSACTIONS')
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('itemsPerPage', 10))
    sort_by = request.args.get('sortBy', '')
    sort_desc = request.args.get('sortDesc', 'false') == 'true'
    search_query = request.args.get('search', '')

    file_path = os.path.join(os.path.dirname(__file__), 'Security_Transactions_Data.xlsx')

    data = load_excel_data(file_path)
    sheet_data = data.get(sheet, [])

    # Apply search filter
    if search_query:
        sheet_data = [item for item in sheet_data if any(search_query.lower() in str(value).lower() for value in item.values())]

    # Perform sorting
    if sort_by:
        # Define a key function for sorting based on the sort_by column
        key_function = lambda x: convert_to_numeric(x.get(sort_by)) if isinstance(x.get(sort_by), (int, float)) else x.get(sort_by)
        sheet_data = sorted(sheet_data, key=key_function, reverse=sort_desc)

    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_data = sheet_data[start:end]

    # return jsonify({ "items": paginated_data, "total": len(sheet_data)}), 201
    response = jsonify({
        'items': paginated_data,
        'total': len(sheet_data)
    })
    response.headers.add('Content-Type', 'application/json')
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()  # Create default admin user
    app.run(debug=True, port=8001)
    # app.run(host='0.0.0.0', port=80)
