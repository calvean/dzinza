""" app/routes/family_member.py """
from flask import Blueprint, request, jsonify, session
from app import db
from app.models import FamilyMember, FamilyTree, User
from app.utils.decorators import login_required

family_member_bp = Blueprint('family_member', __name__)

@family_member_bp.route('/api/family-trees/<int:tree_id>/members', methods=['POST'])
@login_required
def add_family_member(tree_id):
    """
    Add new family member to specified family tree.

    Args:
        tree_id (int): The ID of family tree to which the member will be added.

    Returns:
        jsonify: A JSON response containing added family member.
    """
    try:
        data = request.get_json()
        name = data.get('name')
        gender = data.get('gender')
        date_of_birth = data.get('date_of_birth')
        biography = data.get('biography')
        picture_url = data.get('picture_url')
        father_name = data.get('father_name')
        mother_name = data.get('mother_name')

        """ Check if the member already exists """
        existing_member = FamilyMember.query.filter_by(
            name=name,
            gender=gender,
            date_of_birth=date_of_birth,
            tree_id=tree_id
        ).first()

        if existing_member:
            return jsonify({'error': 'Member already exists in the family tree.'}), 400

        """ Fetch existing parent names for the given tree """
        father_names = [father.name for father in FamilyMember.get_all_members_in_tree(tree_id) if father.gender == 'Male']
        mother_names = [mother.name for mother in FamilyMember.get_all_members_in_tree(tree_id) if mother.gender == 'Female']

        """ Set parent IDs to None if the provided parent names do not exist """
        father_id = FamilyMember.query.filter_by(name=father_name, tree_id=tree_id).first().id if father_name and father_name in father_names else None
        mother_id = FamilyMember.query.filter_by(name=mother_name, tree_id=tree_id).first().id if mother_name and mother_name in mother_names else None

        FamilyMember.add_member(tree_id, name, gender, date_of_birth, biography, picture_url, father_id, mother_id)
        added_member = FamilyMember.query.filter_by(name=name, tree_id=tree_id).first()

        return jsonify({
            'message': 'Family member added successfully',
            'member_id': added_member.id,
            'member_name': added_member.name,
            'father_id': added_member.father_id,
            'mother_id': added_member.mother_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_member_bp.route('/api/family-trees/<int:tree_id>/members/<int:member_id>', methods=['GET'])
@login_required
def get_family_member(tree_id, member_id):
    """
    Retrieve member information in the specified family tree.

    Args:
        tree_id (int): The ID of family tree the member belongs.
        member_id (int): The ID of the family member to retrieve.

    Returns:
        jsonify: A JSON response containing the family member.
    """
    try:
        user_id = session.get('user_id')
        family_tree = FamilyTree.query.filter_by(id=tree_id, user_id=user_id).first()

        if not family_tree:
            return jsonify({'error': 'Family tree not found'}), 404

        member = FamilyMember.query.filter_by(id=member_id, tree_id=tree_id).first()

        if not member:
            return jsonify({'error': 'Family member not found'}), 404

        member_data = {
            'id': member.id,
            'name': member.name,
            'gender': member.gender,
            'date_of_birth': member.date_of_birth,
            'biography': member.biography,
            'picture_url': member.picture_url,
            'father_id': member.father_id,
            'mother_id': member.mother_id,
        }

        return jsonify({'family_member': member_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_member_bp.route('/api/family-trees/<int:tree_id>/members/<int:member_id>/siblings', methods=['GET'])
@login_required
def get_siblings(tree_id, member_id):
    """
    Retrieve siblings of a family member in the specified family tree.

    Args:
        tree_id (int): The ID of family tree the member belongs.
        member_id (int): The ID of the family member whose siblings to retrieve.

    Returns:
        jsonify: A JSON response containing the siblings of the family member.
    """
    try:
        member = FamilyMember.query.filter_by(id=member_id, tree_id=tree_id).first()

        if not member:
            return jsonify({'error': 'Family member not found'}), 404

        siblings = member.get_siblings()

        siblings_list = []
        for sibling in siblings:
            siblings_list.append({
                'id': sibling.id,
                'name': sibling.name,
                'gender': sibling.gender,
                'date_of_birth': sibling.date_of_birth,
                'biography': sibling.biography,
                'picture_url': sibling.picture_url,
            })

        return jsonify({'siblings': siblings_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_member_bp.route('/api/family-trees/<int:tree_id>/members/<int:member_id>/parents', methods=['GET'])
@login_required
def get_parents(tree_id, member_id):
    """
    Retrieve parents of a family member in the specified family tree.

    Args:
        tree_id (int): The ID of family tree the member belongs.
        member_id (int): The ID of family member whose parents to retrieve.

    Returns:
        jsonify: A JSON response containing the parents of the family member.
    """
    try:
        member = FamilyMember.query.filter_by(id=member_id, tree_id=tree_id).first()

        if not member:
            return jsonify({'error': 'Family member not found'}), 404

        parents = member.get_parents()

        parents_data = {
            'father': {
                'id': parents['father'].id,
                'name': parents['father'].name,
                'gender': parents['father'].gender,
                'date_of_birth': parents['father'].date_of_birth,
                'biography': parents['father'].biography,
                'picture_url': parents['father'].picture_url,
            } if parents['father'] else None,
            'mother': {
                'id': parents['mother'].id,
                'name': parents['mother'].name,
                'gender': parents['mother'].gender,
                'date_of_birth': parents['mother'].date_of_birth,
                'biography': parents['mother'].biography,
                'picture_url': parents['mother'].picture_url,
            } if parents['mother'] else None,
        }

        return jsonify({'parents': parents_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_member_bp.route('/api/family-trees/<int:tree_id>/members/<int:member_id>', methods=['PUT'])
@login_required
def update_family_member(tree_id, member_id):
    """
    Update details of a specific family member.

    Args:
        tree_id (int): The ID of the family tree.
        member_id (int): The ID of the family member.

    Returns:
        jsonify: A JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        name = data.get('name')
        gender = data.get('gender')
        date_of_birth = data.get('date_of_birth')
        biography = data.get('biography')
        picture_url = data.get('picture_url')
        father_name = data.get('father_name')
        mother_name = data.get('mother_name')

        family_member = FamilyMember.query.filter_by(id=member_id, tree_id=tree_id).first()

        if not family_member:
            return jsonify({'error': 'Family member not found'}), 404

        existing_member_with_details = FamilyMember.query.filter_by(
            name=name,
            gender=gender,
            date_of_birth=date_of_birth,
            tree_id=tree_id
        ).filter(FamilyMember.id != member_id).first()

        if existing_member_with_details:
            return jsonify({'error': 'Member already exists in the family tree.'}), 400

        father_names = [father.name for father in FamilyMember.get_all_members_in_tree(tree_id) if father.gender == 'Male']
        mother_names = [mother.name for mother in FamilyMember.get_all_members_in_tree(tree_id) if mother.gender == 'Female']
        father_id = FamilyMember.query.filter_by(name=father_name, tree_id=tree_id).first().id if father_name and father_name in father_names else None
        mother_id = FamilyMember.query.filter_by(name=mother_name, tree_id=tree_id).first().id if mother_name and mother_name in mother_names else None

        family_member.update_member(
            name=name,
            gender=gender,
            date_of_birth=date_of_birth,
            biography=biography,
            picture_url=picture_url,
            father_id=father_id,
            mother_id=mother_id
        )

        return jsonify({'message': 'Family member updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_member_bp.route('/api/family-trees/members/search', methods=['GET'])
@login_required
def search_family_members_all_trees():
    """
    Search for family members across all family trees of the logged-in user based on name.

    Returns:
        jsonify: A JSON response containing the search results grouped by family tree.
    """
    try:
        user_id = session.get('user_id')

        # Retrieve all family trees of the user
        user_family_trees = FamilyTree.query.filter_by(user_id=user_id).all()

        search_query = request.args.get('q')

        if not search_query:
            return jsonify({'error': 'Search query is required'}), 400

        search_results = {}

        # Search for family members with matching names in each family tree
        for tree in user_family_trees:
            matching_members = FamilyMember.query.filter(
                FamilyMember.tree_id == tree.id,
                FamilyMember.name.ilike(f"%{search_query}%")
            ).all()

            tree_results = []
            for member in matching_members:
                tree_results.append({
                    'id': member.id,
                    'name': member.name,
                    'gender': member.gender,
                    'date_of_birth': member.date_of_birth,
                    'biography': member.biography,
                    'picture_url': member.picture_url,
                    'father_id': member.father_id,
                    'mother_id': member.mother_id,
                })

            search_results[tree.name] = tree_results

        return jsonify({'search_results': search_results}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@family_member_bp.route('/api/family-trees/<int:tree_id>/members/<int:member_id>', methods=['DELETE'])
@login_required
def delete_family_member(tree_id, member_id):
    """
    Delete a specific family member.

    Args:
        tree_id (int): The ID of the family tree.
        member_id (int): The ID of the family member.

    Returns:
        Response: JSON response indicating the success of the deletion.
    """
    try:
        # Fetch the existing family member
        member = FamilyMember.query.filter_by(id=member_id, tree_id=tree_id).first()

        if not member:
            return jsonify({'error': 'Family member not found'}), 404

        # Delete the family member
        member.delete_member()

        return jsonify({'message': 'Family member deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

