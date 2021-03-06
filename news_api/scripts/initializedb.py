import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
# from ..models import MyModel
from ..models import Feed, Account, AccountRole, roles_association


def usage(argv):
    """ Formats a string to print to the user to help them use the app
    """
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """Function that enables initializedb CLI command.
    """
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    # Creates a connection to the DB
    engine = get_engine(settings)
    # Creates tables for our models in the DB
    Base.metadata.create_all(engine)

    # Below is used for seeding the DB

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        roles = ['admin', 'view']
        for role in roles:
            model = AccountRole(name=role)
            dbsession.add(model)
