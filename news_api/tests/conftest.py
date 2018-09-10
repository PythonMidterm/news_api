# I think he copied from Kat's repo here. Also, musflood on github.
import pytest
import transaction
from ..models.meta import Base
from ..models import get_tm_session, AccountRole


@pytest.fixture(scope='session')
def testapp(request):
    """Function that sets up a test app
    """
    from webtest import TestApp
    from pyramid.config import Configurator
    from pyramid.authorization import ACLAuthorizationPolicy
    from pyramid.security import Allow, ALL_PERMISSIONS

    class RootACL:
        __acl__ = [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, 'view', ['read']),
        ]

        def __init__(self, request):
            pass

    def add_role_principals(userid, request):
        return request.jwt_claims.get('roles', [])

    def main():
        """ Function that returns a Pyramid WSGI app with included settings
        """
        settings = {
            'sqlalchemy.url': 'postgresql://localhost:5432/news_test'
        }
        # news_test is a postgres db set up to be used to run these tests

        config = Configurator(settings=settings)
        config.include('pyramid_jwt')
        config.include('pyramid_restful')

        config.set_root_factory(RootACL)
        config.set_authorization_policy(ACLAuthorizationPolicy())
        config.set_jwt_authentication_policy(
            'superseekretseekrit',
            auth_type='Bearer',
            callback=add_role_principals,
        )

        config.include('news_api.models')
        config.include('news_api.routes')
        config.scan()

        return config.make_wsgi_app()

    app = main()

    SessionFactory = app.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(bind=engine)

    with transaction.manager:
        db_session = get_tm_session(SessionFactory, transaction.manager)
        roles = ['admin', 'view']
        for role in roles:
            model = AccountRole(name=role)
            db_session.add(model)

    def tear_down():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tear_down)

    return TestApp(app)
