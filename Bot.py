from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

import psycopg2
import re

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot('6531330855:AAF_i8JDeYPOH2OYQxjTGGXfqyPmbPrGT2I')
dp = Dispatcher(bot, storage=MemoryStorage())

connection = psycopg2.connect(database="UserData", user="postgres", password="123", host="Localhost", port=5432)











@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if islogin(message.chat.id) == True:
        markup = types.ReplyKeyboardMarkup()
        but1 = types.KeyboardButton("Создать накладную")
        but2 = types.KeyboardButton("Отследить заказ")
        but3 = types.KeyboardButton("У меня претензия")
        but4 = types.KeyboardButton("Перевод на менеджера")
        markup.add(but1, but2, but3, but4)
        await message.answer('Вы авторизованы', reply_markup=markup)
    else:
        await message.answer(f'Давайте авторизуемся, введите ваш номер договора:')
        await reg.login.set()

class reg(StatesGroup):
    login = State()
    password = State()

@dp.message_handler(state=reg.login)
async def get_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)

    await message.answer('Введите пароль:')
    await reg.password.set()
@dp.message_handler(state=reg.password)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    login = str(data.get('login'))
    password = str(data.get('password'))
    await message.answer(f'Ваши данные {login} {password}')
    await state.finish()
    cursor = connection.cursor()
    cursor.execute("SELECT ContractID from users;")
    record1 = str(cursor.fetchall())
    cursor.execute("SELECT Password from users;")
    record2 = str(cursor.fetchall())
    cursor.close()
    id_user = int(message.chat.id)
    pass1 = str(re.findall("'([^']*)'", record1))
    pass2 = re.findall("'([^']*)'", record2)
    try:
        pass1.index(login)
        pass2.index(password)
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET telegramID = '{id_user}' WHERE ContractID = '{login}';")
        connection.commit()
        cursor.close()
        markup = types.ReplyKeyboardMarkup()
        but1 = types.KeyboardButton("Создать накладную")
        but2 = types.KeyboardButton("Отследить заказ")
        but3 = types.KeyboardButton("У меня претензия")
        but4 = types.KeyboardButton("Перевод на менеджера")
        markup.add(but1, but2, but3, but4)
        await message.answer('успешно', reply_markup=markup)
    except:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT login from admin;")
            record1 = str(cursor.fetchall())
            cursor.execute("SELECT Password from admin;")
            record2 = str(cursor.fetchall())
            cursor.close()
            id_user = int(message.chat.id)
            pass1 = str(re.findall("'([^']*)'", record1))
            pass2 = re.findall("'([^']*)'", record2)
            pass1.index(login)
            pass2.index(password)
            cursor = connection.cursor()
            cursor.execute(f"UPDATE admin SET telegramID = '{id_user}' WHERE login = '{login}';")
            connection.commit()
            cursor.close()
            await message.answer('успешно')
        except:
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton("Авторизоваться"))
            await message.answer('ошибка попробуйте ещё раз', reply_markup=markup)
            cursor.close()
class zap(StatesGroup):
    close = State()

class rep(StatesGroup):
    pri = State()
    invoice_id = State()
    report = State()

@dp.message_handler(content_types=['text'])
async def text_message(message: types.Message):
    if message.text == 'Отследить заказ':
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT contractID From users WHERE telegramID = '{message.chat.id}';")
            login = cursor.fetchall()
            login = login[0]
            cursor.execute(f"SELECT * FROM tracking WHERE contractID = '{login[0]}';")
            track = cursor.fetchall()
            if track == []:
                await message.answer('Отсутсвуют активные заказы')
            else:
                cursor.close()
                for i in range(len(track)):
                    mes=track[i]
                    await message.answer(f'Номер акладную: {mes[0]} \n Статус: {mes[1]} \n Дата получения: {mes[2]}')
        except:
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton("Авторизоваться"))
            await message.answer('Вы не вошли в учётную запись', reply_markup=markup)
    elif message.text == 'У меня претензия':
        if islogin(message.chat.id) == True:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            but1 = types.KeyboardButton("Нарушение сроков доставки")
            but2 = types.KeyboardButton("Порча вложения")
            but3 = types.KeyboardButton("Утеря вложения")
            but4 = types.KeyboardButton("Повреждение упаковки")
            but5 = types.KeyboardButton("Отмена")
            markup.add(but1, but2, but3, but4, but5)
            await message.answer('Выберите причину обращения', reply_markup=markup)
            await rep.pri.set()
        else:
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton("Авторизоваться"))
            await message.answer('Вы не вошли в учётную запись', reply_markup=markup)
    elif message.text == 'Создать накладную':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Дверь-Дверь")
        btn2 = types.KeyboardButton("Склад-Склад")
        btn3 = types.KeyboardButton("Склад-Дверь")
        btn4 = types.KeyboardButton("Дверь-Склад")
        markup.add(btn1, btn2, btn3, btn4)
        await message.answer('Давай приступим к созданию анкеты отправки.Выберите режим отправки.', reply_markup=markup)
        await invoice.sending.set()
    elif message.text == 'Проверка':
        await message.answer(islogin(message.chat.id))
    elif message.text == 'Перевод на менеджера':
        if islogin(message.chat.id) == True:
            await message.answer('Перевод на менеджера')
            await zap.close.set()
        else:
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton("Авторизоваться"))
            await message.answer('Вы не вошли в учётную запись', reply_markup=markup)
    elif verification(message.chat.id) == True:
        mess = message.text
        ob = mess.split(':')
        await bot.send_message(ob[0], ob[1])


