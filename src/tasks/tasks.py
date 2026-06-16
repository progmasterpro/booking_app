import asyncio
import os
from time import sleep
from PIL import Image
import logging

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("I'm Crazy")

@celery_instance.task
def resize_image(image_path: str):
    logging.debug("")
    sizes = [1000, 500, 200]
    output_folder = 'src/static/images'

    # Открываем изображение
    img = Image.open(image_path)

    # Получаем имя файла и его расширение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"

        # Полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)

        # Сохраняем изображение
        img_resized.save(output_path)

    logging.info(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")


async def get_booking_with_today_chakin_halper():
    print("Я запускаюсь")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.booking.get_booking_with_today_chakin()
        logging.debug(f"{bookings=}")


@celery_instance.task(name="booking_today_checking")
def send_email_to_users_with_today_checking():
    asyncio.run(get_booking_with_today_chakin_halper())