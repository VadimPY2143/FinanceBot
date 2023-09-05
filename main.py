# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import random as r
import requests
from bs4 import BeautifulSoup as bs
from const import TOKEN
import lxml
import logging
from dotenv import load_dotenv


invest_advices = ['<b>Витрачайте менше, ніж заробляєте</b>\nНе потрібно зменшувати витрати до мінімуму, але розумні витрати призведуть до чудових результатів.\nВажливо купувати лише те, що справді необхідне, та ігнорувати скороминущі забаганки купити щось непотрібне.\nДуже важливо проаналізувати свої витрати та зменшити їх.\nЧасто чимало грошей щомісяця йде на речі, що можуть виявитися зовсім непотрібними',
                  "<b>Заощаджуйте незалежно від рівня доходу</b>\nІдеальний момент, щоб почати заощаджувати гроші, – тут і зараз.\nЦе можна робити, навіть отримуючи мінімальну чи середню зарплату, – все залежить від кількості коштів, що виділяються як накопичення.\nНеобов'язково прив'язуватися до певної суми, важливо, щоб це стало звичкою.\nА якщо ви знайдете додаткове джерело доходу, наприклад опануєте трейдинг, зекономлені кошти можна потрактувати як накопичення.",
                  "<b>Мінімізуйте борги</b>\nМаючи борги, важливо організувати їх погашення за пріоритетами.\nСлід також уникати боргів, що передбачають виплату відсотків.\nЯкщо є можливість, не беріть у борг, а якщо це вже сталося, зробіть усе можливе, щоб якнайшвидше його погасити.",
                  "<b>Контролюйте свої доходи та витрати</b>\nЩе одна корисна порада для тих, хто хоче бути фінансово грамотним.\nЛюди, що мають цю навичку, рекомендують використовувати спеціальні програми (на смартфоні або комп'ютері) із ведення домашньої бухгалтерії.\nЦе спростить контроль за особистими фінансами і дасть розуміння, яке у вас співвідношення доходів/витрат і на що йдуть гроші.\nВажливо записувати абсолютно всі надходження грошей та витрати: і фіксовані, і випадкові.\nЩомісяця аналізуйте, де можна було скоротити витрати та заощадити.",
                  "<b>Фінансова подушка повинна бути в кожного</b>\nКоли ми маємо заощадження, ми відчуваємо себе більш впевненими, стикаючись зі складними ситуаціями в житті.\nВажливо щомісяця відкладати частину прибутку для створення фінансової подушки.\nРозмір щомісячних заощаджень залежить від заробітку, цілей, часу та суми, яку необхідно зібрати.\nФінансова подушка розміром 3 - 6 заробітних плат вже дає можливість не боятись звільнення з роботи.\nНадалі заощаджені гроші можна вигідно інвестувати, щоб отримувати пасивний дохід.",
                  '<b>Купуючи речі в кредит, ми змушені більше працювати</b>\nКрім того, людина з боргами завжди знаходиться в зоні ризику, тому що неможливо передбачити майбутнє.\nНеприємно опинитись в ситуації, коли половина заробленого декілька років підряд витрачається на відсотки за кредитом.\nЗавжди слід порівнювати переваги та недоліки, перш ніж зважитись позичити гроші під відсотки. Крім того, необхідно порівнювати різні кредити, щоб не переплачувати зайвого.',
                  '<b>Корисного має бути більше, ніж приємного</b>\nРечі, які приносять нам прибуток — це наші активи, й навпаки, пасиви — це все, що потребує витрат. Автомобіль для таксиста — це його актив, тому що користуючись ним він заробляє гроші.\nАле якщо авто буде споживати занадто багато пального, витрати перевищать доходи, й він перетвориться в пасив.\nБудинок, який здається в оренду — це актив. Якщо витрати на його утримання перевищують вигоду від володіння, тоді він перетворюється на пасив. Так, ми можемо володіти пасивами — власним будинком, автомобілем, мотоциклом та іншими приємними речами. Але спочатку потрібно придбати активи, доходи від яких дозволять все це придбати й головне — утримувати.']


