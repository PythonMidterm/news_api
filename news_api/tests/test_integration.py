import json

token = ''


def test_registration(testapp):
    """ Tests new user registration returns a 201 status code
    """
    account = {
        'email': 'test@example.com',
        'password': 'hello',
    }

    response = testapp.post('/api/v1/auth/register/', json.dumps(account))
    global token
    token = response.json['token']
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
    global token
    testapp.authorization = ('Bearer', token)
    response = testapp.post('/api/v1/preferences/', json.dumps(preference_order))
    assert response.status_code == 201


def test_invalid_preferences_lookup_methods(testapp):
    """ Tests that user can't do put or delete to preferences lookup route
    """
    response = testapp.put('/api/v1/preferences/', status='4**')
    assert response.status_code == 405
    response = testapp.delete('/api/v1/preferences/', status='4**')
    assert response.status_code == 405


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
