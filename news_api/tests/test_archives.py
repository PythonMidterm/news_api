def test_constructed_entry_added_to_database(db_session):
    """Test adding a complete article entry."""
    from ..models import Archives

    assert len(db_session.query(Archives).all()) == 0
    article = Archives(
        title='Any News',
        url='http://www.cnn.com',
        description='Anything is possible',
        source='fox news',
        date_published='any',
        dom_tone='Joy',
        image='any'
    )

    db_session.add(article)
    assert len(db_session.query(Archives).all()) == 1


def test_constructed_entry_with_incomplete_added(db_session):
    """Test adding incomplete data but with required fields."""
    from ..models import Archives

    assert len(db_session.query(Archives).all()) == 0
    article = Archives(
        title='TEST2',
        url='Test Conglomerate'
    )
    db_session.add(article)
    assert len(db_session.query(Archives).all()) == 1


