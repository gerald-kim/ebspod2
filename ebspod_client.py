# !/usr/bin/env python2.7
# encoding: utf-8
"""
recorder.py

Created by Jaewoo Kim on 2008-12-11.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.

"""
import sys
from os import system, path, remove
import urllib

sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)), "libs"))

import datetime
from mutagen.easyid3 import EasyID3
import tempfile
import S3
from ebspod_client_config import *


def s3_file_name(title):
    return title + '.mp3'


def s3_url(title):
    return "http://s3.amazonaws.com/%s/%s" % (BUCKET_NAME, urllib.quote(s3_file_name(title).encode('utf-8')))


def upload_to_s3(title, filename):
    conn = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    conn.calling_format = S3.CallingFormat.PATH

    key = s3_file_name(title).encode('utf-8')

    f = open(filename)
    r = conn.put(BUCKET_NAME, key, S3.S3Object(f.read()), {'x-amz-acl': 'public-read', 'Content-Type': 'audio/mp3'})
    if r.http_response.status != 200:
        print "upload fail."
        exit(1)


def get_title(program_name):
    return u"%s - %s" % ( program_name.decode('utf-8'), datetime.datetime.now().strftime("%Y-%m-%d") )


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s [record duration in min] [Program name]"
        sys.exit(-1)

    program_name = sys.argv[2]
    title = get_title(program_name)

    flv_file = tempfile.mktemp(".flv")
    mp3_file = tempfile.mktemp(".mp3")
    #system("mimms -c -t %s mms://211.218.209.124/L-FM_300k %s" % (sys.argv[1], flv_file))
    #system("ffmpeg -i %s %s" % (flv_file, mp3_file))
    #system("rtmpdump -r rtmp://ebsandroid.nefficient.com/fmradiofamilypc/familypc1m -B %d -o %s" % (int(sys.argv[1])*60, flv_file))
    #system("ffmpeg -i %s %s" % (flv_file, mp3_file))
    system("rtmpdump -r rtmp://ebsandroid.ebs.co.kr/fmradiofamilypc/familypc1m -B %d -o - | avconv -i - -b 64k %s" % (
        int(sys.argv[1]) * 60, mp3_file))

    #    mp3_file = 'test.mp3'

    audio = EasyID3(mp3_file)
    audio["Album"] = program_name.decode('utf-8')
    audio["Title"] = title
    audio["Artist"] = u'EBSPod'
    audio.save()

    upload_to_s3(title, mp3_file)
    remove(mp3_file)
    #remove(flv_file)
    params = urllib.urlencode(
        {'program_name': program_name, 'title': title.encode('utf-8'), 'title': title.encode('utf-8'),
         'file_url': s3_url(title).encode('utf-8'),
         'client_key': CLIENT_KEY})
    urllib.urlopen(SERVER_ADDR, params).read()
