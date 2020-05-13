
# natasha-demo ![CI](https://github.com/natasha/natasha-demo/workflows/CI/badge.svg) [![codecov](https://codecov.io/gh/natasha/natasha-demo/branch/master/graph/badge.svg)](https://codecov.io/gh/natasha/natasha)

```bash
$ curl -X POST http://natasha-demo.herokuapp.com/api/doc/viz -F text='Простите, еще несколько цитат из приговора. «…Отрицал существование Иисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами ожившего мертвеца — зомби» [и] «качествами покемонов — представителей бестиария японской мифологии, тем самым совершил преступление, предусмотренное статьей 148 УК РФ».' | jq .

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

```
heroku logs --app natasha-demo --tail

2020-05-13T12:20:56.690422+00:00 app[web.1]: 2020-05-13 12:20:56,690 10.37.18.30 [13/May/2020:12:20:56 +0000] "POST /api/doc/spans HTTP/1.1" 200 641 "-" "curl/7.49.1"
2020-05-13T12:20:56.702002+00:00 heroku[router]: at=info method=POST path="/api/doc/spans" host=natasha-demo.herokuapp.com request_id=c9734c31-afb8-4666-8b1b-a5f4b7b77766 fwd="77.50.131.197" dyno=web.1 connect=1ms service=276ms status=200 bytes=641 protocol=http
2020-05-13T12:21:19.010276+00:00 app[web.1]: 2020-05-13 12:21:19,010 Простите, еще несколько цитат из приговора. «…Отрицал существование Иисуса и пророка Мухаммеда», «наделял Иисуса Христа качествами ожившего мертвеца — зомби» [и] «качествами покемонов — представителей бестиария японской мифологии, тем самым совершил преступление, предусмотренное статьей 148 УК РФ».
2020-05-13T12:21:19.013027+00:00 app[web.1]: 2020-05-13 12:21:19,012 10.9.82.109 [13/May/2020:12:21:17 +0000] "POST /api/doc/viz HTTP/1.1" 200 3489 "-" "curl/7.49.1"
2020-05-13T12:21:19.020233+00:00 heroku[router]: at=info method=POST path="/api/doc/viz" host=natasha-demo.herokuapp.com request_id=17b3f370-0f9f-48bc-b74a-f725bda6b92b fwd="77.50.131.197" dyno=web.1 connect=1ms service=1093ms status=200 bytes=3489 protocol=http

```
