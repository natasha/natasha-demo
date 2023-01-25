
import pytest

from app import init


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

MORPH = '''
                 Так ADV|Degree=Pos
            говорила VERB|Aspect=Imp|Gender=Fem|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Act
                   в ADP
                июле NOUN|Animacy=Inan|Case=Loc|Gender=Masc|Number=Sing
                1805 ADJ
                года NOUN|Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing
           известная ADJ|Case=Nom|Degree=Pos|Gender=Fem|Number=Sing
                Анна PROPN|Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing
            Павловна PROPN|Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing
               Шерер PROPN|Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing
                   , PUNCT
            фрейлина NOUN|Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing
                   и CCONJ
        приближенная NOUN|Animacy=Inan|Case=Dat|Gender=Neut|Number=Sing
         императрицы NOUN|Animacy=Anim|Case=Gen|Gender=Fem|Number=Sing
               Марии PROPN|Animacy=Anim|Case=Gen|Gender=Fem|Number=Sing
          Феодоровны PROPN|Animacy=Anim|Case=Gen|Gender=Fem|Number=Sing
                   , PUNCT
            встречая VERB|Aspect=Imp|Tense=Pres|VerbForm=Conv|Voice=Act
             важного ADJ|Animacy=Anim|Case=Acc|Degree=Pos|Gender=Masc|Number=Sing
                   и CCONJ
           чиновного ADJ|Case=Gen|Degree=Pos|Gender=Masc|Number=Sing
               князя NOUN|Animacy=Anim|Case=Gen|Gender=Masc|Number=Sing
             Василия PROPN|Animacy=Anim|Case=Gen|Gender=Masc|Number=Sing
                   , PUNCT
             первого ADJ|Case=Gen|Degree=Pos|Gender=Masc|Number=Sing
         приехавшего VERB|Aspect=Perf|Case=Gen|Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part|Voice=Act
                  на ADP
                  ее DET
               вечер NOUN|Animacy=Inan|Case=Acc|Gender=Masc|Number=Sing
                   . PUNCT
'''[1:]


async def test_spans(client):
    response = await client.post(
        '/api/doc/spans',
        data={'text': TEXT}
    )
    assert response.status == 200
    data = await response.json()

    assert data == SPANS


async def test_viz(client):
    response = await client.post(
        '/api/doc/viz',
        data={'text': TEXT}
    )
    assert response.status == 200
    data = await response.json()

    assert data['morph'] == MORPH
