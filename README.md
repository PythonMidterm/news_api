# Intellinewz API

An API with exposed endpoints to filter a newsfeed based on a user's preference for dominate tones calculated based on tone analysis.

----
## AWS Deployment EC2 Instance:
[http://ec2-34-215-37-227.us-west-2.compute.amazonaws.com/](http://ec2-34-215-37-227.us-west-2.compute.amazonaws.com/)

## Github Repository
[https://github.com/PythonMidterm/news_api](https://github.com/PythonMidterm/news_api)

----
## Table of Contents
* [Overview](#overview)
* [Technologies](#technologies)
* [Getting Started](#start)
* [Participants](#participants)
* [Routes](#routes)
* [Wireframe](#wireframe)
* [User Stories](#user-stories)
----
<a id="overview"></a>
## Overview:
This app uses bcrypt.BCRYPTPasswordManager.
This app draws from the News API and IBM Watson's Tone Analysis API.
This app is made to provide a user with the ability to see news based on their tone preferences.
The problem being solved is that it allows people to understand predominant tones in the articles they read so as to better understand potential biases in their news sources.


----
<a id="technologies"></a>
## Technologies required:
- Python3, News API, Goose Text Extractor, IMB Watson Tone Analyzer (ToneAnalyzerV3), AWS, Gunicorn, WSGI, bcrypt, datetime, sqlalchemy, pyramid_restful, json, marshmallow, shedule, jupyter, numpy, pandas.

----
<a id="start"></a>
## Getting Started:
- Clone the repository from github using the command "git clone [repository link]" in your CLI.
- Use "pipenv shell" in your command line to set up your virtual environment.
- Use "pipenv install" to install all of the necessary dependencies.
- Use "pserve development.ini --reload" to start your server
- Make calls to the routes in an app like Postman or using HTTPy.
- ALSO, look in the README.txt provided by Pyramid for further instruction.
----
<a id="participants"></a>
## Particapants:
- Luther Mckeiver
- Ben Hurst
- Madeline Peters
- Roman Kireev
----
<a id="routes"></a>
## Routes:
**Home:** `/`
* GET: Splash page with login prompt.

**Preferences:** `api/v1/preferences`
* GET: Review preferences in the database.
* POST: Change existing preferences. If no preferences given, default provided.
~~~
preference_order = {
        'preference_order': 'test@example.com',
    }
response.status_code == 201
~~~
* OTHER METHODS:
~~~~
response.status_code == 4**
~~~~

**Feed:** `api/v1/feed`
* GET: See your feed organized based on user preferences. If no user preferences, default preferences used.
* OTHER METHODS:
~~~~
response.status_code == 4**
~~~~
**Visuals:** `api/v1/visuals`
* GET: See visual representations of the data in our article archives.

**Authorization:**
* `api/v1/auth/{auth}`
* `api/v1/register`
* `api/v1/login`
* POST with successful auth:

~~~~
account = {
        'email': 'test@example.com',
        'password': 'hello',
    }
   response.json['token']
   response.status_code == 201
   ~~~~

* POST with unsuccessful auth (no token returned):
~~~~
account = {
        'email': 'test_two@example.com',
    }
    response.status_code == 400
~~~~

----

<a id="wireframe"></a>
## Wireframe:
![Wireframe ](/news_api/assets/wireframe.png)

----
<a id="user-stories"></a>
## User Stories:
* As a user, I would like a news feed filtered by number of articles and categories.
* As a user, I would like to access just the text from the body of an article from its url to perform analysis on.
* As a user, I would like to sort my newsfeed by tone.
* As a user, I would like quick loading- tone has already been analyzed before I request.
* As a user, I would like my prefs to persist.
* As a user, I would like clear documentation.
* As a user, I would like to use  a robust framework.
* As a user, I would like greater than 80% test coverage.
* As a user, I would like an app that analyzes news stories so I can better understand the author's tone or potential biases.
* As a user, I would like to be able to filter my news feed so that I can see news more relevant to my tone preferences.
* As a user, I would like to see articles ranked according to my preferences so that I have a personal news feed.
* As a user, I would like to be able to filter so I can see only the categories I specified.
As a user, I would like to have my preferences persist so they're still there when I return to the page.
