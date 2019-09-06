import argparse
from models import User, Message
from console_functions import check_user_and_password


def create_parser_message():

    parser = argparse.ArgumentParser(
        description="""Select a proper set of options for the program to proceed.
                       To display all the messages by a user, please input the username (after -u) 
                       and the password (after -p) of that user as well as -l.
                       To send the message, please input your username (after -u), password (after -p) and specify
                       who you wish to send the message to (after -t) and write the text of the message (after -s)""")
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

        message_list = Message.load(from_id=user._User__id)
        to_display = []
        for message in message_list:
            to_display_msg = [User.load(id=message[1]).name, User.load(id=message[2]).name, message[3], str(message[4])]
            to_display.append(to_display_msg)

        print(to_display)
        # it might be necessary to check the dates and order by them

    elif args.list and (args.to or args.send):
        print("You used an incorrect set of arguments.")

    elif not args.list and args.to and args.send:

        to_user = User.load(name=args.to)
        if len(to_user) == 0:
            raise Exception("The user you are trying to send the message to does not exist in the database.")

        message = Message()
        message.from_id = user._User__id
        message.to_id = to_user[0][0]
        message.text = args.send
        message.save()

    elif not args.list and not args.to and args.send:
        print("You did not specify the user you wish send the message to.")

    elif not args.list and args.to and not args.send:
        print("You did not write the message.")

