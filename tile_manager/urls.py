from django.urls import path
from .views import ImageUploadView, TileView, image_viewer, home

urlpatterns = [
    path('', home, name='home'), # Главная страница
    path('upload/', ImageUploadView.as_view(), name='image-upload'), # API endpoint для загрузки изображений
    path('tiles/<int:image_id>/<int:level>/<int:x>_<int:y>.png',
         TileView.as_view(), name='tile-view'), # API endpoint для получения тайлов
    path('viewer/<int:image_id>/', image_viewer, name='image-viewer'), # Путь к странице просмотра изображения
]
