from io import BytesIO
from PIL import Image
import storage


def upload_image(file):
    """
    Handles image upload logic.
    - file: The image file object (must have a filename attribute)
    """
    ext = file.filename.split('.')[-1].lower()  # Get the file extension from the filename
    if ext not in storage.get_supported_extensions():
        raise ValueError("Unsupported image format")

    # Save the image and metadata using storage
    image_id, _ = storage.save_image(file, ext)
    return {"image_id": image_id, "extension": ext}


def retrieve_image(image_id, desired_format=None):
    """
    Handles image retrieval logic and optionally performs format conversion.
    - image_id: The unique identifier for the image
    - desired_format: Optionally convert the image to this format
    """
    image, original_ext = storage.load_image(image_id)

    if image is None:
        raise FileNotFoundError("Image not found")

    img_io = BytesIO()

    # Map 'jpg' to 'jpeg' for Pillow compatibility
    if desired_format and desired_format.lower() == 'jpg':
        desired_format = 'jpeg'

    # If format conversion is requested, convert the image
    if desired_format and desired_format != original_ext:
        if desired_format not in storage.get_supported_extensions():
            raise ValueError("Unsupported format for conversion")

        # Automatically convert RGBA to RGB for formats like JPEG that don't support alpha channels
        if desired_format == 'jpeg' and image.mode == 'RGBA':
            image = image.convert('RGB')

        # Convert the image to the desired format
        image.save(img_io, format=desired_format.upper())
        img_io.seek(0)
        return img_io, desired_format
    else:
        # No conversion needed, return the image in its original format
        image.save(img_io, format=original_ext.upper())
        img_io.seek(0)
        return img_io, original_ext
