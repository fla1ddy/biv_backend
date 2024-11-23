import os
import math
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def generate_tiles(image_path, output_dir, tile_size=256):
    print(f"Генерация тайлов из: {image_path}")

    image = Image.open(image_path)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    width, height = image.size
    max_level = int(math.ceil(math.log2(max(width, height) / tile_size)))

    print(f"Размер изображения: {width}x{height}")
    if os.path.exists(output_dir) and len(os.listdir(output_dir)) > 0:
        print(f"Тайлы уже существуют в {output_dir}. Пропуск генерации.")
        return max_level

    print(f"Генерация тайлов для {max_level + 1} уровней")

    for level in range(max_level, -1, -1):
        scale = 2 ** (max_level - level)
        resized_image = image.resize(
            (width // scale, height // scale), Image.Resampling.LANCZOS
        )
        level_dir = os.path.join(output_dir, f"level_{level}")
        os.makedirs(level_dir, exist_ok=True)

        for x in range(0, resized_image.width, tile_size):
            for y in range(0, resized_image.height, tile_size):
                tile = resized_image.crop((x, y, x + tile_size, y + tile_size))
                tile.save(os.path.join(level_dir, f"{x}_{y}.jpg"))

    print(f"Генерация тайлов завершена для {image_path}")
    return max_level