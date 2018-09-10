from ..models import Account, Preferences
from sqlalchemy.exc import IntegrityError, DataError
from pyramid_restful.viewsets import APIViewSet
from pyramid.response import Response
import json


class PreferencesAPIView(APIViewSet):
    # Research SQLAlchemy put method. Otherwise, we may need to delete preferences first and then repopulate.
    def create(self, request, preferences_id=None):
        """Post method to create new preferences. We need conditional logic to check if authenticated user.
        """

        try:
            kwargs = json.loads(request.body)
        except json.JSONDecodeError as e:
            return Response(json=e.msg, status=400)

        # NOTE: below comment only applicable if we have separate preferences table.
        # What are we doing here? We're checking if the user is authenticated. If so, get the account and add it to the kwargs (this will become the foreign key to the corresponding account on the Portfolio table).
        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            kwargs['account_id'] = account.id

            try:
                print('HERE ARE THE KWARGS FROM PREFERENCE VIEW:', kwargs)
                Preferences.new(request, **kwargs)
            except IntegrityError:
                # This is the case where they submit preferences that are the same as the old ones. Keeping for now, but maybe don't throw an error, just do nothing.
                return Response(json='Duplicate Key Error. Portfolio already exists.', status=409)



        # else:
            # NOTE: For MVP, we're requiring registration prior to using site. Below comments don't apply yet
            # If not an authenticated user, call the feed get method, but without storing preferences in the database. That is, call feed endpoint from this endpoint.
            # ORRRR, figure out how to cache guest preferences on the server-side. One option is to create a temporary user to keep the logic/flow consistent, but the challenge would be to figure out how to remove them when they leave the page.


        # Don't think we need to send anything back when preferences are changed. But keeping the commented out code below, just in case.
        # schema = PortfolioSchema()
        # data = schema.dump(portfolio).data

        # return Response(json=data, status=201)
