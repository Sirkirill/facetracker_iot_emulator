BASE_URL = 'https://facein-backend.herokuapp.com'

URL = {
    'move': '/api/moves/move/',
    'cameras': '/api/moves/cameras/',
    'companies': '/api/companies/'
}


def get_url(name):
    return f'{BASE_URL}{URL[name]}'
