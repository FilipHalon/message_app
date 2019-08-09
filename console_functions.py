from models import User
from hash_password import check_password


def check_user_and_password(username, password):
    if username and password:
        user_list = User.load(name=username)
        for user in user_list:
            is_correct = check_password(password, user[3])
            if is_correct:
                return User.load(id=user[0])
    else:
        raise Exception('No such user exists or the username and password information did not match.')