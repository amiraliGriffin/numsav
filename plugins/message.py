from pyrogram import Client , filters
from pyrogram import StopPropagation as stop
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardMarkup as ink
from pyrogram.types import InlineKeyboardButton as inb
from pyrogram.types import BotCommand as cmd
from pyrogram.types import ReplyKeyboardRemove as Kremover
import json
#----------
CD = {
    "err_check_num" : "❌لطفا از اعداد در نام خود استفاده نکنید",
    "confirmation_for_name" :  "نام شما با موفقیت ثبت شد✅\nبا کلیک بر روی دکمه زیر شماره خود را به اشتراک بگذارید\nvدر صورتی که مایل به ثبت شماره دیگری هستید شماره خود را وارد کنید",
    "register_confirmation" : "به خانواده برزگ ایولرن خوش آمدید😍\nمنتظر تماس منتور ها باشید",
    "name_ask"  : "لطفا نام و نام خانوادگی خودرا وارد نمایید",
    "field_ask" : "شماره شما با موفقیت ثبت شد✅\nدانشجوی عزیز لطفا رشته خود را انتخاب نمایید"
}
#------ General functions
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
def request_counter():
    C = file_get_contents("DB/request_count.txt")
    C = int(C[0])
    C += 1
    C = str(C)
    file_put_contents("DB/request_count.txt",C)
#----------
@Client.on_message(filters.command("start"))
def start(client,message) :
    CHI = message.chat.id
    client.send_message(CHI,CD["name_ask"],reply_markup=Kremover())
    file_put_contents(f"BM/{CHI}.txt","Greeting")
    #----
    client.set_bot_commands([
        cmd("start","start the bot")
    ])
    #----
    request_counter()
    raise stop
@Client.on_message(filters.regex("ADMIN_PRIVATE_PANEL"))
def admin(client,message):
    CHI = message.chat.id
    #-----
    kb = ReplyKeyboardMarkup([
        ["send to all"],
        ["real time request"]
    ]
    )
    file_put_contents(f"BM/{CHI}.txt","off")
    client.send_message(CHI,"لطفا گزینه مورد نظر انتخاب کنید",reply_markup=kb)
    raise stop
@Client.on_message(filters.regex("send to all"))
def STA(client,message):
    CHI = message.chat.id
    #------
    client.send_message(CHI,"لطفا پیام خود را ارسال کنید")
    file_put_contents(f"BM/{CHI}.txt","STA")
    raise stop
@Client.on_message(filters.regex("real time request"))
def realreq(client,message):
    CHI = message.chat.id
    #------
    RR = file_get_contents("DB/request_count.txt")
    RR = RR[0]
    client.send_message(CHI,RR)
    raise stop
@Client.on_message(~filters.command("start"))
def error(client,message):
    CHI = message.chat.id
    #----
    client.send_message(CHI,"❌")




