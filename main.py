# -*- coding: utf-8 -*-
import config
import telebot

import os
import shutil

from telebot import types
from timeout import timeout

bot = telebot.TeleBot(config.token)

# ----------------------------------------------------------
# Home page


def homeKeyboard(message):
    print("User {username}, open page 'home'.".format(
        username=message.from_user.username))

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row('Manual', 'New pack')
    bot.send_message(message.chat.id, 'Home page:', reply_markup=keyboard)


# ----------------------------------------------------------
# New pack
@bot.message_handler(func=lambda message: message.text == 'New pack')
def newPack(message):
    print("User {username}, open page 'New pack'.".format(
        username=message.from_user.username))

    basePath = 'files/' + str(message.chat.id)
    if os.path.exists(basePath):
        shutil.rmtree(basePath)

    zipPath = basePath + '.zip'
    if os.path.exists(zipPath):
        os.remove(zipPath)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row('Cancel', 'Done')

    msg = '''
Please send me stickers
    '''
    bot.send_message(message.chat.id, msg, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Cancel')
def cancel(message):
    print("User {username}, cancel 'New pack'.".format(
        username=message.from_user.username))
    homeKeyboard(message)


@bot.message_handler(content_types=['sticker'])
def downloadStickers(message):
    print("User {username}, add sticker.".format(
        username=message.from_user.username))

    sticker = bot.get_file(message.sticker.file_id)

    fileName = str(sticker.file_id) + '.png'
    basePath = 'files/' + str(message.chat.id)
    if not os.path.exists(basePath):
        os.makedirs(basePath)

    path = basePath + '/' + fileName
    if not os.path.exists(path):
        downloaded_file = bot.download_file(sticker.file_path)
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Sticker added')
    else:
        bot.send_message(
            message.chat.id, '<b>Sticker already added!</b>', parse_mode='html')


@bot.message_handler(func=lambda message: message.text == 'Done')
def done(message):
    basePath = 'files/' + str(message.chat.id)
    if os.path.exists(basePath):
        print("User {username}, created an archive.".format(
                username=message.from_user.username))

        shutil.make_archive(basePath, 'zip', basePath)

        def checkZip():
            zipPath = basePath + '.zip'
            if os.path.exists(zipPath):
                bot.send_message(
                    message.chat.id, '<b>Congratulations! Your pack is ready, follow the instructions from point 4.</b>', parse_mode='html')
                bot.send_document(
                    message.chat.id, open(zipPath, 'rb'))
                homeKeyboard(message)
        timeout(checkZip, seconds=0.5)
    else:
        print("User {username}, tried create an archive without stickers.".format(
                username=message.from_user.username))

        bot.send_message(
            message.chat.id, '<b>Please add stickers!</b>', parse_mode='html')

# ----------------------------------------------------------
# Manual


@bot.message_handler(func=lambda message: message.text == 'Manual')
def manual(message):
    print("User {username}, open page 'manual'.".format(
        username=message.from_user.username))

    msg = '''
<b>Manual</b>

1. Click the "New pack" button.
2. Add your favorite stickers.
3. Click the "Done" button.
4. Download the archive and unzip it.
    <b>
    Now you can use stickers like pictures,
    or follow the instructions below to add
    them to Telegram.
    </b>
5. Go to the @Stickers bot.
6. Select /newpack.
7. Enter the name of the sticker set.
8. Send the bot files from the archive
    as a document.
9. Enter the smiley.
10. Follow steps 8, 9 with all the files.
11. Select /publish.
12. Enter the name in Latin.
13. Done!
    '''
    bot.send_message(message.chat.id, msg, parse_mode='html')

# ----------------------------------------------------------


@bot.message_handler(commands=['start'])
def commandStart(message):
    print("User {username}, joined.".format(
        username=message.from_user.username))

    msg = '''
<b>Welcome!</b>

This bot makes a pack of stickers sent to it or upload them as pictures.


I do not know much English :(
    '''
    bot.send_message(message.chat.id, msg, parse_mode='html')
    homeKeyboard(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
