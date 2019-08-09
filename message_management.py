from user_management import *

parser.add_argument('-t', '--to', help='Specify the user you want to send the message to.')
parser.add_argument('-s', '--send', help='Write the message you want to send.')
parser.parse_args()

