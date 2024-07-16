import json
import os
from flask import Flask, request, jsonify, abort
from calculations import reconciliate_data
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    if not request.is_json:
        logger.warning("Request content-type is not application/json")
        abort(400, description="Request must be JSON")

    new_member = request.json.get('name')
    if not new_member or not new_member.strip():
        logger.warning("Invalid member name received.")
        abort(400, description="Invalid member name")

    members_list.append(new_member.strip())
    save_members(members_list)
    return jsonify({"members": members_list}), 201

@app.route('/reconcile', methods=['POST'])
def reconcile():
    """Reconcile data based on the provided incidence matrix, measurements, and tolerances."""
    if not request.is_json:
        logger.warning("Request content-type is not application/json")
        abort(400, description="Request must be JSON")

    data = request.get_json()
    incidence_matrix = data.get('incidence_matrix')
    measurements = data.get('measurements')
    tolerances = data.get('tolerances')

    if incidence_matrix is None or measurements is None or tolerances is None:
        logger.warning("Missing data in reconciliation request.")
        abort(400, description="Missing data")

    try:
        result = reconciliate_data(incidence_matrix, measurements, tolerances)
        reconciled_measurements_str = f"Reconciled Measurements: {result}"
        members_list.append(reconciled_measurements_str)
        save_members(members_list)
        return jsonify({"reconciled_measurements": result, "members": members_list}), 201
    except ValueError as e:
        logger.error(f"ValueError during reconciliation: {e}")
        abort(400, description=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during reconciliation: {e}")
        abort(500, description="Internal server error")

@app.route('/members', methods=['DELETE'])
def delete_member():
    """Delete a member from the list."""
    if not request.is_json:
        logger.warning("Request content-type is not application/json")
        abort(400, description="Request must be JSON")

    member_to_delete = request.json.get('name')
    if not member_to_delete or member_to_delete not in members_list:
        logger.warning(f"Member not found: {member_to_delete}")
        abort(404, description="Member not found")

    members_list.remove(member_to_delete)
    save_members(members_list)
    return jsonify({"members": members_list}), 200

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error.description)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error.description)}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": str(error.description)}), 500

if __name__ == '__main__':
    app.run(debug=True)
