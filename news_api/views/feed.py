from ..models.schemas import FeedSchema
from ..models import Feed
from ..models import Account
from sqlalchemy.exc import IntegrityError, DataError
from pyramid_restful.viewsets import APIViewSet
from pyramid.response import Response
import requests
import json

#

class FeedAPIView(APIViewSet):
    def list(self, request):
        """Ping database and send back list of all news articles
        """

        # FIRST, get preferences for that user.
        # IF no preferences, add default preferences (Maybe do this when account is created)
        # THEN, get everything from the database.
        # FINALLY, sort it all our according to the preferences.

        try:
            preferences = Account.get_prefs()
        except (DataError, AttributeError):
            return Response(json='Not Found', status=404)

        try:
            feed = Feed.get_all()
        except (DataError, AttributeError):
            return Response(json='Not Found', status=404)

        schema = FeedSchema()
        data = schema.dump(feed).data

        # Insert some sorting logic according to preferences


        return Response(json={'feed': data}, status=200)
