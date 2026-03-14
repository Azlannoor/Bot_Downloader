import telebot
import yt_dlp
import os
from keep_alive import keep_alive # Memanggil trik anti-mati

BOT_TOKEN = '7983059034:AAGZpuIMF8wOhSmO4bAoOrvnAG_5KLON2ik'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Kirimkan link YouTube Shorts atau Instagram, saya akan mengunduhnya dalam kualitas HD.")

@bot.message_handler(func=lambda message: True)
def download_media(message):
    url = message.text
    if 'http' not in url:
        bot.reply_to(message, "Mohon kirimkan link yang valid.")
        return

    msg = bot.reply_to(message, "⏳ Sedang memproses... Mohon tunggu.")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'unduhan_%(id)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
            if not os.path.exists(file_name):
                file_name = file_name.rsplit('.', 1)[0] + '.mp4'

        bot.edit_message_text("✅ Mengirim ke chat...", chat_id=message.chat.id, message_id=msg.message_id)
        with open(file_name, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)
        os.remove(file_name)

    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id=message.chat.id, message_id=msg.message_id)

# Menjalankan server mini dan bot
keep_alive()
bot.infinity_polling()
