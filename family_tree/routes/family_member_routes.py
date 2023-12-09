#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from models.family_tree import FamilyTree
from models.family_member import FamilyMember, Marriage
from models.user import User
from models import db

family_member_bp = Blueprint('family_member', __name__)

# Define routes for family members
@family_member_bp.route('/api/family-trees/<int:tree_id>/members', methods=['GET', 'POST'])
def family_members(tree_id):
    if request.method == 'GET':
        # Implement logic to get a list of family members in a tree
        family_members = FamilyMember.query.filter_by(tree_id=tree_id, is_approved=True).all()
        result = [[{'id': member.id, 'name': member.name, 'surname': member.surname, 'gender': member.gender,
                   'date_of_birth': str(member.date_of_birth), 'date_of_death': str(member.date_of_death),
                   'biography': member.biography, 'relationship': member.relationship,
                   'marriages': [{'spouse_id': marriage.spouse_id,
                                  'marriage_date': str(marriage.marriage_date),
                                  'divorce_date': str(marriage.divorce_date),
                                  'deceased_spouse_name': marriage.deceased_spouse_name}
                                 for marriage in member.marriages]}
                   ] for member in family_members]
        return jsonify({'family_members': result})

    elif request.method == 'POST':
        # Implement logic to add a new family member (pending approval)
        data = request.json
        user_id = 1  # Assuming user_id=1 for simplicity
        tree = FamilyTree.query.get(tree_id)

        # Check if the user owns the tree or has admin/moderator rights
        if tree.user_id == user_id or User.query.get(user_id).role in ['admin', 'moderator']:
            new_member = FamilyMember(name=data['name'], surname=data.get('surname', ''), gender=data['gender'],
                                      date_of_birth=data.get('date_of_birth'), date_of_death=data.get('date_of_death'),
                                      biography=data.get('biography'), relationship=data.get('relationship'), tree_id=tree_id)
            db.session.add(new_member)
            db.session.commit()

            # Add marriages
            marriages = data.get('marriages', [])
            for marriage_data in marriages:
                marriage = Marriage(spouse_id=marriage_data['spouse_id'],
                                    marriage_date=marriage_data.get('marriage_date'),
                                    divorce_date=marriage_data.get('divorce_date'),
                                    deceased_spouse_name=marriage_data.get('deceased_spouse_name'))
                new_member.marriages.append(marriage)
                db.session.add(marriage)

            db.session.commit()
            return jsonify({'message': 'Family member added and awaiting approval'})

        return jsonify({'error': 'You do not have permission to add family members to this tree'})

