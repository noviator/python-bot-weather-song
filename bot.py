from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, ParseMode
import time
import gizoogle
import weather_api_for_bot
from plugins import TEXT
from cred import Creds
from Utils import *
from uuid import uuid4
import os
PORT = int(os.environ.get('PORT', 5000))


def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(TEXT.START.format(first_name))


def giz_echo(update, context):
    f = open("zmsg.txt", "a")
    f.write("\n" + update.message.chat.first_name + ':' + update.message.text)

    t = update.message.reply_text(gizoogle.text(update.message.text))
    f.write("\n" + "Bot : " + t.text)
    f.close()


def options(update, context):
    # print(to_dict(update))
    button_list = [[InlineKeyboardButton("col1", callback_data=time.strftime("%H:%M:%S", time.localtime())),
                    InlineKeyboardButton("col2", callback_data="2")],
                   [InlineKeyboardButton("row 2", callback_data="3")]]
    reply_markup = InlineKeyboardMarkup(
        button_list)  # so that bot displays button
    # update.message.reply_text("click any",reply_markup=reply_markup) # this also works
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Click any of the buttons \nnot working lol ",
                             reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    realData = update.callback_query.data
    try:
        song_link = context.bot_data["callbackDecoder"][realData]
    except:
        song_link = "Sorry the data expired"
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  text="Selected  -   {}".format(song_link),
                                  message_id=query.message.message_id)
    # context.bot.send_audio(chat_id=query.message.chat_id,)


def get_location(update, context):
    location_button = [
        [KeyboardButton("Share location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(location_button)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="please share location",
                             reply_markup=reply_markup)


def location(update, context):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    f = open("zloc.txt", "a")
    f.write("\n" + update.message.chat.first_name + ":  lat :" +
            str(latitude) + ",long : " + str(longitude))
    f.close()

    weather, img_url = weather_api_for_bot.by_coordinate(latitude, longitude)
    context.bot.send_photo(chat_id=update.message.chat_id,
                           photo=img_url, caption="`" + weather + "`",
                           reply_markup=ReplyKeyboardRemove(),
                           parse_mode=ParseMode.MARKDOWN_V2)

    f = open("zweather_history.txt", "a")
    f.write("\n" + update.message.chat.first_name + "\n" + weather)
    f.close()
######################################################################################################


def song(update, context):
    qry = "+".join(str(update.message.text).lower().split()
                   ).replace("/song+", "")
    # print(qry)
    data = search(qry)
    if not data:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry,  song not found !!")
    else:
        songs_btn_list = []
        count = 0
        for j in data:
            uuid = str(uuid4())
            context.bot_data["callbackDecoder"][uuid] = play(data[count]['id'])
            new_song_btn = InlineKeyboardButton("{} [ {} ]".format(j['title'], j['subtitle']),
                                                callback_data=uuid)
            songs_btn_list.append(new_song_btn)
            count += 1
        reply_markup = InlineKeyboardMarkup(
            build_menu(songs_btn_list, n_cols=1))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Select the song", reply_markup=reply_markup)
        # val=context.chat_data.get("key","not found")
        # url = play(data[choose]['id'])


########################################################################

def main():
    # check for new messages (polling)
    bot_token = Creds.bot_token
    updater = Updater(token=bot_token, use_context=True, workers=8)

    # allows to register handlers -> command ,text, video, audio etc.
    dispatcher = updater.dispatcher
    # to store data(song links)
    updater.dispatcher.bot_data["callbackDecoder"] = {}

    # handlers
    song_handler = CommandHandler("song", song)
    start_handler = CommandHandler("start", start)
    giz_echo_handler = MessageHandler(Filters.text, giz_echo)
    option_handler = CommandHandler("options", options)
    button_handler = CallbackQueryHandler(button)
    get_location_handler = CommandHandler("location", get_location)
    location_handler = MessageHandler(Filters.location, location)
    dispatcher.add_handler(location_handler)

    # order of dispatched handler matters

    dispatcher.add_handler(song_handler)
    dispatcher.add_handler(option_handler)
    dispatcher.add_handler(button_handler)
    dispatcher.add_handler(get_location_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(giz_echo_handler)

    # start polling
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=bot_token)
    # updater.bot.setWebhook(
    #     'https://appname.herokuapp.com/' + bot_token)
    updater.idle()


if __name__ == '__main__':
    main()
