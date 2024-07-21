from http import HTTPStatus

from fast_study.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World - Root'}


def test_create_user(client):
    # Act
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_deve_retornar_bad_request_username_already_exists(
    client, user
):
    # Act
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'testepass@test.com',
            'password': 'testpassword',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_deve_retornar_bad_request_email_already_exists(
    client, user
):
    # Act
    response = client.post(
        '/users/',
        json={
            'username': 'TestPass',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    # Act
    response = client.get('/users/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    # Arrange
    user_schema = UserPublic.model_validate(user).model_dump()

    # Act
    response = client.get('/users/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    # Act
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_deve_retornar_not_found(client):
    # Act
    response = client.put(
        '/users/5',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    # Act
    response = client.delete('/users/1')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_deve_retornar_not_found(client):
    # Act
    response = client.delete('/users/5')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user_by_id(client, user):
    # Act
    response = client.get('/users/1')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Teste',
        'email': 'teste@test.com',
        'id': 1,
    }


def test_read_user_by_id_deve_retornar_not_found(client):
    # Act
    response = client.get('/users/5')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
