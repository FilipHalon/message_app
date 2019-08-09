import argparse

parser = argparse.ArgumentParser(description='Select a proper set of options for the program to proceed.')
parser.add_argument('-u', '--username', help='Username input.')
parser.add_argument('-p', '--password', help='Password input.')
parser.add_argument('-n', '--new-pass', help='Set a new password.')
parser.add_argument('-l', '--list', help='Display all the users in the database.')
parser.add_argument('-d', '--delete', help='Input the login of a user that you want to delete from the database.')
parser.add_argument('-e', '--edit', help='Input the login of a user the data of whom you want to edit.')
parser.parse_args()
