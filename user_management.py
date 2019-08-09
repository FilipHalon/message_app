import argparse
from models import User
from console_functions import check_user_and_password


def create_parser_user():

    parser = argparse.ArgumentParser(
        description='Select a proper set of options for the program to proceed.')
    parser.add_argument(
        '-u', '--username',
        help='Username input.')
    parser.add_argument(
        '-p', '--password',
        help='Password input.')
    parser.add_argument(
        '-n', '--new-pass',
        help='Set a new password.')
    parser.add_argument(
        '-l', '--list', action='store_true',
        help='Display all the users in the database.')
    parser.add_argument(
        '-d', '--delete', action='store_true',
        help='Input the login of a user that you want to delete from the database.')
    parser.add_argument(
        '-e', '--edit', action='store_true',
        help='Input the login of a user the data of whom you want to edit.')
    return parser.parse_args()


if __name__ == '__main__':

    args = create_parser_user()

    if args.username and args.password and not args.new_pass and not args.list and not args.delete and not args.edit:
        if not User.load(name=args.username):
            user = User()
            user.email = f"{args.username}@mail.com"
            user.name = args.username
            user.set_password(args.password)
            user.save()
        else:
            raise Exception("This user already exists.")

    elif args.username and args.password and args.new_pass and not args.list and not args.delete and args.edit:
        user = check_user_and_password()
        user.set_password(args.password)
        user.save()

    elif args.username and args.password and not args.new_pass and not args.list and args.delete and not args.edit:
        user = check_user_and_password()
        user.delete()

    elif not args.username and not args.password and not args.new_pass and args.list and args.delete and not args.edit:
        user_list = User.load()
        for user in user_list:
            print(f"{user[0]} {user[1]} {user[2]}")

    else:
        print("You used an incorrect set of arguments.")
