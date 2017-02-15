from threading import Thread
from base_dao import *
import urllib2

class PosterChoser(Thread):
    def __init__(self, data_source):
        self.data_source = data_source

    def run(self):
        homepage_req = urllib2.Request(self.data_source['url'], )