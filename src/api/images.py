from fastapi import APIRouter, UploadFile

from fastapi import BackgroundTasks

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения"])

@router.post("")
def upload_image(file:UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)


