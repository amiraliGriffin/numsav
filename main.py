from pyrogram import Client

plug = dict(root="plugins")
#----
bot = Client(
    name = "Pa",
    api_id = 29585063,
    api_hash = "7cbc271846d81539d10bdec6cf36ba6a",
    bot_token = "6881221790:AAH-p3mQYh0Z3vIwigZuiwQ7om1sAe5iKP0",
    plugins = plug,
)

bot.run()
