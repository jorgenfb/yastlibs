#!/usr/bin/python

from time import time
from argparse import ArgumentParser
from yastlib import *

parser = ArgumentParser('Stop running tasks started today')
parser.add_argument('-u', '--user', dest='user', help='username')
parser.add_argument('-p', '--password', type=str, dest='password', help="Password for login")
parser.add_argument('-x', '--hash', dest='hash', help='hash value from yast')
args = parser.parse_args()

options = {}
options['timeFrom'] = int(time()) - 24 * 60 * 60
options['type'] = 1

yast = Yast()

if args.user == None:
    raise Exception("Username and either password or hash must be provided")
else:
    if args.hash == None:
        # No hash given, password required
        if args.password == None:
            raise Exception("Username and either password or hash must be provided for command \"" + commandName + "\"")
        else:
            # Login
            yast.login(args.user, args.password)
    else:
        # Username and hash provided. Already logged in
        yast.user = args.user
        yast.hash = args.hash

records = yast.getRecords(options).values()

for r in records:
    if r.variables['isRunning'] == 1:
        r.variables['isRunning'] = 0;
        r.variables['endTime'] = int(time())
        yast.change(r)
        print('Stopped record ' + str(r.id) + ': ' + r.variables['comment'])
