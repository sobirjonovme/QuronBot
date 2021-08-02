

import logging

from telegram.constants import PARSEMODE_HTML


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
import os

PORT = int(os.environ.get('PORT', '8443'))



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)



# Stages
FIRST, SECOND = 'bir', 'ikki'
# Callback data
ONE, TWO, THREE, FOUR = range(4)

asosiy_tugma = "Suralar ro'yxati"

main_buttons = ReplyKeyboardMarkup([
	[asosiy_tugma],
	],
    resize_keyboard=True
)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    username = user.full_name
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton(asosiy_tugma, callback_data=asosiy_tugma),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard

    update.message.reply_html(f"<b>Assalom-u alaykum, <i> {username}</i> </b>\n\n\
🤖 Men orqali <b>Qur'oni Karim suralari</b>ni topishingiz mumkin 🌐", reply_markup=main_buttons)

    update.message.reply_html("<b>Qur'oni Karim</b>", reply_markup=reply_markup)

    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST



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
    print("royxat2")
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
    print(f"{a1}-surani tanladingiz")
    # a1 - sura raqami
    # a2 - sahifa raqami
    a1, a2 = int(a1), int(a2)
    soni = oyat_soni(a1)
    if a2 == soni//5:
        lst = list(range(a2*5+1,soni+1))
    else:
        lst = list(range(a2*5+1, a2*5+6))
    matn = f"<b><i>{suralar_raqami[str(a1)]}</i>   surasi oyatlari</b>          {lst[0]}-{lst[-1]}   <i>{soni} dan</i>\n\n" 
    print("\n"*4)
    print("1")
    print(lst)
    print("\n"*4)
    for d in lst:
        matn += f"<b>{d}.</b>  {oyat_top(a1, d)}\n\n"
    
    return matn




    
def funk1(update: Update, context: CallbackContext):
    print('\n'*4)
    print('funk1')
    ana = context.bot.send_message(chat_id=update.effective_message.chat_id,
            text="Iltimos biroz kuting...")
    print(ana)
    print('\n'*4)

    query = update.callback_query
    query.answer()

    data = update.callback_query.data
    if data == asosiy_tugma:
        inlinekeyboard = royxat_tuz(0)
        matn = suralar_chiqar(0)
        # query.edit_message_text(text="<b>asdas</b>", parse_mode=PARSEMODE_HTML)
        query.edit_message_text(text=matn, parse_mode=PARSEMODE_HTML, reply_markup=inlinekeyboard)

    if 'sura' in data:
        print("sura borligini topdi")
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
            matn = oyat_chiqar(sura_r, 0)
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
                pass
            if p != None:
                inlinekeyboard = royxat_tuz2(sura_r, p)
                matn = oyat_chiqar(sura_r, p)
                query.edit_message_text(text=matn,
                                parse_mode=PARSEMODE_HTML, reply_markup=inlinekeyboard)

    context.bot.delete_message(chat_id=update.effective_message.chat_id,
                message_id=ana.message_id)


def funk2(update: Update, context: CallbackContext):
    inlinekeyboard = royxat_tuz(0)
    matn = suralar_chiqar(0)
    update.message.reply_text(text=matn, parse_mode=PARSEMODE_HTML, reply_markup=inlinekeyboard)     


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    TOKEN = "1898387737:AAEhjGQr0LhHZeM4d4u5LYLPi_mxG9aOy6E"
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex(asosiy_tugma), funk2))
    dispatcher.add_handler(CallbackQueryHandler(funk1))


    # Start the Bot
    # updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url="https://quron-python-telegram-bot.herokuapp.com/" + TOKEN)


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except:
        print("Xatolik yuz berdi")