__version__ = (1, 6, 4)

#            © Copyright 2024
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# meta banner:https://t.me/HikkTutor
# name: Doxer 
from .. import loader, utils
import random
import asyncio
from telethon.tl.types import User, Channel
from datetime import datetime, timedelta
import requests

@loader.tds
class Doxer(loader.Module):
    """Модуль для фейк-доксинга пользователей чата."""
    strings = {'name': 'Doxer'}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "animation_type",
                "standart",
                lambda: "Тип анимации: короткая, стандартная или длинная",
                validator=loader.validators.Choice(["short", "standart", "long"])
            ),
            loader.ConfigValue(
                "InfoAnimation",
                False,
                lambda: "Включить построчное отображение результатов",
                validator=loader.validators.Boolean()
            )
        )
        self.is_doxing = False

        self.male_names = [
            "Александр", "Дмитрий", "Иван", "Максим", "Артем", "Сергей", "Юрий",
            "Роман", "Виталий", "Денис", "Алексей", "Владислав", "Никита", "Станислав",
            "Егор", "Федор", "Антон", "Григорий", "Семен", "Павел", "Игорь", "Анатолий",
            "Кирилл", "Даниил", "Ярослав", "Рустам", "Виктор", "Илья", "Петр",
            "Николай", "Филипп", "Михаил", "Василий", "Арсен", "Савва", "Валентин",
            "Евгений", "Геннадий", "Артемий", "Матвей", "Леонид", "Тимур", "Данил",
            "Руслан", "Марк", "Валерий", "Владимир", "Георгий", "Арсений", "Борис",
            "Глеб", "Евграф", "Константин", "Лука", "Мирон", "Олег", "Прохор",
            "Родион", "Трофим", "Юлиан", "Ян", "Альберт", "Богдан", "Вадим", "Давид",
            "Елисей", "Захар", "Игнат", "Клим", "Лев", "Мартин", "Назар", "Платон",
            "Ратмир", "Савелий", "Тихон", "Филипп", "Эмиль", "Яромир", "Роберт",
            "Станислав", "Федот", "Юрий", "Яков", "Аристарх", "Бернард", "Варфоломей",
            "Герасим", "Демид", "Ефим", "Зиновий", "Иосиф", "Касьян", "Леон", "Митрофан",
            "Никон", "Остап", "Панкрат", "Ренат", "Сидор", "Терентий", "Устин",
            "Харитон", "Чеслав", "Эдуард", "Юлий", "Ярослав", "Август", "Бронислав",
        ]

        self.female_names = [
            "Мария", "Анна", "Екатерина", "Ольга", "Наталья", "Елена", "Татьяна",
            "Анастасия", "Дарья", "Ксения", "Светлана", "Ирина", "Людмила", "София",
            "Виктория", "Алёна", "Кристина", "Евгения", "Полина", "Маргарита",
            "Надежда", "Тамара", "Галина", "Яна", "Зоя", "Элеонора", "Снежана", "Римма",
            "Варвара", "Кира", "Оксана", "Лариса", "Арина", "Мила", "Диана", "Алла",
            "Алина", "Лилия", "Алиса", "Марина", "Вероника", "Жанна", "Изабелла",
            "Карина", "Лидия", "Марта", "Нина", "Оксана", "Регина", "Сара", "Юлия",
            "Эльвира", "Ярослава", "Агата", "Белла", "Валентина", "Галина", "Дина",
            "Евдокия", "Жанна", "Зинаида", "Ия", "Клариса", "Люция", "Мирослава",
            "Нелли", "Ольга", "Пелагея", "Рада", "Серафима", "Таисия", "Фаина",
            "Христина", "Цветана", "Чулпан", "Эмма", "Юнона", "Ядвига", "Аврора",
            "Беата", "Венера", "Гертруда", "Джульетта", "Есения", "Жасмин", "Земфира",
            "Иветта", "Камилла", "Лариса", "Майя", "Наталия", "Одетта", "Патрисия",
            "Розалия", "Сильвия", "Тамара", "Ульяна", "Флора", "Харита", "Цезария",
        ]

        self.male_surnames = [
            "Смирнов", "Иванов", "Кузнецов", "Попов", "Соколов", "Лебедев", "Ковалев",
            "Петров", "Николаев", "Романов", "Федоров", "Алексеев", "Морозов", "Степанов",
            "Сидоров", "Козлов", "Тихонов", "Беляев", "Громов", "Яковлев", "Захаров",
            "Фролов", "Сергеев", "Шевченко", "Матвеев", "Давыдов", "Савельев", "Лукьянов",
            "Борисов", "Киселев", "Тимофеев", "Афанасьев", "Мартынов", "Сорокин", "Гусев",
            "Андреев", "Макаров", "Крылов", "Куликов", "Карпов", "Власов", "Маслов",
            "Исаков", "Туров", "Сафонов", "Панов", "Мишин", "Родин", "Ермаков", "Зуев",
            "Токарев", "Калинин", "Воронов", "Суханов", "Лапин", "Прохоров", "Нестеров",
            "Соболев", "Титов", "Миронов", "Мельников", "Буров", "Быков", "Зыков",
            "Агафонов", "Баринов", "Вольский", "Гаврилов", "Дроздов", "Евсеев", "Журавлев",
            "Зверев", "Капустин", "Лавров", "Минин", "Носов", "Овчинников", "Пахомов",
            "Рябов", "Стрелков", "Третьяков", "Успенский", "Фомин", "Харламов", "Цветков",
            "Чернышев", "Шаповалов", "Щербаков", "Эдуардов", "Юдин", "Яшин", "Абрамов",
            "Баженов", "Воронцов", "Горбачев", "Демьянов", "Ефимов", "Задорнов", "Игнатьев",
            "Кабанов", "Лизунов", "Михайлов", "Нестеров", "Орлов", "Павлов", "Рожков",
            "Семенов", "Тарасов", "Уваров", "Федосеев", "Худяков", "Царев", "Черкасов",
        ]

        self.female_surnames = [
            "Смирнова", "Иванова", "Кузнецова", "Попова", "Соколова", "Лебедева",
            "Ковалёва", "Петрова", "Николаева", "Романова", "Федорова", "Алексеева",
            "Морозова", "Степанова", "Сидорова", "Козлова", "Тихонова", "Беляева",
            "Громова", "Яковлева", "Захарова", "Фролова", "Александрова", "Григорьева",
            "Матвеева", "Давыдова", "Савельева", "Лукьянова", "Борисова", "Киселева",
            "Тимофеева", "Афанасьева", "Мартынова", "Сорокина", "Гусева", "Андреева",
            "Макарова", "Крылова", "Куликова", "Карпова", "Власова", "Маслова", "Исакова",
            "Турова", "Сафонова", "Панова", "Мишина", "Родина", "Ермакова", "Зуева",
            "Токарева", "Калинина", "Воронова", "Суханова", "Лапина", "Прохорова", "Нестерова",
            "Соболева", "Титова", "Миронова", "Мельникова", "Бурова", "Быкова", "Зыкова",
            "Агафонова", "Баринова", "Вольская", "Гаврилова", "Дроздова", "Евсеева", "Журавлева",
            "Зверева", "Капустина", "Лаврова", "Минина", "Носова", "Овчинникова", "Пахомова",
            "Рябова", "Стрелкова", "Третьякова", "Успенская", "Фомина", "Харламова", "Цветкова",
            "Чернышева", "Шаповалова", "Щербакова", "Эдуардова", "Юдина", "Яшина", "Абрамова",
            "Баженова", "Воронцова", "Горбачева", "Демьянова", "Ефимова", "Задорнова", "Игнатьева",
            "Кабанова", "Лизунова", "Михайлова", "Нестерова", "Орлова", "Павлова", "Рожкова",
            "Семенова", "Тарасова", "Уварова", "Федосеева", "Худякова", "Царева", "Черкасова",
        ]

        self.male_patronymics = [
            "Александрович", "Дмитриевич", "Иванович", "Максимович", "Артемович",
            "Сергеевич", "Юрьевич", "Романович", "Витальевич", "Денисович",
            "Никитич", "Станиславович", "Егорович", "Федорович", "Павлович",
            "Игоревич", "Петрович", "Григорьевич", "Давыдович", "Филиппович",
            "Анатольевич", "Борисович", "Вадимович", "Геннадиевич", "Евгеньевич",
            "Захарович", "Ильич", "Константинович", "Львович", "Михайлович",
            "Николаевич", "Олегович", "Павлович", "Робертович", "Семенович",
            "Тимофеевич", "Федорович", "Эдуардович", "Юрьевич", "Ярославович",
        ]

        self.female_patronymics = [
            "Александровна", "Дмитриевна", "Ивановна", "Максимовна", "Артемовна",
            "Сергеевна", "Юрьевна", "Романовна", "Витальевна", "Денисовна",
            "Никитична", "Станиславовна", "Егоровна", "Федоровна", "Павловна",
            "Игоревна", "Петровна", "Григорьевна", "Давыдовна", "Филипповна",
            "Анатольевна", "Борисовна", "Вадимовна", "Геннадиевна", "Евгеньевна",
            "Захаровна", "Ильинична", "Константиновна", "Львовна", "Михайловна",
            "Николаевна", "Олеговна", "Павловна", "Робертовна", "Семеновна",
            "Тимофеевна", "Федоровна", "Эдуардовна", "Юрьевна", "Ярославовна",
        ]

        self.cities = [
            "Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург",
            "Минск", "Алматы", "Ташкент", "Бишкек", "Астана", "Краснодар",
            "Саратов", "Тула", "Челябинск", "Воронеж", "Рязань", "Ижевск",
            "Омск", "Уфа", "Томск", "Калуга", "Сочи", "Симферополь", "Севастополь",
            "Киров", "Чебоксары", "Владивосток", "Тверь", "Орлов", "Липецк",
            "Брянск", "Гомель", "Гродно", "Могилев", "Витебск", "Брест",
            "Душанбе", "Тбилиси", "Ереван", "Баку", "Ашхабад",
            "Тирасполь", "Кишинев", "Цхинвал", "Сухуми", "Нальчик", "Махачкала",
            "Грозный", "Владикавказ", "Ставрополь", "Астрахань", "Калининград",
            "Кострома", "Иркутск", "Чита", "Улан-Удэ", "Благовещенск", "Хабаровск",
            "Якутск", "Тюмень", "Сургут", "Нижний Тагил", "Пермь", "Пенза",
            "Барнаул", "Волгоград", "Волжский", "Выкса", "Гатчина", "Дзержинск",
            "Ижевск", "Йошкар-Ола", "Калуга", "Кемерово", "Киров", "Кострома",
            "Курган", "Липецк", "Магнитогорск", "Мурманск", "Набережные Челны",
            "Нижневартовск", "Новороссийск", "Орск", "Петрозаводск", "Псков",
            "Рыбинск", "Саранск", "Серпухов", "Сыктывкар", "Таганрог", "Тамбов",
            "Улан-Удэ", "Ульяновск", "Химки", "Чебоксары", "Энгельс", "Южно-Сахалинск",
            "Ярославль"
        ]

    def generate_random_birthdate(self):
        start_date = datetime.now() - timedelta(days=60*365)  
        end_date = datetime.now() - timedelta(days=18*365)   
        return start_date + (end_date - start_date) * random.random()

    def calculate_age(self, birthdate):
        today = datetime.now()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
