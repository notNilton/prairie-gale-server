import json
from flask import Flask, request, jsonify

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


if __name__ == '__main__':
    app.run(debug=True)
