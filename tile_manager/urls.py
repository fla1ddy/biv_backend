from django.urls import path
from .views import ImageUploadView, TileView, image_viewer

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('tiles/<int:image_id>/<int:level>/<int:x>_<int:y>.png', TileView.as_view(), name='tile-view'),
    path('viewer/<int:image_id>/', image_viewer, name='image-viewer'),
]
