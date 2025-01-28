from app.services.user_service import update_user

# User ID to update
user_id = 1

# Data to update
update_data = {
    "name": "John Updated",
    "email": "john.updated@example.com",
    "first_name": "John",
    "last_name": "Doe Updated"
}

# Call the service function
result = update_user(user_id, update_data)

print(result)
