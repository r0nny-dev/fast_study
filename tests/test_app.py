from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_study.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World - Root'}
