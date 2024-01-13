# Utils

This contains utility functions and decorators that enhance the functionality of the application.

## Files

- `decorators.py`: Defines custom decorators used to enforce authentication and other access controls.

## Decorators

### 1. `login_required`

- **File**: `decorators.py`
- **Description**: Ensures that a user is logged in before granting access to protected routes. It utilizes the user's session for authentication.
