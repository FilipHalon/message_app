import argparse
from models import User, Message
from console_functions import check_user_and_password


def create_parser_message():

    parser = argparse.ArgumentParser(
        description='Select a proper set of options for the program to proceed.')
    parser.add_argument(
        '-u', '--username',
        help='Username input.')
    parser.add_argument(
        '-p', '--password',
        help='Password input.')
    parser.add_argument(
        '-l', '--list', action='store_true',
        help='Display all the users in the database.')
    parser.add_argument(
        '-t', '--to',
        help='Specify the user you want to send the message to.')
    parser.add_argument(
        '-s', '--send',
        help='Write the message you want to send.')
    return parser.parse_args()


if __name__ == '__main__':

    args = create_parser_message()

    user = check_user_and_password(args.username, args.password)

    if args.list and not args.to and not args.send:
        print(Message.load(from_id=user.id))
        # it might be necessary to check the dates and order by them

    elif args.list and args.to or args.send:
        print("You used an incorrect set of arguments.")

    elif not args.list and args.to and args.send:
        if User.load(id=args.to):
            message = Message()
            message.from_id = user.id
            message.to_id = args.to
            message.text = args.send
            message.save()
        else:
            print("The user you are trying to send the message to does not exist in the database.")

    elif not args.list and args.to and not args.send:
        print("You did not specify the user you wish send the message to.")

    elif not args.list and not args.to and args.send:
        print("You did not write the message.")

