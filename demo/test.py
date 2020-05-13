
import pytest

from .app import init


@pytest.fixture
def client(loop, aiohttp_client):
    app = init()
    return loop.run_until_complete(aiohttp_client(app))


TEXT = '''Так говорила в июле 1805 года известная Анна Павловна Шерер,
фрейлина и приближенная императрицы Марии Феодоровны, встречая важного
и чиновного князя Василия, первого приехавшего на ее вечер. Анна
Павловна кашляла несколько дней, у нее был грипп, как она говорила
(грипп был тогда новое слово, употреблявшееся только редкими)'''

SPANS = [
    {'fact': {'slots': [{'key': 'first', 'value': 'Анна'},
                        {'key': 'last', 'value': 'Шерер'},
                        {'key': 'middle', 'value': 'Павловна'}]},
     'normal': 'Анна Павловна Шерер',
     'start': 40,
     'stop': 59,
     'text': 'Анна Павловна Шерер',
     'type': 'PER'},
    {'fact': {'slots': [{'key': 'first', 'value': 'Мария'},
                        {'key': 'last', 'value': 'Феодоровна'}]},
     'normal': 'Мария Феодоровна',
     'start': 97,
     'stop': 113,
     'text': 'Марии Феодоровны',
     'type': 'PER'},
    {'fact': {'slots': [{'key': 'first', 'value': 'Василий'}]},
     'normal': 'Василий',
     'start': 150,
     'stop': 157,
     'text': 'Василия',
     'type': 'PER'},
    {'fact': {'slots': [{'key': 'first', 'value': 'Анна'},
                        {'key': 'last', 'value': 'Павловна'}]},
     'normal': 'Анна Павловна',
     'start': 192,
     'stop': 205,
     'text': 'Анна\nПавловна',
     'type': 'PER'}
]


async def test(client):
    response = await client.post(
        '/api/doc/spans',
        data={'text': TEXT}
    )
    assert response.status == 200
    data = await response.json()

    assert data == SPANS
