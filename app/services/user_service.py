from app import db
from app.models.users import Users

def create_user(email, first_name, last_name, password):
    user = Users(email=email, first_name=first_name, last_name=last_name)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return user