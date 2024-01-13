""" app/routes/family_tree.py """
from flask import Blueprint, request, jsonify, session
from app import db
from app.models import FamilyTree, FamilyMember, User
from app.utils.decorators import login_required

family_tree_bp = Blueprint('family_tree', __name__)

@family_tree_bp.route('/api/family-trees', methods=['GET'])
@login_required
def get_family_trees():
    """
    Retrieve a list of family trees associated with the logged-in user.

    Returns:
        jsonify: A JSON response containing user's family trees.
    """
    try:
        user_id = session.get('user_id')
        session_id = session.get('session_cookie')
        user = User.query.get(user_id)
        family_trees = user.get_user_family_trees()

        family_tree_list = []
        for tree in family_trees:
            family_tree_list.append({
                'id': tree.id,
                'name': tree.name,
                'description': tree.description,
            })

        return jsonify({'family_trees': family_tree_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_tree_bp.route('/api/family-trees', methods=['POST'])
@login_required
def create_family_tree():
    """
    Create a new family tree for the logged-in user.

    Returns:
        jsonify: A JSON response indicating the success or failure of the operation.
    """
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        existing_tree = FamilyTree.query.filter_by(name=name, user_id=user_id).first()

        if existing_tree:
            return jsonify({'error': 'Tree with the same name already exists.'}), 400

        FamilyTree.create_family_tree(name, description, user_id)

        return jsonify({'message': 'Family tree created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_tree_bp.route('/api/family-trees/<int:tree_id>', methods=['GET'])
@login_required
def get_family_tree(tree_id):
    """
    Retrieve information about a specific family tree.

    Args:
        tree_id (int): The ID of the family tree to retrieve.

    Returns:
        jsonify: A JSON response containing information about the family tree.
    """
    try:
        user_id = session.get('user_id')
        family_tree = FamilyTree.query.filter_by(id=tree_id, user_id=user_id).first()

        if not family_tree:
            return jsonify({'error': 'Family tree not found'}), 404

        tree_data = {
            'id': family_tree.id,
            'name': family_tree.name,
            'description': family_tree.description,
        }

        return jsonify({'family_tree': tree_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_tree_bp.route('/api/family-trees/<int:tree_id>/members', methods=['GET'])
@login_required
def get_all_members_in_tree(tree_id):
    """
    Retrieve a list of all family members in a specific family tree for logged in user.

    Args:
        tree_id (int): The ID of the family tree to retrieve members from.

    Returns:
        jsonify: A JSON response containing the family members in the tree.
    """
    try:
        user_id = session.get('user_id')
        family_tree = FamilyTree.query.filter_by(id=tree_id, user_id=user_id).first()

        if not family_tree:
            return jsonify({'error': 'Family tree not found'}), 404

        members = FamilyMember.query.filter_by(tree_id=tree_id).all()

        members_list = []
        for member in members:
            members_list.append({
                'id': member.id,
                'name': member.name,
                'gender': member.gender,
                'date_of_birth': member.date_of_birth,
                'biography': member.biography,
                'picture_url': member.picture_url,
            })

        return jsonify({'family_members': members_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@family_tree_bp.route('/api/family-trees/<int:tree_id>', methods=['PUT'])
@login_required
def update_family_tree(tree_id):
    """
    Update details of a specific family tree.

    Args:
        tree_id (int): The ID of the family tree.

    Returns:
        Response: JSON response with updated family tree details.
    """
    try:
        family_tree = FamilyTree.query.filter_by(id=tree_id).first()

        if not family_tree:
            return jsonify({'error': 'Family tree not found'}), 404

        data = request.get_json()
        family_tree.update_tree(
            name=data.get('name'),
            description=data.get('description')
        )

        return jsonify({'message': 'Family tree updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_tree_bp.route('/api/family-trees/<int:tree_id>', methods=['DELETE'])
@login_required
def delete_family_tree(tree_id):
    """
    Delete a specific family tree.

    Args:
        tree_id (int): The ID of the family tree.

    Returns:
        Response: JSON response indicating the success of the deletion.
    """
    try:
        family_tree = FamilyTree.query.filter_by(id=tree_id).first()

        if not family_tree:
            return jsonify({'error': 'Family tree not found'}), 404

        family_tree.delete_tree()

        return jsonify({'message': 'Family tree deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

