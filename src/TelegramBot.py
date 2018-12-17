import telepot
from telepot.loop import MessageLoop
import time
import DataBase
import Chat
import Domanda
from Chat import Chat
from DataBase import DataBase
from pprint import pprint
from random import randint
from Domanda import Domanda
from Utente import Utente

bot = telepot.Bot('548040088:AAFs8Y1Msb4367WkDth_HF30hM2j-yXenNQ')
dataBase = DataBase()
domande = list()
insulti = list()
insulti.append("stronzo") 
insulti.append("gay")

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    dataBase.addChat_id(chat_id)
    dataBase.addUtente(msg['from']['id'])
    if(content_type == 'text'):
        dataBase.addMex(chat_id, msg['text'])
               
        if(msg['text'] == "ciao"):
            bot.sendMessage(chat_id, "afangul")
            
        if "?" in msg['text']:
            metti = True
            mex = msg['text'].lower()
            for domanda in domande:
                if (domanda.domanda == mex):
                    metti = False
                    r = randint(-1, len(domanda.risposte)-1)
                    if(len(domanda.risposte))>0:
                        bot.sendMessage(chat_id, domanda.risposte[r], reply_to_message_id = msg['message_id'])
                        break
            if(metti):
                domanda = Domanda()
                domanda.domanda = mex
                domande.append(domanda)
                print (domande[0].domanda)
                
        if ("gay" in msg['text']) | ("Gay" in msg['text']):
            for utente in dataBase.utenti:
                if msg['from']['id'] == utente.id:
                    utente.coin+=1
                    break
                    
        if (msg['text'] == "jjm coin") | (msg['text'] == "Jjm coin"):
            for utente in dataBase.utenti:
                if msg['from']['id'] == utente.id:
                    bot.sendMessage(chat_id,"Hai "+str(utente.coin)+" jjm coin.", reply_to_message_id= msg['message_id'])
                    break;
        
        if msg['text'] == "lista":
            for utente in dataBase.utenti:
                print (utente.id)
                
        if (msg['text'] == "addInsulto") & (msg['from']['id'] == 660824842):
            if (insulti.__contains__(msg['reply_to_message']['text'].lower()))==False:
                insulti.append(msg['reply_to_message']['text'].lower())
            
        if ('reply_to_message' in msg):
            print ("cacca")
            for domanda in domande:
                if domanda.domanda == msg['reply_to_message']['text'].lower():
                    domanda.addRisp(msg['text'])
                    print (domanda.risposte[0])
            for insulto in insulti:
                if (insulto in msg['text'].lower()) & (("è" in msg['text'])==False) & (("È" in msg['text'])==False):
                    for utente in dataBase.utenti:
                        if utente.id == msg['reply_to_message']['from']['id']:
                            if utente.coin >= 1:
                                bot.sendMessage(chat_id, "parli tu", reply_to_message_id= msg['message_id'])
                    
        
        if((msg['text'] == "rfoto") | (msg['text'] == "Rfoto")):
            for chat in dataBase.lista_chat:
                if((chat.chat_id == chat_id) & (len(chat.foto)>0)):
                    r = randint(-1, len(chat.messaggi)-1)
                    r2 = randint(-1, len(chat.foto)-1)
                    bot.sendPhoto(chat_id, chat.foto[r2], chat.messaggi[r])
            
    if(content_type == 'photo'):
        file_id = msg['photo'][-1]['file_id']
        dataBase.addFoto(chat_id, file_id)
        
MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)