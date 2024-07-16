import json
import os
from flask import Flask, request, jsonify
from calculations import reconciliate_data
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = os.getenv('DATA_FILE', 'members.json')

def load_members():
    """Load members from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f).get('members', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading members: {e}")
        return []

def save_members(members):
    """Save members to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump({"members": members}, f)
    except IOError as e:
        logger.error(f"Error saving members to file: {e}")

members_list = load_members()

@app.route('/members', methods=['GET'])
def get_members():
    """Retrieve the list of members."""
    return jsonify({"members": members_list})

@app.route('/members', methods=['POST'])
def add_member():
    """Add a new member to the list."""
    new_member = request.json.get('name')
    if new_member and new_member.strip():
        members_list.append(new_member.strip())
        save_members(members_list)
        return jsonify({"members": members_list}), 201
    logger.warning("Invalid member name received.")
    return jsonify({"error": "Invalid member name"}), 400

@app.route('/reconcile', methods=['POST'])
def reconcile():
    """Reconcile data based on the provided incidence matrix, measurements, and tolerances."""
    data = request.get_json()
    try:
        incidence_matrix = data.get('incidence_matrix')
        measurements = data.get('measurements')
        tolerances = data.get('tolerances')

        if incidence_matrix is None or measurements is None or tolerances is None:
            logger.warning("Missing data in reconciliation request.")
            return jsonify({"error": "Missing data"}), 400

        result = reconciliate_data(incidence_matrix, measurements, tolerances)
        return jsonify({"reconciled_measurements": result}), 201
    except ValueError as e:
        logger.error(f"ValueError during reconciliation: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error during reconciliation: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/members', methods=['DELETE'])
def delete_member():
    """Delete a member from the list."""
    member_to_delete = request.json.get('name')
    if member_to_delete in members_list:
        members_list.remove(member_to_delete)
        save_members(members_list)
        return jsonify({"members": members_list}), 200
    logger.warning(f"Member not found: {member_to_delete}")
    return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
