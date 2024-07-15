from sqlalchemy import select

from fast_study.models import User


def test_create_user(session):
    new_user = User(
        username='user_exemplo', password='secret', email='teste@test'
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'user_exemplo'))

    assert user.username == 'user_exemplo'
