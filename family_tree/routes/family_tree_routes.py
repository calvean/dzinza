#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from models.family_tree import FamilyTree
from models.family_member import FamilyMember
from models.user import User
from models import db

family_tree_bp = Blueprint('family_tree', __name__)

# Define routes for family trees
@family_tree_bp.route('/api/family-trees', methods=['GET', 'POST'])
def family_trees():
    if request.method == 'GET':
        # Implement logic to get a list of family trees
        family_trees = FamilyTree.query.all()
        result = [{'id': tree.id, 'name': tree.name, 'description': tree.description, 'owner': tree.user.email} for tree in family_trees]
        return jsonify({'family_trees': result})

    elif request.method == 'POST':
        # Implement logic to create a new family tree
        data = request.json
        new_tree = FamilyTree(name=data['name'], description=data.get('description', ''), user_id=1)  # Assuming user_id=1 for simplicity
        db.session.add(new_tree)
        db.session.commit()
        return jsonify({'message': 'Family tree created successfully'})
