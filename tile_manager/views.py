import math
import os

import requests
from PIL import Image
from django.conf import settings
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UploadedImage
from .utils import generate_tiles

# Главная страница с возможностью загрузки изображения
def home(request):
    # Получение загруженного изображения и дополнительных данных
    if request.method == 'POST':
        image = request.FILES.get('image')
        source = request.POST.get('source', '')

        # Отправка POST-запроса на эндпоинт загрузки изображения
        response = requests.post(
            request.build_absolute_uri(reverse('image-upload')),
            files={'image': image},
            data={'source': source},
        )

        # Проверяем, что изображение успешно сохранено
        uploaded_image = UploadedImage.objects.filter(image=image).last()
        if response.status_code == 202:
            return render(request, 'home.html', {"message": f"Изображение успешно загружено и доступно по адресу: ",
                                                 "link": f"http://127.0.0.1:8000/viewer/{response.json().get('id')}"})
        else:
            return render(request, 'home.html', {'error': 'Не удалось загрузить изображение.'})

    # Отображение страницы без загрузки изображения
    return render(request, 'home.html')

# Эндпоинт для загрузки изображений через API
class ImageUploadView(APIView):
    # Указываем парсеры для работы с формами и файлами
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Устанавливаем обработчик временных файлов
        request.upload_handlers = [TemporaryFileUploadHandler()]

        # Получаем файл изображения и источник, если он указан
        file_obj = request.FILES.get('image')
        source = request.data.get('source', '')
        if not file_obj:
            return Response({"error": "Изображение не предоставлено."}, status=400)

        # Создаем запись в базе данных для загруженного изображения
        uploaded_image = UploadedImage.objects.create(image=file_obj, source=source)

        # Асинхронная обработка изображения (генерация тайлов)
        self.process_image_async(uploaded_image.image.path, uploaded_image.id)

        # Возвращаем успешный ответ с ID изображения
        return Response({
            "message": f"Изображение успешно загружено!",
            "id": uploaded_image.id,
        }, status=202)

    def process_image_async(self, image_path, image_id):
        # Асинхронная обработка изображения через отдельный поток
        from threading import Thread
        output_dir = os.path.join(settings.MEDIA_ROOT, 'dzi', str(image_id))
        os.makedirs(output_dir, exist_ok=True) # Создаем директорию для тайлов

        # Запускаем генерацию тайлов в отдельном потоке
        thread = Thread(target=generate_tiles, args=(image_path, output_dir))
        thread.start()

# Эндпоинт для получения конкретного тайла изображения
class TileView(APIView):
    def get(self, request, image_id, level, x, y):
        # Формируем путь к тайлу на диске
        tile_path = os.path.join(
            settings.MEDIA_ROOT, 'dzi', str(image_id), f"level_{level}", f"{x}_{y}.png"
        )

        # Если тайл существует, возвращаем его в ответе
        if os.path.exists(tile_path):
            return FileResponse(open(tile_path, 'rb'), content_type='image/png')
        # Если тайл не найден, возвращаем 404
        raise Http404("Тайл не найден.")

# Функция для просмотра изображения с поддержкой зумирования
def image_viewer(request, image_id):
    # Получаем объект загруженного изображения по ID
    uploaded_image = get_object_or_404(UploadedImage, id=image_id)
    image_path = uploaded_image.image.path


    # Открываем изображение и получаем его размеры
    with Image.open(image_path) as img:
        image_width, image_height = img.size

    # Вычисляем максимальный уровень зума на основе размеров изображения
    max_zoom_level = int(math.ceil(math.log2(max(image_width, image_height) / 256)))

    # Передаем данные в шаблон для отображения
    context = {
        "image_id": image_id,
        "image_width": image_width,
        "image_height": image_height,
        "max_zoom_level": max_zoom_level,
    }
    return render(request, "viewer.html", context)
