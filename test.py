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
TOKEN='5840488180:AAFr_Zs9Ztj2L-zPWdcT-JHUiE-deiqT3Bg' 
bot = telebot.TeleBot(TOKEN)


def table(words,digits):
    """создает таблицу эксель"""
    
    df = pd.DataFrame({'Товар': words,
                   'Количество': digits})
    df.to_excel(f'{int(time())}.xlsx')
    
def parse(tokens):
    """создает два отдельных списка с товарами и количеством"""
    words=[]
    digits=[]
    for i in range(1,len(tokens)):
        tokens[i][0]=(tokens[i][0])[1:]
    for i in range(len(tokens)):
        if tokens[i][0] not in words:
            words.append(tokens[i][0])
            digits.append(int(tokens[i][1]))
        else:
            place=words.index(tokens[i][0])
            digits[place]+=(int(tokens[i][1]))
    
    table(words,digits)

def toTokens(text) -> list:
    """разделяет сообщение на отдельные фразы"""
    tokens = [list(s) for s in re.findall(r"(\D+\s)(\d+)", text)]
    return tokens
    
def recognise(filename) -> list:
    """распознает речь"""
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language="ru-RU")
    return text

def audio(file) -> str:
    """переводит .ogg в .wav для корректной работы"""
    src = file
    dst = f'{int(time())}.wav'
    sound = AudioSegment.from_ogg(src)
    sound.export(dst, format="wav")
    return dst

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    """обработка голосовых сообщений"""
    
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file1=f'{message.chat.id}_{int(time())}.ogg'
    with open(file1, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    file=audio(file1)
    text=recognise(file)
    bot.send_message(message.chat.id, text)
    
    tokens=parse(toTokens(text))
    
bot.polling()
