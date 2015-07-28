#!/usr/bin/env python

import errno, sys, json, urllib2

if not len(sys.argv) > 1:
    print "Requires atleast one argument. [arg] [url]"
    sys.exit(errno.EPERM)

if sys.argv[1] == "progress":
    if not len(sys.argv) != 2:
        print "progress [url]"
        sys.exit(errno.EPERM)

    print urllib2.urlopen(sys.argv[2] + "/pipeline/progress").read()

if sys.argv[1] == "fail":
    if not len(sys.argv) != 2:
        print "fail [url]"
        sys.exit(errno.EPERM)

    print urllib2.urlopen(sys.argv[2] + "/pipeline/fail").read()


elif sys.argv[1] == "init":
    if not len(sys.argv) != 5:
        print "init [json-file] [title] [description] [url]"
        sys.exit(errno.EPERM)

    with open(sys.argv[2]) as data_file:
        data = json.load(data_file)
    data['title'] = sys.argv[3]
    data['description'] = sys.argv[4]

    req = urllib2.Request(sys.argv[5] + "/pipeline/init")
    req.add_header('Content-Type', 'application/json')

    print urllib2.urlopen(req, json.dumps(data))
