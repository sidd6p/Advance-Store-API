from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.library import images_helper
from app.library.strings import get_text
from app.schemas.image import ImageSchema

image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required()
    def post(self):

        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            image_path = images_helper.save_image(data["image"], folder=folder)
            basename = images_helper.get_basename(image_path)
            print(image_path)
            return {"message": get_text("IMAGE_UPLOADED").format(basename)}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = images_helper.get_extension(data["image"])
            return {
                "message": get_text("ILLEGA_IMAGE_EXTENSION").format(extension)
            }, 400
