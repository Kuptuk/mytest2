import telebot
import pymongo
from telebot import types
import os
import datetime

mm = os.environ.get("Mongo")
tt = os.environ.get("TOKEN")
my_client = pymongo.MongoClient(mm)
bot = telebot.TeleBot(tt)

my_database = my_client.dz
my_collection = my_database.dz

my_database2 = my_client.rasp
my_collection2 = my_database2.rasp

my_collection3 = my_database2.stat

prev = [522487188, 408011007, 761305732, 682106182, 740708453, 482625846, 577722848, 712460966, 384499877, 522789808, 793950542, 700577024, 718854606, 486139314, 518005930, 750174290, 340333734, 836792540]

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "/dz - узнать дз\n/rasp - показать расписание\n/stat - статистика\n/bug текст - сообщить о баге (сюда можно и кидать идеи)")
    bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)

@bot.message_handler(commands=["newdz"])
def newdz_message(message):
    try:
        if message.from_user.id == 522487188:
            a = message.text.split()
            dnd = a[1]
            date = a[2]
            text = " ".join(a[3:])
            my_cursor = my_collection.find()
            for item in my_cursor:
                if item["date"] == dnd + " " + date:
                    my_collection.update_one({"text":item["text"]},{"$set":{"text":item["text"]+"\n"+"• " + text + "\n"}})
                    bot.send_message(message.chat.id, "Дз обновлено")
                    break
            else:
                my_collection.insert_one({"date": dnd + " " + date, "text": "• " + text + "\n"})
                bot.send_message(message.chat.id, "Дз создано")
        else:
            bot.send_message(message.chat.id, "У вас нет прав.")
    except:
        bot.send_message(message.chat.id,"Возникла ошибка!")

@bot.message_handler(commands=["dz"])
def url(message):
    global prev
    if message.from_user.id in prev:
        my_cursor = my_collection.find()
        markup = types.InlineKeyboardMarkup()
        a = dict()
        for item in my_cursor:
            a.update({item["date"]:item["text"]})
        d1 = dict(sorted(a.items(), key = lambda x:x[0]))
        for key in d1.keys():
            btn_my_site=types.InlineKeyboardButton(text=str(key),callback_data=key)
            markup.add(btn_my_site)
        try:
            bot.send_message(message.from_user.id, "Выберите дату\nТекущая дата: " + datetime.datetime.now().strftime('%Y-%m-%d'), reply_markup = markup)
        except:
            bot.send_message(message.chat.id, message.from_user.first_name + ", напишите мне в личку /start и я смогу отправлять вам сообщения!")
        bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)
    else:
        bot.send_message(message.from_user.id, "Нет прав. Для получения обращайтесь к создателю.")
        bot.send_message(-326941525, message.from_user.first_name + ": " + "Пытался узнать дз")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global prev
    if call.from_user.id in prev:
        my_cursor = my_collection.find()
        for item in my_cursor:
            if call.message:
                if call.data == item["date"]:
                    try:
                        bot.send_message(call.from_user.id, item["date"] + "\n\n" + item["text"])
                        my_cursor2 = my_collection3.find()
                        for item2 in my_cursor2:
                            if item2["id"] == str(call.from_user.id):
                                if "Понедельник" in item["date"]:
                                    my_collection3.update_one({"id":str(call.from_user.id)},{"$set":{"Понедельник: ": item2["Понедельник: "] + 1}})
                                elif "Вторник" in item["date"]:
                                    my_collection3.update_one({"id":str(call.from_user.id)},{"$set":{"Вторник: ": item2["Вторник: "] + 1}})
                                elif "Среда" in item["date"]:
                                    my_collection3.update_one({"id":str(call.from_user.id)},{"$set":{"Среда: ": item2["Среда: "] + 1}})
                                elif "Четверг" in item["date"]:
                                    my_collection3.update_one({"id":str(call.from_user.id)},{"$set":{"Четверг: ": item2["Четверг: "] + 1}})
                                elif "Пятница" in item["date"]:
                                    my_collection3.update_one({"id":str(call.from_user.id)},{"$set":{"Пятница: ": item2["Пятница: "] + 1}})
                                break
                        else:
                            if "Понедельник" in item["date"]:
                                my_collection3.insert_one({"id": str(call.from_user.id), "Понедельник: ": 1, "Вторник: ": 0, "Среда: ": 0, "Четверг: ": 0, "Пятница: ": 0})
                            elif "Вторник" in item["date"]:
                                my_collection3.insert_one({"id": str(call.from_user.id), "Понедельник: ": 0, "Вторник: ": 1, "Среда: ": 0, "Четверг: ": 0, "Пятница: ": 0})
                            elif "Среда" in item["date"]:
                                my_collection3.insert_one({"id": str(call.from_user.id), "Понедельник: ": 0, "Вторник: ": 0, "Среда: ": 1, "Четверг: ": 0, "Пятница: ": 0})
                            elif "Четверг" in item["date"]:
                                my_collection3.insert_one({"id": str(call.from_user.id), "Понедельник: ": 0, "Вторник: ": 0, "Среда: ": 0, "Четверг: ": 1, "Пятница: ": 0})
                            elif "Пятница" in item["date"]:
                                my_collection3.insert_one({"id": str(call.from_user.id), "Понедельник: ": 0, "Вторник: ": 0, "Среда: ": 0, "Четверг: ": 0, "Пятница: ": 1})
                    except:
                        bot.send_message(call.message.chat.id, call.from_user.first_name + ", напишите мне в личку /start и я смогу отправлять вам сообщения!")
        my_cursor = my_collection2.find()
        for item in my_cursor:
            if call.message:
                if call.data == item["idch"]:
                    try:
                        bot.send_message(call.from_user.id, "• " + item["ch"] + "\n\n" + item["rasp"])
                    except:
                        bot.send_message(call.message.chat.id, call.from_user.first_name + ", напишите мне в личку /start и я смогу отправлять вам сообщения!")
        bot.send_message(-326941525, call.from_user.first_name + ": " + call.data)
    else:
        bot.send_message(call.from_user.id, "Нет прав. Для получения обращайтесь к создателю.")
        bot.send_message(-326941525, call.from_user.first_name + ": " + "Пытался узнать дз на определённую дату")

