from ..models.schemas import ArchivesSchema
from ..models import Archives
from sqlalchemy.exc import DataError
from pyramid_restful.viewsets import APIViewSet
from pyramid.response import Response


class VisualizationAPIViewset(APIViewSet):
    def list(self, request):
        """Ping database and send back list of all news articles in archives
        """
        try:
            archives_sql = Archives.get_all(request)
        except (DataError, AttributeError):
            return Response(json='Not Found', status=404)
        sample_data = []
        for article in archives_sql:
            schema = ArchivesSchema()
            sample_data.append(schema.dump(article).data)
        print('LOOOOK HERE', sample_data)
        archives_parsed = {}

        for article in archives_sql:
            schema = ArchivesSchema()
            el = schema.dump(article).data
            try:
                archives_parsed[el['dom_tone'].lower()].append({'title': el['title'], 'url': el['url']})
            except KeyError:
                archives_parsed[el['dom_tone'].lower()] = [{'title': el['title'], 'url': el['url']}]
        return Response(json={'archives': archives_parsed}, status=200)
