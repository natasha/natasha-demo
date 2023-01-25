
# natasha-demo ![CI](https://github.com/natasha/natasha-demo/actions/workflows/test.yml/badge.svg)

```bash
$ curl -X POST https://bbae7714ctds8cfj0g51.containers.yandexcloud.net/api/doc/viz -F text='Простите, еще несколько цитат из приговора. «…Отрицал существование Иисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами ожившего мертвеца — зомби» [и] «качествами покемонов — представителей бестиария японской мифологии, тем самым совершил преступление, предусмотренное статьей 148 УК РФ».'

{
  "ner": "Простите, еще несколько цитат из приговора. «…Отрицал существование \nИисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами \n                                      PER──────────            \nожившего мертвеца — зомби» [и] «качествами покемонов — представителей \nбестиария японской мифологии, тем самым совершил преступление, \nпредусмотренн
ое статьей 148 УК РФ».\n                               LO  \n",
  "morph": "            Простите VERB|Aspect=Perf|Mood=Imp|Number=Plur|Person=2|VerbForm=Fin|Voice=Act\n                   , PUNCT\n                 еще ADV|Degree=Pos\n
несколько NUM|Case=Nom\n               цитат NOUN|Animacy=Inan|Case=Gen|Gender=Fem|Number=Plur\n                  из ADP\n           приговора NOUN|Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing\n                   . PUNCT\n",
  "syntax": "       Простите  \n┌────► ,         punct\n│   ┌► еще       advmod\n│ ┌►└─ несколько nummod:gov\n└─└─── цитат     \n│   ┌► из        case\n└──►└─ приговора nmod\n       .         \n",
  "spans": [
    {
      "start": 106,
      "stop": 119,
      "type": "PER",
      "text": "Иисуса Христа",
      "normal": "Иисус Христос",
      "fact": {
        "slots": [
          {
            "key": "first",
            "value": "Иисус"
          },
          {
            "key": "last",
            "value": "Христос"
          }
        ]
      }
    },
    {
      "start": 295,
      "stop": 297,
      "type": "LOC",
      "text": "РФ",
      "normal": "РФ"
    }
  ]
}

```

## Development

Dev env

```bash
python -m venv ~/.venvs/natasha-demo
source ~/.venvs/natasha-demo/bin/activate

pip install -r requirements/app.txt -r requirements/test.txt
```

Test + lint

```bash
make test
```

Create YC folder

```bash
yc resource-manager folder create --name natasha-demo
```

Create YC registry

```bash
yc container registry create default --folder-name natasha-demo

# Save registry_id to Makefile
```

Make registry public

```bash
yc container registry add-access-binding default \
  --role container-registry.images.puller \
  --subject system:allUsers \
  --folder-name natasha-demo
```

Create YC Serverless Container

```bash
yc serverless container create --name default --folder-name natasha-demo
```

Make container endpoint public

```bash
yc serverless container allow-unauthenticated-invoke default \
  --folder-name natasha-demo
```

Logs

```bash
yc log read default --follow --folder-name natasha-demo
```
