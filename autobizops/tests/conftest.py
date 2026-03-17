import pytest

from autobizops import app, db


@pytest.fixture
def db_session():
    """ Function scope test in memory"""
    app.config.update(
        TESTING=True,
        SQL_DATABASE_URI='sqlite:///:memory:',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    with app.app_context():

        db.create_all()
        try:
            yield db.session
            db.session.commit()
        finally:
            db.session.remove()
            db.drop_all()
