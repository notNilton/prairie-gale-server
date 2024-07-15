# app.py

import json
from flask import Flask, request, jsonify
from calculations import add_numbers

app = Flask(__name__)

DATA_FILE = 'members.json'

def load_members():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f).get('members', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_members(members):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump({"members": members}, f)
    except IOError as e:
        print(f"Error saving members to file: {e}")

members_list = load_members()

@app.route('/members', methods=['GET'])
def get_members():
    return jsonify({"members": members_list})

@app.route('/members', methods=['POST'])
def add_member():
    new_member = request.json.get('name')
    if new_member and new_member.strip():
        members_list.append(new_member.strip())
        save_members(members_list)
        return jsonify({"members": members_list}), 201
    return jsonify({"error": "Invalid member name"}), 400

@app.route('/sum', methods=['POST'])
def add_sum():
    data = request.json
    number_a = data.get('numberA')
    number_b = data.get('numberB')

    if number_a is not None and number_b is not None:
        try:
            sum_result = add_numbers(number_a, number_b)
            sum_member = f"Sum: {sum_result}"
            members_list.append(sum_member)
            save_members(members_list)
            return jsonify({"members": members_list}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Missing numbers"}), 400

@app.route('/members', methods=['DELETE'])
def delete_member():
    member_to_delete = request.json.get('name')
    if member_to_delete in members_list:
        members_list.remove(member_to_delete)
        save_members(members_list)
        return jsonify({"members": members_list}), 200
    return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
