""" app/models.py """
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """
    Represents a user

    Attributes:
        id (int): ID for the user.
        email (str): The email address of the user (unique).
        password (str): The hashed password of the user.
        family_trees (Relationship): One-to-many relationship with FamilyTree model.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    family_trees = db.relationship('FamilyTree', backref='user', lazy=True)

    @staticmethod
    def register_user(email, password):
        """
        Register a new user.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.

        Raises:
            Exception: If an error occurs during registration.
        """
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate a user with the provided email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.

        Returns:
            User: The authenticated user if successful, else None.
        """
        try:
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                return user
        except Exception as e:
            raise e

    def get_user_family_trees(self):
        """
        Get all family trees associated with the user.

        Returns:
            list: List of FamilyTree objects associated with the user.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return FamilyTree.query.filter_by(user_id=self.id).all()
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_email(email):
        """
        Get a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User: The user with the specified email if found, else None.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            raise e

class FamilyTree(db.Model):
    """
    Represents a family tree.

    Attributes:
        id (int): ID for the family tree.
        name (str): The name of the family tree.
        description (str): The description of the family tree.
        user_id (int): The ID of the user who owns the family tree.
        members (Relationship): One-to-many relationship with FamilyMember model.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    members = db.relationship('FamilyMember', backref='family_tree', lazy=True)

    @staticmethod
    def create_family_tree(name, description, user_id):
        """
        Create a new family tree.

        Args:
            name (str): The name of the family tree.
            description (str): The description of the family tree.
            user_id (int): The ID of the user creating the family tree.

        Raises:
            Exception: If an error occurs during creation.
        """
        try:
            new_tree = FamilyTree(name=name, description=description, user_id=user_id)

            db.session.add(new_tree)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def get_all_trees(self):
        """
        Get all family trees associated with the user.

        Returns:
            list: List of FamilyTree objects associated with the user.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return FamilyTree.query.filter_by(user_id=self.user_id).all()
        except Exception as e:
            raise e

    def update_tree(self, name, description):
        """
        Update the information of the family tree.

        Args:
            name (str): The new name of the family tree.
            description (str): The new description of the family tree.

        Raises:
            Exception: If an error occurs during update.
        """
        try:
            self.name = name
            self.description = description

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_tree(self):
        """
        Delete the family tree and its associated members.

        Raises:
            Exception: If an error occurs during deletion.
        """
        try:
            FamilyMember.query.filter_by(tree_id=self.id).delete()

            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def get_tree_members_count(self):
        """
        Get the count of members in the family tree.

        Returns:
            int: The number of members in the family tree.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return FamilyMember.query.filter_by(tree_id=self.id).count()
        except Exception as e:
            raise e

class FamilyMember(db.Model):
    """
    Represents a family member in the system.

    Attributes:
        id (int): The unique identifier for the family member.
        name (str): The name of the family member.
        gender (str): The gender of the family member.
        date_of_birth (Date): The date of birth of the family member.
        biography (str): The biography of the family member.
        picture_url (str): The URL of the family member's picture.
        tree_id (int): The ID of the family tree to which the member belongs.
        father_id (int): The ID of the father of the family member.
        mother_id (int): The ID of the mother of the family member.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    biography = db.Column(db.Text)
    picture_url = db.Column(db.String(255))
    tree_id = db.Column(db.Integer, db.ForeignKey('family_tree.id'), nullable=False)
    father_id = db.Column(db.Integer, db.ForeignKey('family_member.id'))
    mother_id = db.Column(db.Integer, db.ForeignKey('family_member.id'))

    def get_siblings(self):
        """
        Get all siblings of the family member.

        Returns:
            list: List of FamilyMember objects representing siblings.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            siblings = FamilyMember.query.filter(
                (FamilyMember.id != self.id) &
                ((FamilyMember.father_id == self.father_id) |
                 (FamilyMember.mother_id == self.mother_id))
            ).all()
            return siblings
        except Exception as e:
            raise e

    def get_parents(self):
        """
        Get the parents of the family member.

        Returns:
            dict: Dictionary containing 'father' and 'mother' keys, representing parents.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            father = FamilyMember.query.get(self.father_id) if self.father_id else None
            mother = FamilyMember.query.get(self.mother_id) if self.mother_id else None
            return {'father': father, 'mother': mother}
        except Exception as e:
            raise e

    @staticmethod
    def add_member(tree_id, name, gender, date_of_birth, biography, picture_url, father_id, mother_id):
        """
        Add a new family member to the specified family tree.

        Args:
            tree_id (int): The ID of the family tree to which the member belongs.
            name (str): The name of the family member.
            gender (str): The gender of the family member.
            date_of_birth (Date): The date of birth of the family member.
            biography (str): The biography of the family member.
            picture_url (str): The URL of the family member's picture.
            father_id (int): The ID of the father of the family member.
            mother_id (int): The ID of the mother of the family member.

        Raises:
            Exception: If an error occurs during addition.
        """
        try:
            new_member = FamilyMember(
                name=name,
                gender=gender,
                date_of_birth=date_of_birth,
                biography=biography,
                picture_url=picture_url,
                tree_id=tree_id,
                father_id=father_id,
                mother_id=mother_id,
            )

            db.session.add(new_member)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_members_in_tree(tree_id):
        """
        Get all family members in the specified family tree.

        Args:
            tree_id (int): The ID of the family tree.

        Returns:
            list: List of FamilyMember objects in the family tree.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return FamilyMember.query.filter_by(tree_id=tree_id).all()
        except Exception as e:
            raise e

    @staticmethod
    def get_member_by_id(tree_id, member_id):
        """
        Get a family member by their ID and the ID of the family tree.

        Args:
            tree_id (int): The ID of the family tree.
            member_id (int): The ID of the family member.

        Returns:
            FamilyMember: The family member if found, else None.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return FamilyMember.query.filter_by(id=member_id, tree_id=tree_id).first()
        except Exception as e:
            raise e

    @staticmethod
    def get_members_by_name(tree_id, member_name):
        """
        Get family members by their name and the ID of the family tree.

        Args:
            tree_id (int): The ID of the family tree.
            member_name (str): The name of the family member.

        Returns:
            list: List of FamilyMember objects with the specified name.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return FamilyMember.query.filter_by(name=member_name, tree_id=tree_id).all()
        except Exception as e:
            raise e

    def update_member(self, name, gender, date_of_birth, biography, picture_url, father_id, mother_id):
        """
        Update the information of the family member.

        Args:
            name (str): The new name of the family member.
            gender (str): The new gender of the family member.
            date_of_birth (Date): The new date of birth of the family member.
            biography (str): The new biography of the family member.
            picture_url (str): The new URL of the family member's picture.
            father_id (int): The new ID of the father of the family member.
            mother_id (int): The new ID of the mother of the family member.

        Raises:
            Exception: If an error occurs during update.
        """
        try:
            self.name = name
            self.gender = gender
            self.date_of_birth = date_of_birth
            self.biography = biography
            self.picture_url = picture_url
            self.father_id = father_id
            self.mother_id = mother_id

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_member(self):
        """
        Delete the family member.

        Raises:
            Exception: If an error occurs during deletion.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