@dp.message_handler(state=rep.pri)
async def help(message: types.Message, state: FSMContext):
    await state.update_data(pri=message.text)
    if message.text != 'Отмена':
        if islogin(message.chat.id) == True:
            if message.text == 'Нарушение сроков доставки' or message.text == 'Порча вложения' or message.text == 'Утеря вложения' or message.text == 'Повреждение упаковки':
                await message.answer('Введите номер накладной')
                await rep.invoice_id.set()
        else:
            await state.finish()
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton("Авторизоваться"))
            await message.answer('Вы не вошли в учётную запись', reply_markup=markup)
    else:
        await state.finish()


@dp.message_handler(state=rep.invoice_id)
async def help(message: types.Message, state: FSMContext):
    await state.update_data(invoice_id=message.text)
    if message.text != 'Отмена':
        await message.answer('Расскажите что случилось')
        await rep.report.set()
    else:
        await state.finish()


@dp.message_handler(state=rep.report)
async def help(message: types.Message, state: FSMContext):
    await state.update_data(report=message.text)
    if message.text != 'Отмена':
        try:
            data = await state.get_data()
            typeofrequest = str(data.get('pri'))
            invoice_number = str(data.get('invoice_id'))
            report = str(data.get('report'))
            cursor = connection.cursor()
            cursor.execute(f"SELECT contractID From users WHERE telegramID = '{message.chat.id}';")
            login = cursor.fetchall()
            login = login[0]
            await message.answer(f"('{login[0]}', {invoice_number}, '{report}', '{typeofrequest}')")
            cursor.execute(f"Insert into report (ContractID, InvoiceID, Report, TypeOfRequest) VALUES ('{login[0]}', {invoice_number}, '{report}', '{typeofrequest}');")
            connection.commit()
            cursor.close()
            await message.answer('Мы передали ваш запрос, скоро вам ответят')
        except:
            await state.finish()
            await message.answer('Ошибка, проверьте вошли ли вы в аккаунт и правильно ли введён номер номинклатуры')
    await state.finish()

def verification(id):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT login From admin WHERE telegramID = '{id}';")
        record = cursor.fetchall()
        record = record[0]
        record = list(record[0])
        cursor.close()
        return True
    except:
        return False
def islogin(id):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT contractID From users WHERE telegramID = '{id}';")
        record = cursor.fetchall()
        record = record[0]
        record = list(record[0])
        cursor.close()
        return True
    except:
        return False
@dp.message_handler(state=zap.close)
async def help(message: types.Message, state: FSMContext):
    await state.update_data(zap=message.text)
    if message.text != '/close':
        cursor = connection.cursor()
        cursor.execute(f"SELECT adminID From users WHERE telegramID = '{message.chat.id}';")
        id_admin = cursor.fetchall()
        id_admin = id_admin[0]
        cursor.execute(f"SELECT telegramID From admin WHERE adminID = {id_admin[0]};")
        id_admin = cursor.fetchall()
        id_admin = id_admin[0]
        cursor.close()
        await bot.send_message(id_admin[0], f'ID: {message.chat.id}, {message.text}')
    else:
        await state.finish()

class invoice(StatesGroup):
    sending = State()
    number_of_seats = State()
    description = State()
    dimensions = State()
    weight = State()
    price = State()
    address1 = State()
    address2 = State()
    payment_method = State()

@dp.message_handler(state=invoice.sending)
async def get_sending(message: types.Message, state: FSMContext):

    if message.text == 'Дверь-Дверь':
        await state.update_data(sending=message.text)
        await message.answer('Введите количество мест', reply_markup=types.ReplyKeyboardRemove())
        await invoice.number_of_seats.set()
    elif message.text == 'Склад-Склад':
        await state.update_data(sending=message.text)
        await message.answer('Введите количество мест', reply_markup=types.ReplyKeyboardRemove())
        await invoice.number_of_seats.set()
    elif message.text == 'Склад-Дверь':
        await state.update_data(sending=message.text)
        await message.answer('Введите количество мест', reply_markup=types.ReplyKeyboardRemove())
        await invoice.number_of_seats.set()
    elif message.text == 'Дверь-Склад':
        await state.update_data(sending=message.text)
        await message.answer('Введите количество мест', reply_markup=types.ReplyKeyboardRemove())
        await invoice.number_of_seats.set()
    else:
        await message.answer('Неверное значение попробуйте ещё раз')

