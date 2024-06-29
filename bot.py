from typing import Final
import mysql.connector
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import TOKEN


BOT_USERNAME = '@ppt_document_bot'
UPLOADS_DIR = 'uploads'  # Directory to store uploaded files

db = mysql.connector.connect(
    host="localhost",
    user="danya",
    password="9d10a11b",
    database="telegram_bot_db"
)
cursor = db.cursor()

def get_file_path(file_name: str) -> str:
    cursor.execute("SELECT file_path FROM files WHERE file_name=%s", (file_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None
async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name: str):
    file_path = get_file_path(file_name)
    
    if file_path and os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    else:
        await update.callback_query.message.reply_text(f'{file_name} file not found.')


async def capture_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Chat ID: {chat_id}')
    print(f'Chat ID: {chat_id}')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("PHP", callback_data='PHP')],
        [InlineKeyboardButton("Advanced programming", callback_data='advanced')],
        [InlineKeyboardButton("Computer Vision", callback_data='CV')],
        [InlineKeyboardButton("Computer Graphics", callback_data='CG')],
        [InlineKeyboardButton("Automata", callback_data='automata')],
        [InlineKeyboardButton("Operating System", callback_data='OS')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an option', reply_markup=reply_markup)

async def PHP(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update, context, 'PHP')
    
   

async def advanced(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update, context, 'advanced')



async def CV(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update, context, 'CV')


async def CG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update,context,'CG')

async def automata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update,context,'automata')

async def OS(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update,context,'OS')


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'PHP':
        await PHP(update, context)
    elif query.data == 'advanced':
        await advanced(update, context)
    elif query.data == 'CV':
        await CV(update, context)
    elif query.data == 'CG':
        await CG(update, context)
    elif query.data == 'automata':
        await automata(update, context)
    elif query.data == 'OS':
        await OS(update, context)

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hello there!'
    if 'how are you' in processed:
        return 'I am doing good'
    return 'I do not understand what you said..'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # Messages
    # app.add_handler(MessageHandler(filters.Text & ~filters.Command, handle_message, context_types=ContextTypes.DEFAULT_TYPE))  # Corrected filter usage
    app.add_handler(MessageHandler(filters.ALL, capture_chat_id))   # Corrected filter usage

    print('Polling...')
    app.run_polling(poll_interval=3)
