import os
import traceback

from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
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
            return {"message": get_text("IMAGE_UPLOADED").format(basename)}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = images_helper.get_extension(data["image"])
            return {
                "message": get_text("ILLEGA_IMAGE_EXTENSION").format(extension)
            }, 400


class Image(Resource):
    @jwt_required()
    def get(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not images_helper.is_filename_safe(filename):
            return {"messgae", get_text("NOT_A_FILE")}, 401

        try:
            return send_file(images_helper.get_path(filename, folder))
        except FileNotFoundError:
            return {"message": get_text("FILE_NOT_FOUND").format(filename)}

    @jwt_required()
    def delete(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not images_helper.is_filename_safe(filename):
            return {"messgae", get_text("NOT_A_FILE")}, 401

        try:
            os.remove(
                os.path.join(
                    os.getcwd(), "app", images_helper.get_path(filename, folder)
                )
            )
            return {"message": get_text("DELETED")}, 200
        except FileNotFoundError:
            return {"message": get_text("FILE_NOT_FOUND").format(filename)}
