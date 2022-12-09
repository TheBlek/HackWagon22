from time import time
import speech_recognition as sr
import telebot
import uuid
import os
from os import path
from pydub import AudioSegment
import re
import pandas as pd


language='ru_RU' 
TOKEN='TOKEN'
bot = telebot.TeleBot(TOKEN)

frames = pd.DataFrame({'Товар': [],
                   'Количество': []})

def table(df):
    df.to_excel(f'{int(time())}.xlsx')

def toTokens(text):
    tokens = [list(s) for s in re.findall(r"(\D+\s)(\d+)", text)]
    return tokens
    
def recognise(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language="ru-RU")
    return text


@bot.message_handler(content_types=['voice'])

def voice_processing(message):
    global frames

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file1=f'{message.chat.id}_{int(time())}.ogg'
    with open(file1, 'wb') as new_file:
        new_file.write(downloaded_file)
    src = file1
    dst = f'{message.chat.id}_{int(time())}.wav'
    sound = AudioSegment.from_ogg(src)
    sound.export(dst, format="wav")
    text=recognise(dst)
    bot.send_message(message.chat.id, text)
    tokens=toTokens(text)

    for i in range(1,len(tokens)):
        tokens[i][0]=(tokens[i][0])[1:]
    
    for token in tokens:
        print(frames)
        if not ((frames['Товар'].eq(token[0])).any()):
            new_frame = pd.DataFrame({'Товар': [token[0]],
                                    'Количество': [int(token[1])]})
            print('-')
            frames = pd.concat([frames, new_frame], ignore_index=True)
        else:
            print('+')
            frames.loc[frames['Товар']==token[0], 'Количество'] += int(token[1])

    print(frames)
    table(frames)

bot.polling()
