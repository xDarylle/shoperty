from flask import request, send_file
from app import app
from app.Components.image_handler import get_img
from app.Components.response import Response

@app.route('/api/v1/images/<image>', methods=['GET'])
def image(image):
    if request.method == 'GET':
        try:
            img = get_img(image)
        except FileNotFoundError:
            return Response(
                status=404,
            )
        
        return send_file(
            img,
            mimetype='image/png'
        )