import os
import cloudinary
import cloudinary.uploader
from PIL import Image
from io import BytesIO

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_image(file, resize_to=(800, 600)):
    # Resize image using Pillow
    img = Image.open(file)
    img = img.convert("RGB")
    img.thumbnail(resize_to)
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    # Upload to Cloudinary
    result = cloudinary.uploader.upload(buffer, folder="spacer/spaces")
    return result.get("secure_url")