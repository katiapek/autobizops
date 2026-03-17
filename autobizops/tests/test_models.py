# Test DataBase Models
from autobizops.models import User, Automations, CREDIT_REGISTRATION_GIFT


def test_create_user(db_session):
    u = User(username='alice', email='alice@dromader.pl', password='qwerty123')
    db_session.add(u)
    db_session.commit()

    assert u.id is not None
    assert u.username == 'alice'
    assert u.email == 'alice@dromader.pl'
    assert u.password_hash != 'qwerty123'
    assert u.credits_balance == CREDIT_REGISTRATION_GIFT


def test_unique_email_constraint(db_session):
    u1 = User(username='Bob1', email='bob1@mail.com', password='I am Bob')
    db_session.add(u1)
    db_session.commit()

    u2 = User(username='Bob2', email='bob1@mail.com', password='I am also Bob')
    db_session.add(u2)

    try:
        db_session.commit()
        assert False
    except Exception:
        db_session.rollback()
        assert True


def test_unique_username_constraint(db_session):
    u1 = User(username='Bob1', email='bob1@mail.com', password='I am Bob')
    db_session.add(u1)
    db_session.commit()

    u2 = User(username='Bob1', email='bob2@mail.com', password='I am also Bob')

    db_session.add(u2)
    try:
        db_session.commit()
        assert False
    except Exception:
        db_session.rollback()
        assert True


def test_create_automation(db_session):
    a = Automations(name="Blog Post Generator", cost=25)

    db_session.add(a)
    db_session.commit()

    assert a.id is not None
    assert a.name == 'Blog Post Generator'
    assert a.cost == 25
