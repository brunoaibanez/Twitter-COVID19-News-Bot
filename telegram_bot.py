"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from datetime import datetime, timedelta
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from database_connection import MongoDB
import keywords, get_google_image
import json

with open('properties_user', 'r') as f:
 data_user = json.load(f)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, SEND_INFO_TO_VALIDATE, IS_IT_TRUE, WHY_TRUST_YOU = range(6)

reply_keyboard = [['Información última hora', 'Información tiempo real'],
                  ['Validar/Desmentir información'],
                  ['Nada más']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text(
        "Hola! Somos una asociación sin ánimo de lucro que vela por la información verídica en épocas de FakeNews en Twitter y cadenas de mensajes",
        reply_markup=markup)

    return CHOOSING


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

    return TYPING_REPLY


def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{} You can tell me more, or change your opinion"
                              " on something.".format(facts_to_str(user_data)),
                              reply_markup=markup)

    return CHOOSING


def get_tweet(dict_tweet):
    tweet = ""
    tweet += "Tweet por @%s\n" % (dict_tweet["user"]["name"])
    tweet += "%s\n" % (dict_tweet["text"])
    try:
        tweet += "%s" % (dict_tweet["entities"]["urls"][0]["url"])
    except:
        pass

    keys = keywords.get_keywords(dict_tweet["text"])
    # keys = " ".join(keys)
    # url_image = list(get_google_image.get_scrapped_image(keys))[0]
    url_image = ""
    return tweet, url_image


def get_information(update, context):
    mongo = MongoDB()
    max_range_time = datetime.utcnow()-timedelta(minutes=5)
    tweets = mongo.get_popular_tweets(max_range_time)
    # print('tweets', len(tweets))
    for num_tweet in range(len(tweets)):
        if num_tweet > 10:
            break
        # print(str(num_tweet) + str(tweets[num_tweet]))
        tweet, url_image = get_tweet(tweets[num_tweet])
        # chat_id = update.message.chat_id
        # context.bot.send_photo(chat_id=chat_id, photo=url_image, caption=tweet)
        update.message.reply_text(tweet)
    return CHOOSING


def get_information_live(update, context):
    mongo = MongoDB()
    max_range_time = datetime.utcnow()-timedelta(minutes=1)
    tweets = mongo.get_popular_tweets(max_range_time)
    # print('tweets', len(tweets))
    for num_tweet in range(len(tweets)):
        if num_tweet > 20:
            break
        # print(str(num_tweet) + str(tweets[num_tweet]))
        tweet, url_image = get_tweet(tweets[num_tweet])
        # chat_id = update.message.chat_id
        # context.bot.send_photo(chat_id=chat_id, photo=url_image, caption=tweet)
        update.message.reply_text(tweet)
    return CHOOSING


def get_text_to_validate(update, context):
    text = update.message.text
    user_data = context.user_data
    name = update.message.from_user.name
    if user_data["true_or_false"] == True:
        if "validated" not in user_data:
            user_data["validated"] = []
        user_data["validated"].append(update.message.text)
    else:
        if "denied" not in user_data:
            user_data["denied"] = []
        user_data["denied"].append(update.message.text)

    if "who_it_is" not in user_data:
        update.message.reply_text(
            '%s, dínos quien eres para así poder tener en cuenta tu información. Por ejemplo: "Doctor en el Hospital Vall Hebron, especializado en Epidemiologia"' % (
                name))
        user_data["name"] = name
        return WHY_TRUST_YOU

    update.message.reply_text("Esta información ha sido añadida al algoritmo. Gracias!".format(facts_to_str(user_data)),
                              reply_markup=markup)
    return CHOOSING


def is_true_or_false(update, context):
    text = update.message.text
    user_data = context.user_data
    if text == "Validar":
        user_data["true_or_false"] = True
    elif text == "Desmentir":
        user_data["true_or_false"] = False
    else:
        update.message.reply_text('Escribe "Validar" o "Desmentir"')
        return IS_IT_TRUE

    update.message.reply_text(
        "Envíanos un link que hayas recibido, una cadena de mensajes o un tweet y lo tendremos en cuenta en nuestro algoritmo")
    return SEND_INFO_TO_VALIDATE


def who_you_are(update, context):
    text = update.message.text
    user_data = context.user_data
    user_data["who_it_is"] = text

    update.message.reply_text(
        "Gracias por tu información! Qué quieres hacer ahora? Clica sobre el icono para volver a ver las opciones disponibles")

    return CHOOSING


def validate_information(update, context):
    update.message.reply_text('Quieres validar o desmentir una información? Escribe "Validar" o "Desmentir"')
    return IS_IT_TRUE


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def done(update, context):
    user_data = context.user_data
    if "name" in user_data:
        output = "%s - %s, gracias por tu aportación\n" % (user_data["name"], user_data["who_it_is"])
        if "validated" in user_data:
            output += "Información validada:\n"
            for link in user_data["validated"]:
                output += link + "\n"
        if "denied" in user_data:
            output += "Información desmentida:\n"
            for link in user_data["denied"]:
                output += link + "\n"
        output += "Hasta la próxima!"

        update.message.reply_text(output)

    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def run_telegram():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(data_user["telegram_key"], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^Información última hora$'),
                                      get_information),
                       MessageHandler(Filters.regex('^Validar/Desmentir información$'),
                                      validate_information),
                       MessageHandler(Filters.regex('^Información tiempo real$'),
                                      get_information_live)
                       ],

            SEND_INFO_TO_VALIDATE: [MessageHandler(Filters.text,
                                                   get_text_to_validate)
                                    ],

            IS_IT_TRUE: [MessageHandler(Filters.regex('^Validar|Desmentir$'),
                                        is_true_or_false)],

            WHY_TRUST_YOU: [MessageHandler(Filters.text,
                                           who_you_are)
                            ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice)
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information),
                           ],

        },

        fallbacks=[MessageHandler(Filters.regex('^Nada más$'), done)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    run_telegram()
