# -*- coding: utf-8 -*-
import os

print('\n')
token = ''
if not os.path.exists('token.txt'):
    token = input('Please enter your token fom BotFather: ')
    if input('Do you want to keep the token? "Y" or "N": ') == "Y":
        open('token.txt', 'w').write(token)
else:
    print("If you want to reset the token, delete the file 'token.txt'. \n")
    token = open('token.txt', 'r').read()
