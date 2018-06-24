# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2

import os

import json

from googleapiclient.discovery import build

from datetime import datetime, timedelta

import rfc3339 

search_date = datetime.now() - timedelta(days=50)

FORMAT='%Y-%m-%dT00:00:00Z'

API_KEY = "AIzaSyCLblmIG79BNiHAGgrzzly6aNJOlFuSQR0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

f = open(os.path.join(__location__, 'index.html'))

html_content = f.read()

class MainPage(webapp2.RequestHandler):
    def get(self):

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html_content)

class ApiHandler(webapp2.RequestHandler):
    def get(self):

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)


        channels_response = youtube.search().list( 
            channelId='UCIGhG3zPzhPHR_2fcLX2zhQ', 
            part='snippet',
            order='date',
            type='video',
            publishedAfter=search_date.strftime(FORMAT)
            ).execute()

        print json.dumps(channels_response)
        self.response.headers['Content-Type'] = 'application/json'

        api_content = channels_response
        self.response.write(json.dumps(api_content))




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/video', ApiHandler),
], debug=True)
