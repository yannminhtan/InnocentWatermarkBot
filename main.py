import os
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
import tempfile

BOT_TOKEN = os.getenv("BOT_TOKEN")"
WATERMARK_FILE = "Innocent.png"

async def add_watermark_photo(image_path):
    base = Image.open(image_path).convert("RGBA")
    watermark = Image.open(WATERMARK_FILE).convert("RGBA")
    w_ratio = base.width // 5
    watermark = watermark.resize((w_ratio, int(watermark.height * w_ratio / watermark.width)))
    position = (base.width - watermark.width - 10, base.height - watermark.height - 10)
    base.paste(watermark, position, watermark)
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    base.convert("RGB").save(output.name, "JPEG")
    return output.name

async def add_watermark_video(video_path):
    watermark = Image.open(WATERMARK_FILE)
    watermark_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    watermark.save(watermark_path.name)

    clip = VideoFileClip(video_path)
    logo = (ImageClip(watermark_path.name)
            .set_duration(clip.duration)
            .resize(height=50)
            .margin(right=8, bottom=8, opacity=0)
            .set_pos(("right", "bottom")))
    final = CompositeVideoClip([clip, logo])
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    final.write_videofile(output.name, codec="libx264", audio_codec="aac")
    return output.name

async def handle_media_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    media_group_id = update.message.media_group_id
    context.user_data.setdefault(media_group_id, [])
    context.user_data[media_group_id].append(update.message)

    if len(context.user_data[media_group_id]) >= 10 or update.message == context.user_data[media_group_id][-1]:
        messages = context.user_data.pop(media_group_id)
        media = []
        for msg in messages:
            if msg.photo:
                photo = msg.photo[-1]
                file = await context.bot.get_file(photo.file_id)
                file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
                await file.download_to_drive(file_path)
                wm_path = await add_watermark_photo(file_path)
                media.append(InputMediaPhoto(open(wm_path, "rb")))
            elif msg.video:
                file = await context.bot.get_file(msg.video.file_id)
                file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
                await file.download_to_drive(file_path)
                wm_path = await add_watermark_video(file_path)
                media.append(InputMediaVideo(open(wm_path, "rb")))

        if media:
            await update.message.reply_media_group(media=media)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & filters.MEDIA_GROUP, handle_media_group))
    app.run_polling()
