
# natasha-demo ![CI](https://github.com/natasha/natasha-demo/workflows/CI/badge.svg) [![codecov](https://codecov.io/gh/natasha/natasha-demo/branch/master/graph/badge.svg)](https://codecov.io/gh/natasha/natasha)

```bash
$ python -m demo.app
2020-05-08 08:47:57,841 Loading dictionaries from /Users/alexkuk/envs/py36/lib/python3.6/site-packages/pymorphy2_dicts/data
2020-05-08 08:47:57,936 format: 2.4, revision: 393442, updated: 2015-01-17T16:03:56.586168
======== Running on http://0.0.0.0:4000 ========
(Press CTRL+C to quit)

$ curl -X POST http://localhost:4000/api/doc/spans -F text='Простите, еще несколько цитат из приговора. «…Отрицал существование Иисуса и пророка Мухаммеда», «наделял Иисуса Х
риста качествами ожившего мертвеца — зомби» [и] «качествами покемонов — представителей бестиария японской мифологии, тем самым совершил преступление, предусмотренное статьей 148 УК РФ».' | jq .
[
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

```
