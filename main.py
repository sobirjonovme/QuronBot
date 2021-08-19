

import logging
import json
from telegram.constants import PARSEMODE_HTML


from admin_funksiyalari import users_list, users_number
from surah import suralar_raqami
from quron_search import oyat_top, sura_info, oyat_soni



from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardMarkup,
    keyboardbutton,
    message,
    update
)

from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)

# import os

# PORT = int(os.environ.get('PORT', '8443'))



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)





baza_fayl_nomi = "quron_bot_baza.json"


asosiy_tugma = "Suralar ro'yxati"
kitob_haqida = "Qur'oni Karim haqida"


main_buttons = ReplyKeyboardMarkup(
    [
        [
            asosiy_tugma,
            kitob_haqida,
        ],
    
	],
    resize_keyboard=True
)







def start(update: Update, context: CallbackContext):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    foydalanuvchi = update.effective_user
    username = user.full_name
    logger.info("User %s started the conversation.", user.first_name)


    # Foydalanuvchilar haqidagi ma'lumotni bazaga saqlab boradi
    with open(baza_fayl_nomi, "r") as f:
        baza_malumoti = json.load(f)

    with open(baza_fayl_nomi, "w") as f:
        baza_malumoti["users"][str(foydalanuvchi.id)] = {
            "full_name" : foydalanuvchi.full_name,
            "user_name" : foydalanuvchi.username,
        }
        json.dump(baza_malumoti, f, indent=4)




    keyboard = [
        [
            InlineKeyboardButton(asosiy_tugma, callback_data=asosiy_tugma),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    
    update.message.reply_html(text=f"<b>Assalom-u alaykum, <i> {username}</i> </b>\n\n\
🤖 Men orqali <b>Qur'oni Karim suralari</b>ning o'zbekcha tarjimasini topishingiz mumkin 📖", reply_markup=main_buttons)
    
    kirish = "<i>Bismillahir rohmanir rohiym</i> \n        <b>QUR'ONI KARIM</b>\n\n"
    kirish += "<i>Tarjima muallifi:</i> <b>Shayx Muhammad Sodiq Muhammad Yusuf</b>\n"
    kirish += "<i>Suralar haqida:</i> <b>Alouddin Mansur</b>\n\n"
    kirish += "<i>Abdulaziz Mansur:\n</i>"
    kirish += """   Ma'lumki, Qur'oni karim Alloh taolo tomonidan Payg'ambarimiz Muhammad alayhissalomga 23 yil mobaynida sura, oyat tarzida elchi farishta –Jabroil alayhissalom orqali ilohiy vahiy sifatida, arab tilida, og'zaki nozil qilingan. Islom dini ta'limotining asosiy manbalari (Qur'on, Sunnat, Ijmo', Qiyos)ning birinchisi sanalmish bu Kalomi sharifning til va bayon jihatidan ilohiy mo'jizaligi ham uni arab tilida o'qib, fikr yuritgandagina namoyon bo'ladi. Boshqa har qanday tilga o'girilganda Qur'on tiliga xos xususiyatlar, nazmiy uslub, maftunkor ohang va ruhiy ta'sir o'z kuchini yo'qotadi. Tarjimon har qancha mahoratli, tajribali lug'atga boy bo'lmasin, oyatlarning arabcha holidagi mazmunini boshqa tilda mukammal ifoda eta olmaydi. Bu inkor etib bo'lmas haqiqat.
   Arab tilida o'qib anglash esa, hammaning ham imkon darajasida emas. Hatto arablarning o'zlari ham Qur'on oyatlarini to'la tushuna olmasliklarini tan oladilar. Ulug' sahobalar ham ko'pdan-ko'p oyatlar mazmunida bahslashib, bir yechimga kelisha olmay, Rosul alayhissalomning o'zlaridan so'rab, aniqlab olganlari to'g'risida sahih hadislar mavjud. """
    kirish += "\n\n<i>Kamchiliklar uchun avvaldan uzur!</i>"

    update.message.reply_html(text=kirish, reply_markup=reply_markup)




def admin_sozlamalari(update: Update, context: CallbackContext):
    parol = context.args[0]
    if parol == "hunter2003":
        keyboard = [
            [
                InlineKeyboardButton("Foydalanuvchilar ro'yxati", callback_data="foydalanuvchilar_royxati"),
            ],
            [
                InlineKeyboardButton("Baza(json) fayli", callback_data="baza_fayl")
            ]
        ]
        reply_keyboard = InlineKeyboardMarkup(keyboard)

        matn = "<b>Xush kelibsiz!</b>\n\n"
        matn += f"<i>Hozirda <b>bot</b>dan </i> <b>{users_number()}</b> <i>nafar odam foydalanmoqda</i>"
        update.message.reply_html(text=matn, reply_markup=reply_keyboard)

def foydalanuvchi_saqla(update: Update, context: CallbackContext): 
    # Foydalanuvchilar haqidagi ma'lumotni bazaga saqlab boradi
    
    foydalanuvchi = update.effective_user

    with open(baza_fayl_nomi, "r") as f:
        baza_malumoti = json.load(f)

    with open(baza_fayl_nomi, "w") as f:
        baza_malumoti["users"][str(foydalanuvchi.id)] = {
            "full_name" : foydalanuvchi.full_name,
            "user_name" : foydalanuvchi.username,
        }
        json.dump(baza_malumoti, f, indent=4)



def royxat_tuz(a):
    a = str(a)
    if a == '11':
        keyboard = [
            [
                InlineKeyboardButton('111', callback_data="sura|111|11"),
                InlineKeyboardButton('112', callback_data="sura|112|11"),
                InlineKeyboardButton('113', callback_data="sura|113|11"),
                InlineKeyboardButton('114', callback_data="sura|114|11"),
            ],
            [
            InlineKeyboardButton("⬅️", callback_data=f"sura|ortga|{a}"),
            InlineKeyboardButton("➡️", callback_data=f"sura|oldinga|{a}"),
        ]
    ]
    else:
        b = ''
        if a != '0':
            b = a
        lst = []
        for c in range(1,10):
            lst.append((str(b)+str(c)))
        lst.append(str((int(a)+1)*10))
        keyboard = [[],[],[
            InlineKeyboardButton("⬅️", callback_data=f"sura|ortga|{a}"),
            InlineKeyboardButton("➡️", callback_data=f"sura|oldinga|{a}"),
        ]]
        for d in lst[:5]:
            keyboard[0].append(InlineKeyboardButton(d, callback_data=f"sura|{d}|{a}"))
        for d in lst[5:10]:
            keyboard[1].append(InlineKeyboardButton(d, callback_data=f"sura|{d}|{a}"))
    inlinekeyboard = InlineKeyboardMarkup(keyboard)
    
    return inlinekeyboard
        

def suralar_chiqar(a):
    a = str(a)
    if a == '11':
       lst = ["111", "112", "113", "114"]
       matn = f"<b>Qur'on suralari ro'yxati</b>\n {lst[0]}-{lst[3]}   <i>114</i> dan\n\n"
    else:
        b = ''
        if a != '0':
            b = a
        lst = []
        for c in range(1,10):
            lst.append(b+str(c))
        lst.append(str((int(a)+1)*10))
        matn = f"<b>Qur'on suralari ro'yxati</b>\n {lst[0]}-{lst[9]}   <i>114</i> dan\n\n"
    for d in lst:
        matn += f"<b>{d}.  <i> {suralar_raqami[d]}</i></b>   surasi  \n"
    return matn


def royxat_tuz2(a1, a2):
    # a1 - sura raqami
    # a2 - sahifa raqami
    a1, a2 = int(a1), int(a2)
    soni = oyat_soni(a1)
    if a2 == soni//5:
        lst = list(range(a2*5+1,soni+1))
    else:
        lst = list(range(a2*5+1, a2*5+6))
    keyboard = [
        [],
        [
            InlineKeyboardButton("⬅️", callback_data=f"oyat|{a1}|{a2}|ortga"),
            InlineKeyboardButton("➡️", callback_data=f"oyat|{a1}|{a2}|oldinga")
        ]
    ]
    for d in lst:
        keyboard[0].append(InlineKeyboardButton(d, callback_data=f"oyat|{a1}|{a2}|{d}"))
        # f"oyat|{a1}|{a2}|{d}"   d - oyat raqami
    inlinekeyboard = InlineKeyboardMarkup(keyboard)
    return inlinekeyboard


def oyat_chiqar(a1, a2):
    # a1 - sura raqami
    # a2 - sahifa raqami
    a1, a2 = int(a1), int(a2)
    soni = oyat_soni(a1)
    if a2 == soni//5:
        lst = list(range(a2*5+1,soni+1))
    else:
        lst = list(range(a2*5+1, a2*5+6))
    matn = f"<b><i>{suralar_raqami[str(a1)]}</i>   surasi oyatlari</b>\n{lst[0]}-{lst[-1]}   <i>{soni} dan</i>\n\n" 

    for d in lst:
        matn += f"<b>{d}.</b>  {oyat_top(a1, d)}\n\n"
    
    return matn


    
def funk1(update: Update, context: CallbackContext):
   
    ana = context.bot.send_message(chat_id=update.effective_message.chat_id,
            text="Iltimos biroz kuting...")
    

    query = update.callback_query
    query.answer()

    data = update.callback_query.data
    if data == asosiy_tugma:
        inlinekeyboard = royxat_tuz(0)
        matn = suralar_chiqar(0)
        query.edit_message_text(text=matn, parse_mode=PARSEMODE_HTML, reply_markup=inlinekeyboard)

    if 'sura' in data:
        a = data.split("|")[2]
        # a - sahifa raqami
        
        b = None
        if "ortga" in data:
            if a == "0":
                print("Allaqachon birinchi sahifadasiz") 
            else:
                b = int(a)-1
        elif "oldinga" in data:
            if a == "11":
                print("Allqachon oxirgi sahifadasiz")
            else:
                b = int(a)+1
        else:
            k = data.split("|")[1]
            k = str(k)
            # k - sura raqami
            k1 = suralar_raqami[str(k)]
            # k1 - sura nomi
            txt = f"<b>{k1}  <i>surasi \n{oyat_soni(k)}</i> ta oyat</b>dan tashkil topgan\n\n{sura_info(k)}"
            key = [
                [InlineKeyboardButton(f"{suralar_raqami[str(k)]} surasi oyatlarini ko'rish",
                callback_data=f"oyat|{k}|bosh")]
            ]
            in_key = InlineKeyboardMarkup(key)
            query.edit_message_text(text=txt,
                            parse_mode=PARSEMODE_HTML, reply_markup=in_key)
            
        if b != None:
            inlinekeyboard = royxat_tuz(b)
            matn = suralar_chiqar(b)
            query.edit_message_text(text=matn,
                            parse_mode=PARSEMODE_HTML, reply_markup=inlinekeyboard)
    
    if "oyat" in data:
        sura_r = data.split("|")[1]
        if "bosh" in data:
            inlinekeyboard = royxat_tuz2(sura_r, 0)
            matn = "<b><i>Mehribon va rahmli Alloh nomi bilan (boshlayman). </i></b>\n\n"
            matn += oyat_chiqar(sura_r, 0)
            context.bot.send_message(chat_id=update.effective_message.chat_id,
                text=matn,parse_mode=PARSEMODE_HTML, reply_markup=inlinekeyboard)
        else:
            sahifa_tartibi = data.split("|")[2]  
            oyat_s = oyat_soni(sura_r)
            p = None 
            if "ortga" in data:
                if sahifa_tartibi == "0":
                    print("Siz allaqachon birinchi sahifadasiz")
                else:
                    p = int(sahifa_tartibi) - 1
            elif "oldinga" in data:
                if sahifa_tartibi == str(oyat_s//5):
                    print("Siz allaqachon oxirgi sahifadasiz")
                else:
                    p = int(sahifa_tartibi) + 1 
            else:
                oyat_r = data.split("|")[3]
                oyat_self = "<b>QUR'ONI KARIM</b>\n"
                oyat_self += f"<b>{suralar_raqami[sura_r]}</b> <i>surasi</i>, <b>{oyat_r}</b>–<i>oyat</i>\n\n"
                oyat_self += oyat_top(sura_r, oyat_r)
                context.bot.send_message(chat_id=update.effective_message.chat_id,
                text=oyat_self, parse_mode=PARSEMODE_HTML)

                
            if p != None:
                inlinekeyboard = royxat_tuz2(sura_r, p)
                matn = oyat_chiqar(sura_r, p)
                query.edit_message_text(text=matn,
                                parse_mode=PARSEMODE_HTML, reply_markup=inlinekeyboard)

    if "foydalanuvchilar_royxati" in data:
        context.bot.send_message(
            chat_id=update.effective_user.id, text=users_list())
    
    if "baza_fayl" in data:
        file = open(baza_fayl_nomi, "r")
        context.bot.send_document(
            chat_id=update.effective_user.id, document=file)

    try:
        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                    message_id=ana.message_id)
    except:
        print("Kutish haqidagi xabarni o'chirishda xatolik")


def funk2(update: Update, context: CallbackContext):
    inlinekeyboard = royxat_tuz(0)
    matn = suralar_chiqar(0)
    update.message.reply_text(text=matn, parse_mode=PARSEMODE_HTML, reply_markup=inlinekeyboard)
    
    # Foydalanuvchilar haqidagi ma'lumotni bazaga saqlab boradi
    foydalanuvchi_saqla(update, context)
    

def funk3(update: Update, context: CallbackContext):

    keyboard = [
        [
            InlineKeyboardButton(asosiy_tugma, callback_data=asosiy_tugma),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    kirish = "<i>Bismillahir rohmanir rohiym</i> \n        <b>QUR'ONI KARIM</b>\n\n"
    kirish += "<i>Tarjima muallifi:</i> <b>Shayx Muhammad Sodiq Muhammad Yusuf</b>\n"
    kirish += "<i>Suralar haqida:</i> <b>Alouddin Mansur</b>\n\n"
    kirish += "<i>Abdulaziz Mansur:\n</i>"
    kirish += """   Ma'lumki, Qur'oni karim Alloh taolo tomonidan Payg'ambarimiz Muhammad alayhissalomga 23 yil mobaynida sura, oyat tarzida elchi farishta –Jabroil alayhissalom orqali ilohiy vahiy sifatida, arab tilida, og'zaki nozil qilingan. Islom dini ta'limotining asosiy manbalari (Qur'on, Sunnat, Ijmo', Qiyos)ning birinchisi sanalmish bu Kalomi sharifning til va bayon jihatidan ilohiy mo'jizaligi ham uni arab tilida o'qib, fikr yuritgandagina namoyon bo'ladi. Boshqa har qanday tilga o'girilganda Qur'on tiliga xos xususiyatlar, nazmiy uslub, maftunkor ohang va ruhiy ta'sir o'z kuchini yo'qotadi. Tarjimon har qancha mahoratli, tajribali lug'atga boy bo'lmasin, oyatlarning arabcha holidagi mazmunini boshqa tilda mukammal ifoda eta olmaydi. Bu inkor etib bo'lmas haqiqat.
   Arab tilida o'qib anglash esa, hammaning ham imkon darajasida emas. Hatto arablarning o'zlari ham Qur'on oyatlarini to'la tushuna olmasliklarini tan oladilar. Ulug' sahobalar ham ko'pdan-ko'p oyatlar mazmunida bahslashib, bir yechimga kelisha olmay, Rosul alayhissalomning o'zlaridan so'rab, aniqlab olganlari to'g'risida sahih hadislar mavjud."""
    kirish += "\n\n<i>Kamchiliklar uchun avvaldan uzur!</i>"

    update.message.reply_html(text=kirish, reply_markup=reply_markup)
    
    # Foydalanuvchilar haqidagi ma'lumotni bazaga saqlab boradi
    foydalanuvchi_saqla(update, context)
    


def main():
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    TOKEN = "1910700952:AAGRQyfXiVfasDhHIBqQB49McKAcjmK1nAw"

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex(asosiy_tugma), funk2))
    dispatcher.add_handler(MessageHandler(Filters.regex(kitob_haqida), funk3))
    dispatcher.add_handler(CommandHandler("admin", admin_sozlamalari))
    dispatcher.add_handler(CallbackQueryHandler(funk1))


    # Start the Bot
    updater.start_polling()

    # updater.start_webhook(listen="0.0.0.0",
    #                   port=PORT,
    #                   url_path=TOKEN,
    #                   webhook_url="https://quron-python-telegram-bot.herokuapp.com/" + TOKEN)


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()