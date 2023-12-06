import pytest
from app import schemas
from jose import JWTError, jwt
from app.config import settings


def test_create_user(client):
    res = client.post('/users/', json={
        'email': 'someone@example.com',
        'password': 'password123'
    })
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'someone@example.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post('/login', data={
        'username': test_user['email'],
        'password': test_user['password']
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, settings.algorithm)
    id = payload.get('user_id')

    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'


@pytest.mark.parametrize('email, password, status_code', [('wrongemail@gmail.com', 'password123', 403), ('someone@example.com', 'wrongPassword', 403), ('wrongemail@gmail.com', 'wrongPassword', 403), (None, 'password123', 422), ('someone@example.com', None, 422)])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        '/login', data={'username': email, 'password': password})
    assert res.status_code == status_code
