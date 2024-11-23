from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os
from .models import UploadedImage
from .utils import generate_tiles
from PIL import Image

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.FILES.get('image')
        source = request.data.get('source', '')
        if not file_obj:
            return Response({"error": "Изображение не предоставлено."}, status=400)

        uploaded_image = UploadedImage.objects.create(image=file_obj, source=source)
        image_path = uploaded_image.image.path
        output_dir = os.path.join(settings.MEDIA_ROOT, 'dzi', str(uploaded_image.id))
        os.makedirs(output_dir, exist_ok=True)

        generate_tiles(image_path, output_dir)

        return Response({"message": "Изображение загружено и тайлы сгенерированы."})

class TileView(APIView):
    def get(self, request, image_id, level, x, y):
        tile_path = os.path.join(
            settings.MEDIA_ROOT, 'dzi', str(image_id), f"level_{level}", f"{x}_{y}.png"
        )

        if os.path.exists(tile_path):
            return FileResponse(open(tile_path, 'rb'), content_type='image/png')
        raise Http404("Тайл не найден.")

def image_viewer(request, image_id):
    uploaded_image = get_object_or_404(UploadedImage, id=image_id)
    image_path = uploaded_image.image.path

    with Image.open(image_path) as img:
        image_width, image_height = img.size

    output_dir = os.path.join(settings.MEDIA_ROOT, 'dzi', str(image_id))
    max_zoom_level = generate_tiles(image_path, output_dir)

    context = {
        "image_id": image_id,
        "image_width": image_width,
        "image_height": image_height,
        "max_zoom_level": max_zoom_level,
    }
    return render(request, "viewer.html", context)
