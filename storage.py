import os
import uuid
import json
from PIL import Image

# The folder where images and metadata will be saved locally
UPLOAD_FOLDER = 'uploaded_images'
METADATA_FOLDER = 'image_metadata'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(METADATA_FOLDER, exist_ok=True)


def save_image(image_file, ext):
    """
    Save an image and its metadata to the local filesystem.
    - image_file: the image file object
    - ext: the file extension
    """
    image_id = str(uuid.uuid4())
    image_path = os.path.join(UPLOAD_FOLDER, f"{image_id}.{ext}")

    # Save the image file
    with open(image_path, 'wb') as f:
        f.write(image_file.read())  # Read the file stream and save it

    # Save the metadata as a JSON file
    metadata = {
        "image_id": image_id,
        "original_extension": ext
    }
    metadata_path = os.path.join(METADATA_FOLDER, f"{image_id}.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)

    return image_id, image_path


def load_image(image_id):
    """
    Load an image from the local filesystem using its UUID.
    The original extension is determined from the metadata file.
    - image_id: The UUID of the image
    """
    # Load the metadata file to determine the original extension
    metadata_path = os.path.join(METADATA_FOLDER, f"{image_id}.json")
    if not os.path.exists(metadata_path):
        return None, None

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
        ext = metadata['original_extension']

    # Load the image using the original extension
    image_path = os.path.join(UPLOAD_FOLDER, f"{image_id}.{ext}")
    if os.path.exists(image_path):
        return Image.open(image_path), ext
    return None, None


def get_supported_extensions():
    """Return a list of supported image file extensions."""
    return ['png', 'jpeg', 'gif']
