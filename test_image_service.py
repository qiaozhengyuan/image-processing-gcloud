import unittest
import os
from io import BytesIO
from PIL import Image
import image_service
import storage


class TestImageServiceFullFlow(unittest.TestCase):

    def setUp(self):
        """Create the uploaded_images folder if it doesn't exist for testing."""
        if not os.path.exists(storage.UPLOAD_FOLDER):
            os.makedirs(storage.UPLOAD_FOLDER)

    def tearDown(self):
        """Remove all files from the uploaded_images folder after each test."""
        for file in os.listdir(storage.UPLOAD_FOLDER):
            file_path = os.path.join(storage.UPLOAD_FOLDER, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)  # Delete the file
            except Exception as e:
                print(f"Error cleaning up file {file}: {e}")

    def create_test_image(self, format='PNG'):
        """Helper function to create a simple in-memory image for testing."""
        img = Image.new('RGB', (60, 30), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format=format)
        img_bytes.seek(0)
        return img_bytes

    def test_full_flow_upload_image(self):
        """Test the full flow of uploading an image and checking it was saved to disk."""
        test_file = self.create_test_image()

        # Simulate a file with a filename, matching what Flask would provide
        test_file.filename = 'test_image.png'

        # Call the image_service to upload the image
        result = image_service.upload_image(test_file)

        # Check that the image file is saved on disk
        image_id = result['image_id']
        ext = result['extension']
        saved_file_path = os.path.join(storage.UPLOAD_FOLDER, f"{image_id}.{ext}")

        # Assert the image file was saved correctly
        self.assertTrue(os.path.exists(saved_file_path), f"File not found: {saved_file_path}")

    def test_full_flow_retrieve_image(self):
        """Test the full flow of uploading and retrieving an image from disk."""
        # First, upload an image
        test_file = self.create_test_image()

        # Simulate a file with a filename, matching what Flask would provide
        test_file.filename = 'test_image.png'

        # Upload the image
        result = image_service.upload_image(test_file)
        image_id = result['image_id']

        # Now retrieve the same image
        img_io, ext = image_service.retrieve_image(image_id)

        # Assert that the retrieved image matches the original one
        retrieved_image = Image.open(img_io)
        self.assertEqual(retrieved_image.size, (60, 30))
        self.assertEqual(ext, 'png')

    def test_full_flow_image_format_conversion(self):
        """Test the full flow of uploading an image and converting it to a different format."""
        # Upload an image as PNG
        test_file = self.create_test_image('PNG')

        # Simulate a file with a filename, matching what Flask would provide
        test_file.filename = 'test_image.png'

        result = image_service.upload_image(test_file)
        image_id = result['image_id']

        # Retrieve the image as JPEG
        img_io, ext = image_service.retrieve_image(image_id, desired_format='jpeg')

        # Assert the converted image is in JPEG format
        self.assertEqual(ext, 'jpeg')
        self.assertEqual(Image.open(img_io).format, 'JPEG')


if __name__ == '__main__':
    unittest.main()
