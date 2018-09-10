# import requests
# import unittest
# from pyramid import testing
# import transaction


# def dummy_request(dbsession):
#     return testing.DummyRequest(dbsession=dbsession)


# class BaseTest(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp(settings={
#             'sqlalchemy.url': 'postgres://localhost:5432/news_test'
#         })
#         self.config.include('.models')
#         settings = self.config.get_settings()

#         from .models import (
#             get_engine,
#             get_session_factory,
#             get_tm_session,
#             )

#         self.engine = get_engine(settings)
#         session_factory = get_session_factory(self.engine)

#         self.session = get_tm_session(session_factory, transaction.manager)

#     def init_database(self):
#         from .models.meta import Base
#         Base.metadata.create_all(self.engine)

#     def tearDown(self):
#         from .models.meta import Base

#         testing.tearDown()
#         transaction.abort()
#         Base.metadata.drop_all(self.engine)
import json


def test_registration(testapp):
    """ Tests new user registration returns a 201 status code
    """
    account = {
        'email': 'test@example.com',
        'password': 'hello',
    }

    response = testapp.post('/api/v1/auth/register/', json.dumps(account))
    assert response.status_code == 201
    assert response.json['token']


def test_invalid_registration(testapp):
    """ Tests invalid registration returns 400 status code
    """
    account = {
        'email': 'test_two@example.com',
    }

    response = testapp.post('/api/v1/auth/register/', json.dumps(account), status='4**')
    assert response.status_code == 400


def test_login(testapp):
    """ Tests login route returns 201 status code
    """
    account = {
        'email': 'test@example.com',
        'password': 'hello',
    }

    response = testapp.post('/api/v1/auth/login/', json.dumps(account))
    assert response.status_code == 201
    assert response.json['token']


def test_preferences_lookup(testapp):
    """ Tests to have user look up by preferences
    """
    preference_order = {
        'preference_order': 'test@example.com',
    }
    response = testapp.post('/api/v1/preferences/', json.dumps(preference_order))
    assert response.status_code == 201


# def test_invalid_lookup_methods(testapp):
#     """
#     """
#     response = testapp.put('/api/v1/lookup/98109', status='4**')
#     assert response.status_code == 405
#     response = testapp.delete('/api/v1/lookup/98109', status='4**')
#     assert response.status_code == 405
#     response = testapp.post('/api/v1/lookup/98109', status='4**')
#     assert response.status_code == 405


# def test_create_location(testapp):
#     """
#     """
#     account = {
#         'email': 'test@example.com',
#         'password': 'hello',
#     }

#     token = testapp.post('/api/v1/auth/login', json.dumps(account)).json['token']

#     location = {
#         'name': 'Seattle',
#         'zip_code': 98109
#     }
#     testapp.authorization = ('Bearer', token)
#     response = testapp.post('/api/v1/location', json.dumps(location))
#     assert response.status_code == 201
