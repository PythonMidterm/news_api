import json

token = ''


""" Auth Tests for reg and login- api/v1/auth/login/
and api/v1/auth/register/ """


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


def test_good_login(testapp):
    """ Tests login route returns 201 status code
    """
    account = {
        'email': 'test@example.com',
        'password': 'hello',
    }

    response = testapp.post('/api/v1/auth/login/', json.dumps(account))
    assert response.status_code == 201
    assert response.json['token']


# def test_bad_login(testapp):
#     """ Tests bad login returns 400
#     """
#     account = {
#         'email': 'test@example.com',
#     }

#     response = testapp.post('/api/v1/auth/login/', json.dumps(account))
#     assert response.status_code == 401
#     # assert response.json['token']


""" Preferences Tests- api/v1/preferences/"""


def test_preferences_post_auth(testapp):
    """ Tests authenticated user posting new prefs
    """
    preference_order = {
        'preference_order': 'test@example.com',
    }
    global token
    testapp.authorization = ('Bearer', token)
    response = testapp.post('/api/v1/preferences/', json.dumps(preference_order))
    assert response.status_code == 201


# def test_preferences_post_not_auth(testapp):
#     """ Test cannot post preferences without auth
#     """
#     preference_order = {
#         'preference_order': 'test_1@example.com',
#     }
#     response = testapp.post('/api/v1/preferences/', json.dumps(preference_order))
#     assert response.status_code == 400


def test_prefs_rtn_integrity_error_if_already_in_db():
    """ Test if authenticated, that if you try to update prefs, but they're
    the same, throws integrity error
    """
    pass


def test_get_prefs_auth():
    """ Tests that an authenticated user can see prefs
    """
    pass


def test_not_auth_cannot_see_prefs():
    """ Tests that a non-authenticated user canot see prefs
    """
    pass


def test_invalid_preferences_lookup_methods(testapp):
    """ Tests that user can't do put or delete to preferences lookup route
    """
    response = testapp.put('/api/v1/preferences/', status='4**')
    assert response.status_code == 405
    response = testapp.delete('/api/v1/preferences/', status='4**')
    assert response.status_code == 405


""" Feed tests- api/v1/feed """


def test_get_feed_auth():
    """ Tests authorized user can get feed
    """
    pass


def test_get_feed_not_auth():
    """ Tests unauthorized user cannot get feed
    """
    pass


def test_default_prefs_auth():
    """ Tests default user prefs work when none given
    """


def test_invalid_feed_lookup_methods(testapp):
    """ Tests you cannot delete or post to the feed
    """
    response = testapp.put('/api/v1/feed/', status='4**')
    assert response.status_code == 405
    response = testapp.delete('/api/v1/feed/', status='4**')
    assert response.status_code == 405
    response = testapp.post('/api/v1/feed/', status='4**')
    assert response.status_code == 405


# def test_get_from_db(testapp):
#     """ Tests new user registration returns a 201 status code
#     """
#     account = {
#         'email': 'test@example.com',
#         'password': 'hello',
#     }

#     response = testapp.post('/api/v1/auth/register/', json.dumps(account))
#     global token
#     token = response.json['token']
#     assert response.status_code == 201
#     assert response.json['token']
#     response = testapp.get('/api/v1/auth/profile/')
    # assert response has the correct data in it
