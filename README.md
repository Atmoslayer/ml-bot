# Чат боты поддержки
Проект содержит чат ботов для телеграма и ВКонтакте для общения с пользователями в формате тех-поддержки.
Боты подключены к нейросети [DialofFlow](https://cloud.google.com/dialogflow). Проект позволяет обучать нейросеть давать конкретные 
ответы на задаваемые вопросы.
## Пример работы бота для телеграма
![](https://github.com/Atmoslayer/ml-bot/blob/main/demo%20gif/demo_tg_bot.gif)
## Пример работы бота для ВКонтакте
![](https://github.com/Atmoslayer/ml-bot/blob/main/demo%20gif/demo_vk_bot.gif)
## Примеры рабочих версий проекта
Проект содержит рабочие версии [телегамм бота](https://t.me/AI_Helper_Atmoslayer_Bot) и бота, подключенного к [группе ВКонтакте](https://vk.com/club212911768).
## Как установить
### Для телеграм бота
Необходимо создать телеграм-бота с помощью отца ботов @BotFather, написав ему и выбрав имена для бота. 
После этого будет получен токен, подобный этому: `1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234`.
Логи работы телеграмм бота отсылаются администратору, телеграмм id которого можно получить,
написав боту @getmyid_bot.
После этого будет получен id наподобие этого: `1234567891`.
### Для ВК бота
Необходимо создать группу ВКонтакте, разрешить в ней отправлять сообщения и получить токен в разделе
`Работа с API`.
В том же разделе появится токен наподобие этого: `vk1.a.4-Abcdfghij_klmnOp...gdf`.
Логи работы вк бота присылаются администратору, вк id которого можно получить из ссылки на свою страницу.
Если id пользователя не меняли, обычно это набор цифр наподобие этого: `1234567778`.
### Для работы с нейросетью
Необходимо [создать](https://dialogflow.cloud.google.com) аккаунт DialogFlow согласно 
[инструкции](https://cloud.google.com/dialogflow/es/docs/quick/setup), после чего создать агента по следующей [инструкции](https://cloud.google.com/dialogflow/docs/quick/build-agent).
После создания проекта необходимо сохранить id проекта содержащий в себе его название, который будет указан на его главной странице.
Пример id: `dialog-flow-project`.
Затем необходимо [включить API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api).
С помощью [консольной утилиты](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk) необходимо получить 
json файл с ключами и добавить его к проекту.
Теперь необходимо [получить токен](https://cloud.google.com/docs/authentication/api-keys) для DialogFlow наподобие этого:
`AbcgfjRglkgjdfgERjgjkllgdfsdfopwr`.
### Для работы проекта
Для хранения токенов в проекте используются переменные окружения. После получения токены и путь к json файлу с ключами необходимо добавить в файл `.env`.
Пример заполненного файла:
```
TG_BOT_TOKEN=1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
GOOGLE_CLOUD_PROJECT=AbcgfjRglkgjdfgERjgjkllgdfsdfopwr
TG_ADMIN_CHAT_ID=1234567891
VK_ADMIN_ID=1234567778
PROJECT_ID=dialog-flow-project
VK_TOKEN=vk1.a.4-Abcdfghij_klmnOp...gdf
```
Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
## Запуск телеграм бота
Бот запускается командой:
```
python3 telegram_bot.py           
```
## Запуск ВК бота
Бот запускается командой:
```
python3 vk_bot.py           
```
## Запуск обучения нейросети
Для запуска обучения нейросети нужно создать и заполнить json файл, содержащий группированные по темам
вопросы и ответ на них. Пример заполнения файла:
```
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
}
```
Путь к файлу указывается с помощью аргумента `--questions_path` (по умолчанию указано questions).
Обучение запускается следующей командой:
```
python3 train_network.py --questions_path C:\Users\atmoslayer\questions.json
```
Если создаваемый набор уже существует в проекте, его создание будет пропущено и в консоль будет выдано
соответствующее уведомление.
## Запуск с помощью docker
Проект содержит dockerfile, позволяющий создать образ и контейнер для проекта.
Docker должен быть установлен и запущен.
Для создания образа используйте `docker build` с указанием имени образа через `-t`:
```commandline
docker build . -t ml_bot
```
Для создания контейнеров используйте `docker run` с указанием имени контейнера через `--name`, указанием пути к .env файлу чере- `--env-file` 
и аргументом для запуска соответствующего бота.
### Запуск телеграм бота через docker
```commandline
docker run --name telegram_bot --env-file=./.env -it ml_bot python telegram_bot.py
```
### Запуск ВК бота через docker
```commandline
docker run --name vk_bot --env-file=./.env -it ml_bot python vk_bot.py
```
После создания контейнеры с ботами будут запущены и готовы к работе.
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).