#import datetime
import urllib
from google.appengine.ext import db
#from google.appengine.api import users
from time import strftime

class Program(db.Model):
    title = db.StringProperty(required=True)

    def escaped_key(self):
        return urllib.quote(self.key().name().encode('utf-8'))

class Episode(db.Model):
    program = db.ReferenceProperty( Program )
    title = db.StringProperty()
    file_url = db.LinkProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, program_name, title, file_url):
        program = Program.get_or_insert(program_name, title = program_name)
        episode = Episode(key_name = title, program=program, title = title, file_url = db.Link(file_url))
        episode.put()

        return episode

    def pub_date(self):
        return self.created_at.strftime("%a, %d %b %Y %H:%M:%S +0000")

class ClientKey(db.Model):
    pass