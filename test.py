import main

request = {
  "meta": {
    "locale": "ru-RU",
    "timezone": "UTC",
    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
    "interfaces": {
      "screen": {},
      "payments": {},
      "account_linking": {}
    }
  },
  "session": {
    "message_id": 2,
    "session_id": "59ac499e-a0a6-454a-adfe-43307273c13c",
    "skill_id": "e16c6f77-619d-4653-8f00-2f271796619d",
    "user": {
      "user_id": "9F987CE372B265013E6A4E49594AD8A632B3A12690DDBB735E53B90F050311E7"
    },
    "application": {
      "application_id": "5BFCD8908EE79A05963BBC65834A335D919979B34563C3E00301A94B11C569FE"
    },
    "new": False,
    "user_id": "5BFCD8908EE79A05963BBC65834A335D919979B34563C3E00301A94B11C569FE"
  },
  "request": {
    "command": "стальной алхимик",
    "original_utterance": "Атака титанусов",
    "nlu": {
      "tokens": [
        "стальной",
        "алхимик"
      ],
      "entities": [],
      "intents": {}
    },
    "markup": {
      "dangerous_context": False
    },
    "type": "SimpleUtterance"
  },
  "version": "1.0"
}

print(main.handler(request, [])['response']['text'])

