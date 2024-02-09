from pyrogram import Client , filters
from pyrogram import StopPropagation as stop
from pyrogram import enums
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardMarkup as ink
from pyrogram.types import InlineKeyboardButton as inb
from pyrogram.types import KeyboardButton as keyb
from pyrogram.types import ReplyKeyboardRemove as Kremover
import json
#-----------
CD = {
    "err_check_num" : "لطفا از اعداد در نام خود استفاده نکنید",
    "register_confirmation" : "اطلاعات شما با موفقیت ثبت شد✅\nمنتظر تماس نمایندگان ما باشید\nدر صورت اشتباه در ثبت اطلاعات یا ثبت اطلاعات برای شخص دیگری مجددا از دستور /start استفاده نمایید",
    "name_ask"  : "لطفا نام و نام خانوادگی خودرا وارد نمایید",
    "confirmation_name" : "نام شما با موفقیت ثبت شد✅\nبا کلیک بر روی دکمه زیر شماره خود را به اشتراک بگذارید\nدر صورتی که مایل به ثبت شماره دیگری هستید شماره خود را وارد کنید",
    "confirmation_phone" : "شماره شما با موفقیت ثبت شد✅\nلطفا ساعت مشاوره خود را انتخاب کنید"
}
number_persian_dic = {
    "۰" : "0",
    "۱" : "1",
    "۲" : "2",
    "۳" : "3",
    "۴" : "4",
    "۵" : "5",
    "۶" : "6",
    "۷" : "7",
    "۸" : "8",
    "۹" : "9",
    "0" : "0",
    "1" : "1",
    "2" : "2",
    "3" : "3",
    "4" : "4",
    "5" : "5",
    "6" : "6",
    "7" : "7",
    "8" : "8",
    "9" : "9",
}
#-----------
def file_get_contents(address):
    file = open(address)
    file = file.readlines()
    return file
def file_put_contents(address,element,mode="w"):
    if mode == "w" :
        file = open(address,mode)
        file = file.write(element)
        return True
    elif mode == "a" :
        file = open(address,mode)
        file = file.write(element)
        return True
    else :
        return False
def Jread(address):
   jfile = open(address)
   jobj = json.load(jfile)
   return jobj
def Jwrite(address,obj):
   jobj = json.dumps(obj)
   file_put_contents(address,jobj)
def Jdelete(address,item):
   js  = Jread(address)
   #--
   del js[item]
   #--
   Jwrite(address,js)
def request_counter():
    C = file_get_contents("DB/request_count.txt")
    C = int(C[0])
    C += 1
    C = str(C)
    file_put_contents("DB/request_count.txt",C)
#----- General filters
def BotMode(mode) :
    def func(hand,__,message) :
        try :
            CHI = message.chat.id
            file = file_get_contents(f"BM/{CHI}.txt")
            file = file[0]
            return hand.data == file
        except :
            x = "nothing to do"
    return filters.create(func,data=mode)
