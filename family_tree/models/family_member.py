#!/usr/bin/python3

from models import db

class FamilyMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    gender = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date)
    date_of_death = db.Column(db.Date)
    biography = db.Column(db.Text)
    mother_id = db.Column(db.Integer, db.ForeignKey('family_member.id'))
    father_id = db.Column(db.Integer, db.ForeignKey('family_member.id'))
    tree_id = db.Column(db.Integer, db.ForeignKey('family_tree.id'), nullable=False)
    tree = db.relationship('FamilyTree', backref=db.backref('family_members', lazy=True))
    relationship = db.Column(db.String(50))
    is_approved = db.Column(db.Boolean, default=False)

    mother = db.relationship('FamilyMember', remote_side=[id], backref=db.backref('children_mother', lazy=True))
    father = db.relationship('FamilyMember', remote_side=[id], backref=db.backref('children_father', lazy=True))

    # New attributes
    marriages = db.relationship('Marriage', backref='family_member')


class Marriage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spouse_id = db.Column(db.Integer, db.ForeignKey('family_member.id'), nullable=False)
    marriage_date = db.Column(db.Date)
    divorce_date = db.Column(db.Date)
    deceased_spouse_name = db.Column(db.String(100))
