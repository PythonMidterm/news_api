from ..models.schemas import FeedSchema
from ..models.schemas import PreferencesSchema
from ..models import Feed
from ..models import Preferences
from ..models import Account
from sqlalchemy.exc import IntegrityError, DataError
from pyramid_restful.viewsets import APIViewSet
from pyramid.response import Response
import requests
import json


class FeedAPIView(APIViewSet):
    def list(self, request):
        """Ping database and send back list of all news articles
        """

        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            preferences = Preferences.oneByKwarg(request, account.id)

        schema = PreferencesSchema()
        preference_order = schema.dump(preferences).data['preference_order']

        print('HERE ARE THE PREFS', preference_order)

        try:
            feed_sql = Feed.get_all(request)
        except (DataError, AttributeError):
            return Response(json='Not Found', status=404)

        feed_parsed = {}

        for article in feed_sql:
            schema = FeedSchema()
            el = schema.dump(article).data
            try:
                feed_parsed[el['dom_tone'].lower()].append({'title': el['title'], 'url': el['url']})
            except KeyError:
                feed_parsed[el['dom_tone'].lower()] = [{'title': el['title'], 'url': el['url']}]

        feed_sorted = {}

        # import pdb; pdb.set_trace()
        for pref in preference_order:
            try:
                feed_sorted[pref] = feed_parsed[pref]
            except KeyError:
                continue




        print('THE FEEEED', feed_sorted)


        return Response(json={'feed': feed_sorted}, status=200)
