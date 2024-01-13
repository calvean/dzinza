#!/bin/bash

# Function to extract a cookie value from the response headers
get_cookie_value() {
    grep -i "$1" | tr -d '\r' | awk '{print $2}' | cut -f1 -d';'
}

# Register user
REGISTER_RESPONSE=$(curl -i -X POST -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "password"}' http://localhost:5000/api/register)
echo "Register Response: $REGISTER_RESPONSE"

# Extract cookies from the response headers
COOKIE_HEADER=$(echo "$REGISTER_RESPONSE" | grep -i 'Set-Cookie')
SESSION_COOKIE=$(get_cookie_value 'session_cookie')

echo "Session Cookie after registration: $SESSION_COOKIE"

# Log in the user
LOGIN_RESPONSE=$(curl -i -X POST -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "password"}' -H "Cookie: $SESSION_COOKIE" http://localhost:5000/api/login)
echo "Login Response: $LOGIN_RESPONSE"


# Create a family tree
FAMILY_TREE_RESPONSE=$(curl -X POST -H "Content-Type: application/json" -H "Cookie: session_cookie=$SESSION_ID" -d '{"name": "My Family Tree", "description": "Test Tree"}' http://localhost:5000/api/family-trees)
echo "Family tree created: $FAMILY_TREE_RESPONSE"

# Add three family members
for i in {1..3}; do
  FAMILY_MEMBER_RESPONSE=$(curl -X POST -H "Content-Type: application/json" -H "Cookie: session_cookie=$SESSION_ID" -d "{\"name\": \"Member $i\", \"gender\": \"Male\", \"date_of_birth\": \"1990-01-01\", \"biography\": \"Biography $i\", \"picture_url\": \"https://example.com/picture$i.jpg\", \"father_id\": $((i + 1)), \"mother_id\": $i}" http://localhost:5000/api/family-trees/1/members)
  echo "Family member $i added: $FAMILY_MEMBER_RESPONSE"
done

# Comprehensive testing of all family tree routes
ROUTES_TO_TEST=(
  "/api/family-trees"
  "/api/family-trees/1"
  "/api/family-trees/1/members"
  "/api/family-trees/1/members/1"
)

for route in "${ROUTES_TO_TEST[@]}"; do
  TEST_ROUTE_RESPONSE=$(curl -X GET -H "Cookie: session_cookie=$SESSION_ID" http://localhost:5000$route)
  echo "Testing route $route: $TEST_ROUTE_RESPONSE"
done

# Log out the user
LOGOUT_RESPONSE=$(curl -X POST -H "Cookie: session_cookie=$SESSION_ID" http://localhost:5000/api/logout)
echo "User logged out: $LOGOUT_RESPONSE"

# Capture user_id and session id after logout
USER_ID=$(echo "$LOGOUT_RESPONSE" | jq -r '.user_id')
SESSION_ID=$(echo "$LOGOUT_RESPONSE" | jq -r '.session_id')
echo "User ID after logout: $USER_ID"
echo "Session ID after logout: $SESSION_ID"

