"""
Tools for generating images and thumbnails
"""
import os
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from config import UPLOADS_FOLDER, CACHE_FOLDER


def generate_thumbnail(file_path, resolution, ext=None):
    file_name = os.path.basename(file_path)
    file_name, file_ext = secure_filename(file_name).rsplit(".")
    if not ext:
        ext = file_ext.strip(".")

    if ext.lower() == "jpg":
        ext = "jpeg"

    if resolution in ["prev", "preview"]:
        res_x, res_y = (1920, 1080)
    elif resolution in ["thumb", "thumbnail"]:
        res_x, res_y = (300, 300)
    elif resolution in ["pfp", "profile"]:
        res_x, res_y = (150, 150)
    elif resolution in ["icon", "favicon"]:
        res_x, res_y = (30, 30)
    else:
        return None

    if os.path.exists(os.path.join(CACHE_FOLDER, f"{file_name}_{res_x}x{res_y}.{ext}")):
        return os.path.join(CACHE_FOLDER, f"{file_name}_{res_x}x{res_y}.{ext}")

    if not os.path.exists(os.path.join(UPLOADS_FOLDER, file_path)):
        return None

    image = Image.open(os.path.join(UPLOADS_FOLDER, file_path))
    image_icc = image.info.get("icc_profile")
    img_x, img_y = image.size

    image = ImageOps.exif_transpose(image)
    image.thumbnail((min(img_x, int(res_x)), min(img_y, int(res_y))))

    try:
        image.save(
            os.path.join(CACHE_FOLDER, f"{file_name}_{res_x}x{res_y}.{ext}"),
            icc_profile=image_icc,
        )
    except OSError:
        image = image.convert("RGB")
        image.save(
            os.path.join(CACHE_FOLDER, f"{file_name}_{res_x}x{res_y}.{ext}"),
            icc_profile=image_icc,
        )

    image.close()

    return os.path.join(CACHE_FOLDER, f"{file_name}_{res_x}x{res_y}.{ext}")