#------------
@Client.on_message(BotMode("Greeting") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL"))
def greet(client,message):
    CHI  = str(message.chat.id)
    text = str(message.text)
    #-----
    try : 
        numstr = "0123456789"
        for num in numstr :
            if num in text :
                raise Exception("do not use numbers")
    except :
        client.send_message(CHI,CD["err_check_num"])
    else :
        try :
            obj = Jread("DB/db.json")
            obj[CHI]["name"] = text
            Jwrite("DB/db.json",obj)
        except :
            obj = Jread("DB/db.json")
            obj[CHI] = {"name" : text}
            Jwrite("DB/db.json",obj)
        #-----
        kb = ReplyKeyboardMarkup(
                [
                    [
                        keyb("اشتراک گذاری تلفن همراه📳",request_contact=True)
                    ]
                ]
            )
        client.send_message(CHI,CD["confirmation_name"],reply_markup=kb)
        #----
        file_put_contents(f"BM/{CHI}.txt","Phone")
        #-----
    request_counter()
    raise stop
@Client.on_message(BotMode("visit") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL"))
def visit(client,message):
    CHI  = str(message.chat.id)
    text = str(message.text)
    username = "@" + str(message.from_user.username)
    if username == "@None" :
        username = "❌"
    #-----
    try :
        x = "a"
        if text == "۸ الی ۱۲" :
            x = 1
        elif text == "۱۲ الی ۱۶" :
            x = 1
        elif text == "۱۶ الی ۲۰" :
            x = 1
        x = int(x)
        obj = Jread("DB/db.json")
        obj[CHI]["Visit"]= text
        Jwrite("DB/db.json",obj)
        #-----
        file_put_contents(f"BM/{CHI}.txt","off")
        #------
        chanID = -1002025719431
        obj = Jread("DB/db.json")
        profile = obj[CHI]
        #------
        name         = profile["name"]
        phone_number = profile["phone_number"]
        visit        = profile["Visit"]
        #------
        txt = f"🔹نام و نام خانوادگی = {name}\n🔹شماره تماس= {phone_number}\n🔹دسترسی به کاربر = [find me here](tg://user?id={CHI})\n🔹آیدی = {username}\n🔹ساعت مشاوره : {visit}"
        client.send_message(chanID,txt,parse_mode=enums.ParseMode.MARKDOWN)
        #----
        client.send_message(CHI,CD["register_confirmation"],reply_markup=Kremover())
        #----
        file_put_contents(f"BM/{CHI}.txt","off")
        #-----
        request_counter()
    except :
        client.send_message(CHI,"لطفا ساعت مشاوره صحیح را انتخاب کنید❌")
    raise stop
@Client.on_message((filters.contact | BotMode("Phone")) & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL"))
def contact(client,message):
    CHI   = str(message.chat.id)
    text  = message.text
    try :
        phone = message.contact.phone_number
        #-----
        obj = Jread("DB/db.json")
        obj[CHI]["phone_number"] = phone 
        Jwrite("DB/db.json",obj)
        #------
        kb = ReplyKeyboardMarkup([
            [
                "۸ الی ۱۲",
                "۱۲ الی ۱۶",
                "۱۶ الی ۲۰"
            ]

        ])
        client.send_message(CHI,CD["confirmation_phone"],reply_markup=kb)
        file_put_contents(f"BM/{CHI}.txt","visit")
    except :
        try :
            text = str(text)
            for char in text :
                text.replace(char,number_persian_dic[char])
            phone = int(text)
            phone = str(phone)
            cnt = 0
            for num in phone :
                cnt+=1
            #-----
            phone = str(int(phone))
            if cnt == 10 :
                obj = Jread("DB/db.json")
                obj[CHI]["phone_number"] = phone 
                Jwrite("DB/db.json",obj)
                #------
                kb = ReplyKeyboardMarkup([
                    [
                        "۸ الی ۱۲",
                        "۱۲ الی ۱۶",
                        "۱۶ الی ۲۰"
                    ]

                ])
                client.send_message(CHI,CD["confirmation_phone"],reply_markup=kb)
                file_put_contents(f"BM/{CHI}.txt","visit")
            else :
                raise Exception("digit style incorrect")
        except :
            client.send_message(CHI,"❌خطا")
    request_counter()
    raise stop
@Client.on_message(BotMode("STA") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL") & ~filters.regex("send to all") & ~filters.regex("real time request"))
def lets_send(client,message):
    CHI     = str(message.chat.id)
    if hasattr(message.video,'file_id') :
        file_id = message.video.file_id
        cap = message.caption
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_video(person,file_id,caption=cap)
    elif hasattr(message.voice,'file_id') :
        file_id = message.voice.file_id
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_voice(person,file_id)
    elif hasattr(message.photo,'file_id') :
        file_id = message.photo.file_id
        cap = message.caption
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_photo(person,file_id,caption=cap)
    elif hasattr(message.audio,'file_id') :
        file_id = message.audio.file_id
        cap = message.caption
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_audio(person,file_id,caption=cap)
    elif hasattr(message.document,'file_id') :
        file_id = message.document.file_id
        cap = message.caption
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_document(person,file_id,caption=cap)
    else :
        text = message.text
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_message(person,text)
    #-----
    client.send_message(CHI,"پیام شما برای تمامی کاربران ارسال شد✅",reply_markup=Kremover())
    file_put_contents(f"BM/{CHI}.txt","off")
    raise stop
