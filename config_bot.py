# це файл config_bot.py

# тексти в повідомленнях (текстах) і на кнопках, позначення: _TXT - повідомлення, _BTN - кнопка
# щоб зробити перехід на нову строку, треба поставити "\n"
# API_TOKEN  ключ вашего бота из @BotFather
# CHANNEL_USERNAME юзернейм вашого канала типу @username (обязательно)
# CHANNEL_ID_1 идентификатор вашего телеграмма полученный из @userinfobot

# BGN_TXT - текст після підписки
# LID_BTN - кнопка після підписки
# LID_TXT - текст після натискання на LID_BTN
# TEST1_TXT - показується один раз після підписки, слідуючі натискання на TEST_BTN його не виводять
# TEST2_TXT - завжди виводиться при натискання на TEST_BTN 
# LID_TIME1_TXT - текст через LID_TIME1 после нажатия на LID_BTN (только раз после подписки будет)
# LID_TIME2_TXT - текст через LID_TIME2 после нажатия на LID_BTN (только раз после подписки будет)
# TEST_TIME1_TXT - текст через TEST_TIME1 после нажатия на TEST_BTN (только раз после подписки будет)
# TEST_TIME2_TXT - текст через TEST_TIME2 после нажатия на TEST_BTN (только раз после подписки будет)
API_TOKEN = "8129449329:AAG6BNXeYQn6XwcHdgSm_sBqUJnjeeRq5_8"
CHANNEL_USERNAME = "@Channel_Qy"
CHANNEL_ID_1 = 903001450  # свій чат з ботом для отримання повідомлень 

BGN_TXT="За всем не уследишь. Предлагаем бот, который автоматизирует ваши продажи Узнать здесь: https://sherproart.github.io/shinypesok/describe_bot.html"
LID_BTN="Взрывные продажи с лид-магнитом"
LID_TXT="Лид-магнит ваш! Хотите больше продаж? \nПереходите по ссылке: https://vlad12121212.github.io/Vlad/output.html"
BAY_BTN="Бери бота за $100 - время денег"
BAY_TXT="Вот ссылка на оплату ($100)."
RENT_BTN="Аренда за $15/мес"
TEST_BTN="Тест 14 дней бесплатно"
TEST1_TXT="Тест активирован! Мы напомним вам через 10 дней."
TEST2_TXT="Вот ссылка на личку ..."
LID_TIME1_TXT="Чек-лист помог? 80% малого бизнеса теряют клиентов из-за слабой воронки."
LID_TIME2_TXT="Не упусти шанс! Бот за 100$ удвоит ваши продажи. Последний день скидки."
TEST_TIME1_TXT="Осталось 4 дня теста! Бот работает? Продолжай за $15/мес"
TEST_TIME2_TXT="Пробный период окончен. Бот выключен."
# пример записи времени: LID_TIME1=4*3600  - 4 часа
# пример записи времени: LID_TIME1=5*24*3600  - 5 суток
# LID_TIME1 - время после нажатия на LID_BTN в секундах - первый вывод напоминания
# LID_TIME2 - время после нажатия на LID_BTN в секундах - второй вывод напоминания
# TEST_TIME1 - время после нажатия на TEST_BTN в секундах - первый вывод напоминания
# TEST_TIME2 - время после нажатия на TEST_BTN в секундах - второй вывод напоминания
LID_TIME1=10
LID_TIME2=20
TEST_TIME1=40
TEST_TIME2=60

# вимикання кнопки для тестового періоду, 
# для вимкнення треба написати: TEST_BTN_ENABLE=0
# для ввімкнення треба написати: TEST_BTN_ENABLE=1

TEST_BTN_ENABLE=1
