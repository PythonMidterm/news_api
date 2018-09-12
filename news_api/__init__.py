from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, ALL_PERMISSIONS
from .utils.scheduler import job
from .schedule import schedule
import time


class RootACL:
    __acl__ = [
        (Allow, 'admin', ALL_PERMISSIONS),
        (Allow, 'view', ['read']),
    ]

    def __init__(self, request):
        pass


def add_role_principals(userid, request):
    return request.jwt_claims.get('roles', [])


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jwt')
    config.include('pyramid_restful')

    config.set_root_factory(RootACL)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_jwt_authentication_policy(
        'superseekretseekrit',  # os.environ.get('SECRET', None)
        auth_type='Bearer',
        callback=add_role_principals,
    )

    config.include('.models')
    config.include('.routes')
    # config.include('.utils')
    config.scan()
    schedule.every(30).seconds.do(job)
    schedule.run_continuously()
    return config.make_wsgi_app()
