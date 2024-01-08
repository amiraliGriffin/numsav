from pyrogram import Client

plug = dict(root="plugins")
#----
bot = Client(
    name = "Pa",
    api_id = 29585063,
    api_hash = "7cbc271846d81539d10bdec6cf36ba6a",
    bot_token = "6703791627:AAEcP1rPAloQmS5Gx-AIHDsTxo8-H5MFktU",
    plugins = plug,
)

bot.run()
