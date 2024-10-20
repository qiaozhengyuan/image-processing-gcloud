import functions_framework
from flask import request, jsonify, send_file
import image_service


@functions_framework.http
def image(request):
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        try:
            result = image_service.upload_image(file)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    elif request.method == 'GET':
        image_id = request.args.get('image_id')
        format = request.args.get('format', 'png')  # Default to PNG if no format is specified

        try:
            img_io, img_format = image_service.retrieve_image(image_id, format)
            return send_file(img_io, mimetype=f'image/{img_format}')
        except FileNotFoundError:
            return jsonify({"error": "Image not found"}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    return jsonify({"error": "Method not allowed"}), 405