@dp.message_handler(state=invoice.number_of_seats)
async def get_number_of_seats(message: types.Message, state: FSMContext):
    await state.update_data(number_of_seats=message.text)
    mes = message.text
    a = True
    try:
        int(mes)
    except:
        a = False
    if a == False:
        await message.answer('Неправильно заполнена форма')
    else:
        await message.answer('Опишите свои вложения одним сообщением')
        await invoice.description.set()

@dp.message_handler(state=invoice.description)
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Напишите габариты каждого места в см через запятую в таком формате: Длина-Ширина-Высота\n'
                        'Пример: 10-10-10, 20-20-20')
    await invoice.dimensions.set()


@dp.message_handler(state=invoice.dimensions)
async def get_dimensions(message: types.Message, state: FSMContext):
    await state.update_data(dimensions=message.text)
    mes = message.text
    ob = mes.split(', ')
    a = True
    for i in ob:
        ob1 = i.split('-')
        for i in ob1:
            try:
                int(i)
            except:
                a = False
    if a == False:
        await message.answer('Неправильно заполнена форма')
    else:
        await message.answer('Напишите вес каждого места в кг через запятую \n Пример 44.2, 33')
        await invoice.weight.set()


@dp.message_handler(state=invoice.weight)
async def get_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    mes = message.text
    ob = mes.split(', ')
    a = True
    try:
        for i in ob:
            float(i)
    except:
            a = False
    if a == False:
        await message.answer('Неправильно заполнена форма')

    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn1 = types.KeyboardButton("Общая")
        btn2 = types.KeyboardButton("По местам")
        markup.add(btn1, btn2)
        await message.answer('Выберите стоимость вложения', reply_markup=markup)
        await invoice.price.set()

@dp.message_handler(state=invoice.price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    sending = str(data.get('sending'))
    if sending == 'Дверь-Дверь' or sending == 'Дверь-Склад':
        await message.answer('Введите адресс где забрать посылку')
        await invoice.address1.set()
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * From pickuppoint;")
        recep = cursor.fetchall()
        cursor.close()
        await message.answer(f'Выберите адресс где забрать посылку {recep}')
        await invoice.address1.set()

@dp.message_handler(state=invoice.address1)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address1=message.text)
    data = await state.get_data()
    sending = str(data.get('sending'))
    if sending != 'Склад-Склад' or sending == 'Дверь-Склад':
        await message.answer('Введите адресс куда отправить посылку')
        await invoice.address2.set()
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * From pickuppoint;")
        recep = cursor.fetchall()
        cursor.close()
        await message.answer(f'Выберите адресс куда отправить посылку {recep}')
        await invoice.address2.set()

@dp.message_handler(state=invoice.address2)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address2=message.text)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton("Оплата получателем")
    btn2 = types.KeyboardButton("Отправляем по договору")
    markup.add(btn1, btn2)
    await message.answer('Выберите способ оплаты', reply_markup=markup)
    if message.text == 'Оплата получателем' or message.text == 'Отправляем по договору':
        await state.update_data(price=message.text)
        await invoice.payment_method.set()
@dp.message_handler(state=invoice.payment_method)
async def get_payment_method(message: types.Message, state: FSMContext):
    await state.update_data(payment_method=message.text)
    await state.finish()
    data = await state.get_data()
    sending = str(data.get('sending'))
    number_of_seats = str(data.get('number_of_seats'))
    description = str(data.get('description'))
    dimensions = str(data.get('dimensions'))
    weight = str(data.get('weight'))
    price = str(data.get('price'))
    payment_method = str(data.get('payment_method'))
    adress1 = str(data.get('address1'))
    adress2 =str(data.get('address2'))
    cursor = connection.cursor()
    cursor.execute(f"SELECT contractID From users WHERE telegramID = '{message.chat.id}';")
    login = cursor.fetchall()
    login = login[0]
    cursor = connection.cursor()
    cursor.execute("SELECT invoiceid From invoice;")
    recep = cursor.fetchall()
    recep.reverse()
    recep = recep[0]
    recep = recep[0]
    recep += 1
    cursor.execute(f"Insert into invoice (invoiceid, typeofsend, placenum, diladress, sendadress, paytype, contractid, size, weight, description, cost) VALUES ({recep}, '{sending}', {number_of_seats}, '{adress1}', '{adress2}','{payment_method}', '{login[0]}', '{dimensions}', '{weight}', '{description}', '{price}');")
    cursor.close()
    await message.answer(f'Ваши данные {sending} {number_of_seats} {description} {dimensions} {weight} {price} {payment_method}', reply_markup=types.ReplyKeyboardRemove())

executor.start_polling(dp)