salary = 0
user_waste = {}


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

START = '<b>Вітаю вас у FinanceBot!</b>\nДаний бот був створений для того, щоб кожна людина могла контролювати свої фінанси та стала трошки досвідченнішою у цій сфері.'

HELP = 'Чим я можу бути корисним для вас?🧐'


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

button1 = KeyboardButton(text='💰Курс валют')
button2 = KeyboardButton(text='💵Розподілення бюджету')
button3 = KeyboardButton(text='💸Фінансова порада')


kb_client.add(button1,button2,button3)


inline_menu1 = InlineKeyboardMarkup(row_width=2)
btn_mney = InlineKeyboardMarkup(text='USD', callback_data = 'btn_mney')
btn_mney2 = InlineKeyboardMarkup(text='EUR', callback_data = 'btn_mney2')
btn_mney3 = InlineKeyboardMarkup(text='BTC', callback_data = 'btn_mney3')


inline_menu2 = InlineKeyboardMarkup(row_width=2)
week_money = InlineKeyboardMarkup(text='Бюджет на тиждень', callback_data = 'week_money')
daily_money= InlineKeyboardMarkup(text='Бюджет на день', callback_data = 'daily_money')
change_money = InlineKeyboardMarkup(text='Корректувати бюджет', callback_data = 'chng_mney')
analyze_waste = InlineKeyboardMarkup(text='Додати витрату', callback_data = 'anlz_wst')


inline_menu3 = InlineKeyboardMarkup(row_width=1)
check_statistic = InlineKeyboardMarkup(text='Звіт за місяць', callback_data = 'check_stat')

inline_menu1.insert(btn_mney)
inline_menu1.insert(btn_mney2)
inline_menu1.insert(btn_mney3)

inline_menu2.insert(week_money)
inline_menu2.insert(daily_money)
inline_menu2.insert(change_money)
inline_menu2.insert(analyze_waste)

inline_menu3.insert(check_statistic)

request = requests.get('https://ua.sinoptik.ua//погода-львів')
html = bs(request.content, 'html.parser')

for i in html.select('#content'):
    day = i.select('.day-link')[0].text
    date = i.select('.date')[0].text
    month = i.select('.month')[0].text

request_USD = requests.get('https://www.currency.me.uk/convert/usd/uah')
soup = bs(request_USD.text, 'lxml')
curs_USD = soup.find("span", {'class' : 'mini ccyrate'}).text
curs_USD2 = ''
for h in curs_USD:
    if h.isdigit():
        curs_USD2+=h
curs_USD3 = curs_USD2[1:3]


request_EUR = requests.get('https://www.currency.me.uk/convert/eur/uah')
soup2 = bs(request_EUR.text, 'lxml')
curs_EUR = soup2.find("span", {'class':'mini ccyrate'}).text


request_BTC = requests.get('https://minfin.com.ua/ua/currency/crypto/bitcoin-uah/')
soup3 = bs(request_BTC.text, 'lxml')
curs_BTC = soup3.find('div', {'class': 'sc-18a2k5w-7 jLhBcj'}).text
curs_BTC2 = ''
for y in curs_BTC:
    if y == '.':
        break
    if y.isdigit():
        curs_BTC2+=y


@dp.message_handler(text=['💰Курс валют'])
async def money(message: types.Message):
    await message.answer('Яку валюту ви хочете переглянути?', reply_markup=inline_menu1)


@dp.callback_query_handler(text='btn_mney')
async def USD_print(message: types.Message):
    await bot.send_message(message.from_user.id,f'Курс доллара на {date} {month} ({day}): {curs_USD}')


@dp.callback_query_handler(text='btn_mney2')
async def EURO_print(message: types.Message):
    await bot.send_message(message.from_user.id, f'Курс євро на {date} {month} ({day}): {curs_EUR}')


@dp.callback_query_handler(text='btn_mney3')
async def USD_print(message: types.Message):
    await bot.send_message(message.from_user.id,f'Курс біткоїна на {date} {month} ({day}): 1 BTC = {curs_BTC2}$\n({int(curs_USD3) * int(curs_BTC2)} грн)')


