from pyramid.response import Response
from pyramid.view import view_config
from textwrap import dedent

# TODO: Change this

@view_config(route_name='home', renderer='json', request_method='GET')
def home_view(request):
    """Get method to hit the root route.
    """
    message = dedent('\nGET / - the base API route\nPOST /api/v1/auth/{auth} - for registering a new account and signing up\nPOST /api/v1/preferences/ - for modifying default tone order preferences\nGET /api/v1/feed/ - for listing the news feed according to the user preferences\nGET /api/v1/visuals/{source}/ - Retrieve a data visualization for a specified news outlet. Takes query in form of ?type=pie\n')
    return Response(body=message, status=200)
