# Dzinza

Dzinza is a web application that allows users to create and manage their family trees. Users can build their family trees by adding family members, updating information, and visualizing the relationships within the tree.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication:**
  - Login and signup with email and password.

- **Family Tree Management:**
  - Create, update, and delete family trees.
  - Add, update, and delete family members.
  - View family members' details, including parents and siblings.

- **Search:**
  - Search functionality to find family members across all trees.

## Project Structure

The project follows a modular structure for better organization:

- **app:**
  - `config.py`: Configuration settings for the application.
  - `models.py`: Database models for User, FamilyTree, and FamilyMember.
  - `routes:` Folder containing route files for family_tree, family_member, and user.
  - `utils:` Folder containing utility functions.
  - `tests:` Folder with unit tests for the application.

## Getting Started

### Prerequisites

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/family_tree_project.git
   ```

2. Create a virtual environment and activate it:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Running the Application

To run the application locally, use the following commands:

```
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

The application will be accessible at `http://localhost:5000`.

## API Endpoints

The API endpoints for the application are defined in the `routes` folder. Refer to the individual route files for details on each endpoint.

## Testing

Unit tests for the application can be found in the `tests` folder. Run the tests using the following command:

```
python -m unittest discover tests
```

## License

No licences, just give me some credit.