@dp.message_handler(text=['💵Розподілення бюджету'])
async def get_user_salary(message: types.Message):
    await bot.send_message(message.from_user.id,'Введіть ваш бюджет на місяць (число у гривнях)')
    @dp.message_handler(lambda message: True)
    async def get_user_salary2(message: types.Message):
        global salary
        try:
            if salary == 0:
                salary+=int(message.text)
                await bot.send_message(message.from_user.id, f'Ваша сума на місяць: {salary}грн\nОберіть наступну дію', reply_markup=inline_menu2)
        except:
            await bot.send_message(message.from_user.id, 'Ви ввели неправильну інформацію!')


@dp.callback_query_handler(text='week_money')
async def check_week_money(message: types.Message):
    await bot.send_message(message.from_user.id, f'Ваш бюджет на тиждень: {salary//4}грн')


@dp.callback_query_handler(text='daily_money')
async def check_week_money(message: types.Message):
    await bot.send_message(message.from_user.id, f'Ваш бюджет на день {salary//30}грн')


@dp.callback_query_handler(text='chng_mney')
async def check_week_money(message: types.Message):
    global salary
    await bot.send_message(message.from_user.id, 'Введіть нову суму')
    salary = 0
    user_waste.clear()
    @dp.message_handler(lambda message: True)
    async def get_user_salary2(message: types.Message):
        global salary
        try:
            if len(message.text.split()) == 1:
                salary += int(message.text)
                await bot.send_message(message.from_user.id, f'Ваша сума - {salary}грн', reply_markup=inline_menu2)
                print(salary)
        except:
            await bot.send_message(message.from_user.id, 'Ви ввели неправильну інформацію!')


@dp.callback_query_handler(text='check_stat')
async def view_stats(message: types.Message):
    global user_waste
    result = ''
    for key,item in user_waste.items():
        result+=key+' '
        result+=item
        result+='\n'
    await bot.send_message(message.from_user.id, result)


@dp.callback_query_handler(text='anlz_wst')
async def analyze_user_waste(message: types.Message, state: FSMContext):
    global user_waste
    await bot.send_message(message.from_user.id, 'Введіть категорію, а через пробіл суму витрати')
    await state.set_state('get_user_info_state')


@dp.message_handler(state = 'get_user_info_state')
async def analyze_money(message: types.Message, state: FSMContext):
    global user_waste
    global salary

    try:
        user_message = message.text.split(' ')
        if salary - int(user_message[1]) >=0:
            if len(user_message) == 2:
                user_waste[user_message[0]] = user_message[1]
                salary-=int(user_message[1])
                await bot.send_message(message.from_user.id, 'Ваші данні додані в базу', reply_markup=inline_menu3)
                await bot.send_message(message.from_user.id, f'Ваша сума на місяць {salary}грн', reply_markup=inline_menu2)
                await state.finish()
        else:
            await bot.send_message(message.from_user.id, 'У вас недостатньо грошей!')

    except:
        await bot.send_message(message.from_user.id, 'Ви ввели неправильну інформацію!')


@dp.message_handler(text = ['💸Фінансова порада'])
async def cmd_help(message: types.Message):
    try:
        rand_advice = r.choice(invest_advices)
        await message.answer(rand_advice, parse_mode='html')
        invest_advices.remove(rand_advice)
    except IndexError:
        await message.answer('Поради закінчились😢')


@dp.message_handler(commands=['start','help'])
async def cmd_start(message: types.Message):
    await message.answer_photo('https://img.freepik.com/free-vector/finance-and-financial-performance-concept-illustration_53876-40450.jpg?w=996&t=st=1693661780~exp=1693662380~hmac=7d01bb43d0bf5652585dd0026df2a7a2fc994e6122266972df8ed15b967ef515')
    await message.answer(START, reply_markup=kb_client, parse_mode='html')

print('Запущено')

async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустити бота'),
            types.BotCommand('help', '/help')

        ]
    )

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_default_commands)