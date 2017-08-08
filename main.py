# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import os
import shutil
from timeout import timeout

bot = telebot.TeleBot(config.token)

# ----------------------------------------------------------
# Home page


def homeKeyboard(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row('Manual', 'New pack')
    bot.send_message(message.chat.id, 'Home page:', reply_markup=keyboard)


# ----------------------------------------------------------
# New pack
@bot.message_handler(func=lambda message: message.text == 'New pack')
def newPack(message):
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
    homeKeyboard(message)


@bot.message_handler(content_types=['sticker'])
def downloadStickers(message):
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
        shutil.make_archive(basePath, 'zip', basePath)

        def checkZip():
            zipPath = basePath + '.zip'
            if os.path.exists(zipPath):
                bot.send_message(message.chat.id, '<b>Congratulations! Your pack is ready, click "Manual"</b>', parse_mode='html')
                bot.send_document(
                    message.chat.id, open(zipPath, 'rb'))
                homeKeyboard(message)
        timeout(checkZip, seconds=0.5)
    else:
        bot.send_message(
            message.chat.id, '<b>Please add stickers!</b>', parse_mode='html')

# ----------------------------------------------------------
# Manual
#TODO: Manual

@bot.message_handler(func=lambda message: message.text == 'Manual')
def manual(message):
    msg = '''
<b>Manual</b>
    '''
    bot.send_message(message.chat.id, msg, parse_mode='html')

# ----------------------------------------------------------


@bot.message_handler(commands=['start'])
def commandStart(message):
    msg = '''
<b>Welcome!</b>

This bot makes a pack of stickers sent to it.
    '''
    bot.send_message(message.chat.id, msg, parse_mode='html')
    homeKeyboard(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