@bot.message_handler(commands=["deletedz"])
def deletedz_message(message):
    try:
        if message.from_user.id == 522487188:
            a = message.text.split()
            my_cursor = my_collection.find()
            for item in my_cursor:
                if item["date"] == a[1] + " " + a[2]:
                    my_collection.delete_one({"date":item["date"]})
                    bot.send_message(message.chat.id, "Дз на дату " + a[2] + " удалено")
                    break
            else:
                bot.send_message(message.chat.id, "Такой даты нет")
        else:
            bot.send_message(message.chat.id, "У вас нет прав.")
    except:
        bot.send_message(message.chat.id, "Возникла ошибка!")

@bot.message_handler(commands=["stat"])
def stat_message(message):
    try:
        my_cursor2 = my_collection3.find()
        for item in my_cursor2:
            if item["id"] == str(message.from_user.id):
                bot.send_message(message.from_user.id, "Понедельник: " + str(item["Понедельник: "]) + "\n" + "Вторник: " + str(item["Вторник: "]) + "\n" + "Среда: " + str(item["Среда: "]) + "\n" + "Четверг: " + str(item["Четверг: "]) + "\n" + "Пятница: " + str(item["Пятница: "]))
                break
        else:
            my_collection3.insert_one({"id": str(message.from_user.id), "Понедельник: ": 0, "Вторник: ": 0, "Среда: ": 0, "Четверг: ": 0, "Пятница: ": 0})
            bot.send_message(message.from_user.id, "Понедельник: 0\nВторник: 0\nСреда: 0\nЧетверг: 0\nПятница: 0")
    except:
        bot.send_message(message.chat.id, "Напишите мне в личку /start. После этого я смогу вам отправлять сообщения")
    bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)

@bot.message_handler(commands=["bug"])
def bug_message(message):
    try:
        bot.send_message(-326941525, message.from_user.first_name + ": " + " ".join(message.text.split()[1:]))
        bot.send_message(message.chat.id, "Успешно отправлено, спасибо!")
    except:
        bot.send_message(message.chat.id, "Ошибка")

@bot.message_handler(commands=["send"])
def send1_message(message):
    if message.from_user.id == 522487188:
        bot.send_message(761305732, message.text[6::])

@bot.message_handler(commands=["sendkl"])
def send1_message(message):
    if message.text[8::] != "":
        if message.from_user.id == 522487188:
            bot.send_message(-361703950, message.text[8::])
            bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)
    else:
        bot.send_message(message.chat.id, "Введите текст")

@bot.message_handler(commands=["set"])
def set_message(message):
    if message.from_user.id == 522487188:
        my_cursor = my_collection2.find()
        for item in my_cursor:
            if item["idch"] == "prosto":
                if item["val"] == "Числитель":
                    my_collection2.update_one({"idch":"prosto"},{"$set":{"val":"Знаменатель"}})
                    bot.send_message(message.chat.id,"Изменено на знаменатель")
                    break
                else:
                    my_collection2.update_one({"idch":"prosto"},{"$set":{"val":"Числитель"}})
                    bot.send_message(message.chat.id,"Изменено на числитель")
                    break
                    
@bot.message_handler(commands=["rasp"])
def rasp_message(message):
    global prev
    if message.from_user.id in prev:
        my_cursor = my_collection2.find()
        markup2 = types.InlineKeyboardMarkup()
        btn_my_site=types.InlineKeyboardButton(text="Понедельник",callback_data="Mon")
        markup2.add(btn_my_site)
        btn_my_site=types.InlineKeyboardButton(text="Вторник",callback_data="Tue")
        markup2.add(btn_my_site)
        btn_my_site=types.InlineKeyboardButton(text="Среда",callback_data="Wed")
        markup2.add(btn_my_site)
        btn_my_site=types.InlineKeyboardButton(text="Четверг",callback_data="Thu")
        markup2.add(btn_my_site)
        btn_my_site=types.InlineKeyboardButton(text="Пятница",callback_data="Fri")
        markup2.add(btn_my_site)
        for item in my_cursor:
            if item["idch"] == "prosto":
                try:
                    bot.send_message(message.from_user.id, "Выберите день недели\nНа данный момент: " + item["val"], reply_markup = markup2)
                    break
                except:
                    bot.send_message(message.chat.id, message.from_user.first_name + ", напишите мне в личку /start и я смогу отправлять вам сообщения!")
                    break
        bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)
    else:
        bot.send_message(message.from_user.id, "Нет прав. Для получения обращайтесь к создателю.")
        bot.send_message(-326941525, message.from_user.first_name + ": " + "Пытался узнать расписание")
        
@bot.message_handler(commands=["sendgroup"])
def sendgroup(message):
    if message.from_user.id == 522487188:
        for i in prev:
            bot.send_message(i, "Завтра на первую пару идёт первая группа (группа ЮН)")    

@bot.message_handler(commands=["id"])
def id_message(message):
    bot.send_message(message.chat.id,str(message.chat.id))

@bot.message_handler(content_types=["text"])
def text_message(message):
    bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)

bot.polling()
