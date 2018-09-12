from ..models import Account, Preferences
from ..models.schemas import PreferencesSchema
from sqlalchemy.exc import IntegrityError, DataError
from pyramid_restful.viewsets import APIViewSet
from pyramid.response import Response
import json


class PreferencesAPIView(APIViewSet):
    def create(self, request, preferences_id=None):
        """Post method to create new preferences. We need conditional logic to check if authenticated user.
        """

        try:
            kwargs = json.loads(request.body)
            kwargs['preference_order'] = json.loads(request.body.decode())['preference_order']
        except json.JSONDecodeError as e:
            return Response(json=e.msg, status=400)

        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            kwargs['account_id'] = account.id

            try:
                # import pdb; pdb.set_trace()
                preferences = Preferences.new(request, **kwargs)
            except IntegrityError:
                # This is the case where they submit preferences that are the same as the old ones. Keeping for now, but maybe don't throw an error, just do nothing.
                return Response(json='Duplicate Key Error. Portfolio already exists.', status=409)

            schema = PreferencesSchema()
            data = schema.dump(preferences).data

            return Response(json=data, status=201)

    # TODO: (GET api/v1/preferences) Write retrieve method to get user's preferences from database. Follow logic of first "if" conditional in views/.py list method.

