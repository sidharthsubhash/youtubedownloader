from telegram.ext import Updater, MessageHandler, Filters
import yt_dlp
import os
import imghdr

TOKEN = "7953602481:AAH2Bj97OEJfGWAmgWDRBhAvcbNV0ATT6IY"

def download_video(url):
    ydl_opts = {
        'format': 'best[height<=480]',   # limit to 480p max
        'outtmpl': 'video.%(ext)s',
        'socket_timeout': 30,            # 30 sec timeout
        'retries': 5                     # retry 5 times if it fails
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
def handle_message(update, context):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        update.message.reply_text("Downloading video, please wait ⏳...")
        try:
            filepath = download_video(url)
            with open(filepath, 'rb') as video:
                update.message.reply_video(video)
            os.remove(filepath)  # clean up after sending
        except Exception as e:
            update.message.reply_text(f"Error: {e}")
    else:
        update.message.reply_text("Send me a YouTube link 🎥")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

