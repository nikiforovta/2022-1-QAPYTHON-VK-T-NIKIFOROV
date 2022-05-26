import json
import random


def test_add_user(socket_client, test_user):
    post_data = socket_client.post('/add_user', {'name': test_user})
    assert socket_client.get_response_code(post_data) == 201


def test_get_added_user(socket_client, test_user):
    post_data = socket_client.post('/add_user', {'name': test_user})
    get_data = socket_client.get(f'/get_user/{test_user}')
    assert socket_client.get_response_code(get_data) == 200
    assert json.loads(post_data[-1])['user_id'] == json.loads(get_data[-1])['user_id']


def test_add_existent_user(socket_client, test_user):
    for i in range(random.randint(2, 10)):
        post_data = socket_client.post('/add_user', {'name': test_user})
    assert socket_client.get_response_code(post_data) == 400


def test_get_non_existent_user(socket_client, test_user):
    get_data = socket_client.get(f'/{test_user}')
    assert socket_client.get_response_code(get_data) == 404


def test_with_age(socket_client, test_user):
    socket_client.post('/add_user', {"name": test_user})
    get_data = socket_client.get(f'/get_user/{test_user}')
    age = int(json.loads(get_data[-1])['age'])
    assert 0 <= age <= 100


def test_has_surname(socket_client, test_user):
    socket_client.post('/add_user', {"name": test_user})
    put_data = socket_client.put(f'/update_surname/{test_user}', {'surname': test_user[::-1]})
    assert socket_client.get_response_code(put_data) == 200

    get_data = socket_client.get(f'/get_user/{test_user}')
    surname = json.loads(get_data[-1])['surname']
    assert surname == test_user[::-1]


def test_update_surname(socket_client, test_user):
    socket_client.post('/add_user', {"name": test_user})
    put_data = socket_client.put(f'/update_surname/{test_user}', {'surname': test_user[::-1]})
    assert socket_client.get_response_code(put_data) == 200

    put_data = socket_client.put(f'/update_surname/{test_user}', {'surname': test_user})
    assert socket_client.get_response_code(put_data) == 200

    get_data = socket_client.get(f'/get_user/{test_user}')
    surname = json.loads(get_data[-1])['surname']
    assert surname == test_user


def test_update_without_surname(socket_client, test_user):
    socket_client.post('/add_user', {"name": test_user})
    put_data = socket_client.put(f'/update_surname/{test_user}')

    assert socket_client.get_response_code(put_data) == 400


def test_remove_existing_surname(socket_client, test_user):
    socket_client.post('/add_user', {"name": test_user})
    socket_client.put(f'/update_surname/{test_user}', {'surname': test_user[::-1]})
    delete_data = socket_client.delete(f'/delete_surname/{test_user}')

    assert socket_client.get_response_code(delete_data) == 200


def test_remove_empty_surname(socket_client, test_user):
    socket_client.post('/add_user', {"name": test_user})
    delete_data = socket_client.delete(f'/delete_surname/{test_user}')

    assert socket_client.get_response_code(delete_data) == 404
