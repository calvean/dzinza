# Routes

This folder contains the route handlers for various entities in your application. Each route file handles the HTTP requests and responses related to a specific entity or resource.

## Files

- `family_member.py`: Defines routes for managing family members, including adding, updating, and retrieving information about family members.

- `family_tree.py`: Contains routes for handling family trees, including creating, updating, and deleting trees, as well as retrieving information about trees and their members.

## Family Member Routes

### 1. Add Family Member

- **Route**: `/api/family-trees/{tree_id}/members`
- **Method**: `POST`
- **Description**: Adds a new family member to the specified family tree.

### 2. Update Family Member

- **Route**: `/api/family-trees/{tree_id}/members/{member_id}`
- **Method**: `PUT`
- **Description**: Updates information about a specific family member in the given family tree.

### 3. Retrieve Family Member

- **Route**: `/api/family-trees/{tree_id}/members/{member_id}`
- **Method**: `GET`
- **Description**: Retrieves information about a specific family member in the specified family tree.

### 4. Delete Family Member

- **Route**: `/api/family-trees/{tree_id}/members/{member_id}`
- **Method**: `DELETE`
- **Description**: Deletes a specific family member from the given family tree.

### 5. Get Parents of a Family Member

- **Route**: `/api/family-trees/{tree_id}/members/{member_id}/parents`
- **Method**: `GET`
- **Description**: Retrieves the parents of a specific family member in the specified family tree.

### 6. Get Siblings of a Family Member

- **Route**: `/api/family-trees/{tree_id}/members/{member_id}/siblings`
- **Method**: `GET`
- **Description**: Retrieves the siblings of a specific family member in the specified family tree.

### 7. Get All Members in a Family Tree

- **Route**: `/api/family-trees/{tree_id}/members`
- **Method**: `GET`
- **Description**: Retrieves a list of all family members in the specified family tree.

### 8. Search Family Members in All Trees

- **Route**: `/api/family-trees/members/search?q={query}`
- **Method**: `GET`
- **Description**: Searches for family members across all family trees based on the given query.

### 9. Search Family Members in All Trees (No Query)

- **Route**: `/api/family-trees/members/search`
- **Method**: `GET`
- **Description**: Returns an error response indicating that a search query is required.

## Family Tree Routes

### 1. Get Family Trees

- **Route**: `/api/family-trees`
- **Method**: `GET`
- **Description**: Retrieves a list of family trees associated with the logged-in user.

### 2. Create Family Tree

- **Route**: `/api/family-trees`
- **Method**: `POST`
- **Description**: Creates a new family tree for the logged-in user.

### 3. Get Family Tree

- **Route**: `/api/family-trees/{tree_id}`
- **Method**: `GET`
- **Description**: Retrieves information about a specific family tree.

### 4. Get All Members in a Family Tree

- **Route**: `/api/family-trees/{tree_id}/members`
- **Method**: `GET`
- **Description**: Retrieves a list of all family members in the specified family tree.

### 5. Get Family Member in a Family Tree

- **Route**: `/api/family-trees/{tree_id}/members/{member_id}`
- **Method**: `GET`
- **Description**: Retrieves information about a specific family member in the specified family tree.

### 6. Update Family Tree

- **Route**: `/api/family-trees/{tree_id}`
- **Method**: `PUT`
- **Description**: Updates details of a specific family tree.

### 7. Delete Family Tree

- **Route**: `/api/family-trees/{tree_id}`
- **Method**: `DELETE`
- **Description**: Deletes a specific family tree.

## Usage

Make HTTP requests to the specified endpoints