# идею функции и часть кода взял у t.me/hikka_mods
# из модуля https://github.com/C0dwiz/H.Modules/blob/main/AccountData.py#L36-L50
    async def get_creation_date(self, id: int) -> str:
        url = "https://restore-access.indream.app/regdate"
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
            "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
            "accept-language": "en-US,en;q=0.9",
        }
        data = {"telegramId": id}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["data"]["date"]
        else:
            return "Ошибка получения данных"

    async def doxcmd(self, message):
        "Пробить в базе"
        if self.is_doxing:
            await message.edit("<b>Доксинг уже выполняется. Пожалуйста, дождитесь завершения.</b>")
            return

        if not (message.is_reply or utils.get_args_raw(message)):
            await message.edit("<b>Ошибка: необходимо указать юзернейм, ссылку или ответить на сообщение.</b>")
            return

        self.is_doxing = True

        try:
            user = None

            if message.is_reply:
                replied_message = await message.get_reply_message()
                user = await message.client.get_entity(replied_message.from_id)
            else:
                args = utils.get_args_raw(message)
                if args:
                    try:
                        user = await message.client.get_entity(args.strip())
                    except Exception:
                        await message.edit("<b>Этот юзернейм никем не используется или не настоящий.</b>")
                        return

            if not user:
                await message.edit("<b>Не удалось получить информацию о пользователе. Пожалуйста, укажите корректные данные.</b>")
                return

            if isinstance(user, User) and user.bot:
                await message.edit(f"<b>Пользователь <a href='tg://user?id={user.id}'>{user.first_name}</a> является ботом, я могу доксить только людей.</b>")
                return
            elif isinstance(user, Channel):
                await message.edit(f"<b>Пользователь <a href='https://t.me/{user.username}'>{user.title}</a> является каналом, я могу доксить только людей.</b>")
                return

            if user.id == message.from_id:
                await message.edit("<b>Вы не можете доксить себя.</b>")
                return

            await message.edit("<b>Запуск доксинга...</b>")
            await asyncio.sleep(1)

            animation_type = self.config["animation_type"]

            if animation_type == "short":
                await self.short_loading(message)
            elif animation_type == "standart":
                await self.medium_loading(message)
            else:
                await self.long_loading(message)

            await self.display_results(message, user)

        finally:
            self.is_doxing = False

    async def short_loading(self, message):
        await asyncio.sleep(1)
        await message.edit("<b>Собираю данные...</b>")
        await asyncio.sleep(2)

    async def medium_loading(self, message):
        current_percent = 0
        while current_percent < 100:
            increment = random.randint(5, 25)
            current_percent = min(100, current_percent + increment)
            filled_blocks = current_percent // 10
            await message.edit(f"<b>Собираю данные...</b> [{'■' * filled_blocks}{'□' * (10 - filled_blocks)}] {current_percent}%")
            await asyncio.sleep(random.uniform(0.3, 0.7))

    async def long_loading(self, message):
        current_percent = 0
        while current_percent < 100:
            increment = random.randint(5, 15)
            current_percent = min(100, current_percent + increment)
            filled_blocks = current_percent // 10
            await message.edit(f"<b>Собираю данные...</b> [{'■' * filled_blocks}{'□' * (10 - filled_blocks)}] {current_percent}%")
            await asyncio.sleep(random.uniform(0.4, 0.9))

    async def display_results(self, message, user):
        user_first_name = user.first_name if user.first_name else ""

        is_male = user_first_name in self.male_names
        is_female = user_first_name in self.female_names

        if is_male:
            random_name = user_first_name
            random_surname = random.choice(self.male_surnames)
            random_patronymic = random.choice(self.male_patronymics)
        elif is_female:
            random_name = user_first_name
            random_surname = random.choice(self.female_surnames)
            random_patronymic = random.choice(self.female_patronymics)
        else:
            random_name = random.choice(self.male_names + self.female_names)
            if random_name in self.male_names:
                random_surname = random.choice(self.male_surnames)
                random_patronymic = random.choice(self.male_patronymics)
            else:
                random_surname = random.choice(self.female_surnames)
                random_patronymic = random.choice(self.female_patronymics)

        random_city = random.choice(self.cities)

        random_ip = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
        random_phone = f"+7 (999) {random.randint(100, 999)}-{random.randint(1000, 9999)}"#на данный момент не сезон грибов, по этому автору негде брать идеи для прозвищ
        funny_nickname = random.choice([
            "Душнила", "Сёмга", "Дед инсульт", "Спамщик", "Мегачорт", "Мошенник",
            "Бронированный вафельный стаканчик", "Чудо в перьях", "Агрессивный баклажан",
            "Магический пердёж", "Сморщенный кусочек не понятно чего", "Дед-скуфик",
            "Трисися", "Сиська потного индейца", "Тумбочка", "Капитан очевидность",
            "Грозный метр с кепкой", "Диктатор", "Солевой магнат", "Дилер",
            "Очередной Гений", "Пенсионер"
        ])

        user_rating = random.randint(1, 10)

        birthdate = self.generate_random_birthdate()
        age = self.calculate_age(birthdate)

        creation_date_str = await self.get_creation_date(user.id)
        if "Ошибка" not in creation_date_str:
            if len(creation_date_str) == 7: 
                creation_date_str += '-01' 
            creation_date = datetime.strptime(creation_date_str, "%Y-%m-%d")
            account_age = self.calculate_age(creation_date)
        else:
            account_age = "Не удалось получить данные"

        all_info = [
            (f"<b>🪪ФИО:</b> <code>{random_surname} {random_name} {random_patronymic}</code>", "Основная информация:"),
            (f"<b>🌆Город:</b> <code>{random_city}</code>", ""),
            (f"<b>📢IP-адрес:</b> <code>{random_ip}</code>", ""),
            (f"<b>📱Телефон:</b> <code>{random_phone}</code>\n", ""),
            (f"<b>⏳Возраст:</b> <code>{age} лет</code>", "Дополнительная информация:"),
            (f"<b>🗓️Дата рождения:</b> <code>{birthdate.strftime('%d.%m.%Y')}</code>", ""),
            (f"<b>⏳Возраст аккаунта:</b> <code>{account_age} лет</code>\n", ""),
            (f"<b>📒Прозвище:</b> <code>{funny_nickname}</code>", "Прочая информация:"),
            (f"<b>ℹ️ID:</b> <code>{user.id}</code>", ""),
            (f"<b>ℹ️Юзернейм:</b> {f'@{user.username}' if user.username else 'не указан'}", ""),
            (f"<b>Рейтинг:</b> <code>{user_rating}/10</code>", "")
        ]

        
        
        
        display_text = f"<b>Вот всё, что я нашел про {user.first_name}:</b>\n\n"

        if self.config["InfoAnimation"]:
            for info, section in all_info:
                if section:
                    display_text += f"<b>{section}</b>\n"
                display_text += info + "\n"
                await message.edit(display_text)
                await asyncio.sleep(0.5)
        else:
            for info, section in all_info:
                if section:
                    display_text += f"<b>{section}</b>\n"
                display_text += info + "\n"
            await message.edit(display_text)