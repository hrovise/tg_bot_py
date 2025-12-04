import io
import os
import logging
import textwrap

from dotenv import load_dotenv
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
load_dotenv()


# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Отправь картинку с подписью и можно выбрать цвет текста: '
        '"цвет=черный" или "цвет=белый". Например:\n\n'
        'цвет=белый Привет мир!'
    )


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.photo:
        await update.message.reply_text("Пожалуйста, отправь фото вместе с подписью.")
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_bytes = await file.download_as_bytearray()


    caption = update.message.caption or "Ваш текст!"
    color = (0, 0, 0)  # по умолчанию черный

    if caption.lower().startswith("цвет="):
        try:
            parts = caption.split(" ", 1)
            color_name = parts[0].split("=")[1].strip().lower()
            if color_name == "белый":
                color = (255, 255, 255)
            elif color_name == "черный":
                color = (0, 0, 0)

            caption = parts[1] if len(parts) > 1 else "Ваш текст!"
        except Exception:
            pass

    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)


    font_path= os.path.join("assets", "DejaVuSans.ttf")
    font = ImageFont.truetype(font_path, 55)


    img_width, img_height = image.size


    max_chars_per_line = 25
    lines = textwrap.wrap(caption, width=max_chars_per_line)
    if len(lines) > 2:
        lines = lines[:1] + [' '.join(lines[1:])]


    spacing = 10
    total_height = sum([draw.textbbox((0,0), line, font=font)[3] - draw.textbbox((0,0), line, font=font)[1] for line in lines]) + spacing * (len(lines)-1)


    y = img_height - total_height - 30


    for line in lines:
        text_bbox = draw.textbbox((0,0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = (img_width - text_width) / 2

        # Добавляем тень (если цвет текста черный — тень белая и наоборот)
        shadow_offset = 2
        shadow_color = (255, 255, 255) if color == (0,0,0) else (0,0,0)
        draw.text((text_x + shadow_offset, y + shadow_offset), line, font=font, fill=shadow_color)
        draw.text((text_x, y), line, font=font, fill=color)

        y += text_height + spacing


    output_stream = io.BytesIO()
    image.save(output_stream, format="PNG")
    output_stream.seek(0)

    await update.message.reply_photo(photo=InputFile(output_stream, filename="image_with_text.png"))



def main() -> None:
    # TOKEN = os.getenv("TOKEN")
    TOKEN = os.environ["TOKEN"]
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("✅ Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()