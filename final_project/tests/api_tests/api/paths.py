class User:
    BASE_PATH = '/api/user'

    login = '/login'

    add_user = BASE_PATH
    delete_user = lambda username: User.BASE_PATH + f'/{username}'
    change_password = lambda username: User.BASE_PATH + f'/{username}/change-password'
    block = lambda username: User.BASE_PATH + f'/{username}/block'
    accept = lambda username: User.BASE_PATH + f'/{username}/accept'


class Application:
    status = '/status'
