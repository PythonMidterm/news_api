from pyramid_restful.viewsets import APIViewSet
from pyramid.response import Response
from sqlalchemy.exc import IntegrityError
from ..models import Account
from ..models import Preferences
import json


class AuthAPIView(APIViewSet):
    def create(self, request, auth=None):
        """POST method to api/v1/auth endpoint. Currently, no database setup.
        """
        data = json.loads(request.body.decode())
        if auth == 'register':
            # TODO: Pull in Preferences model and add default preferences after account is created.
            try:
                user = Account.new(
                    request,
                    data['email'],
                    data['password'])
            except (IntegrityError, KeyError):
                return Response(json='Bad Request', status=400)

            default_preferences = ['analytical', 'tentative', 'joy', 'confident', 'sadness', 'fear', 'anger']
            kwargs = {}
            kwargs['preference_order'] = default_preferences
            print(user)
            # kwargs['account_id'] = account.id


            return Response(
                json_body={
                    'token': request.create_jwt_token(
                        user.email,
                        roles=[role.name for role in user.roles],
                        userName=user.email,
                    )
                },
                status=201
            )

        if auth == 'login':
            authenticated = Account.check_credentials(request, data['email'], data['password'])

            if authenticated:
                return Response(
                    json_body={
                        'token': request.create_jwt_token(
                            authenticated.email,
                            roles=[role.name for role in authenticated.roles],
                            userName=authenticated.email
                        )
                    },
                    status=201
                )

            return Response(json='Not Authorized', status=401)

        return Response(json='Not Found', status=404)
