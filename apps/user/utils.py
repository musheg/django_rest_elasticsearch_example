import os
import uuid

from django.utils.deconstruct import deconstructible


@deconstructible
class UploadDir:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        return "%s/%s%s" % (self.path, uuid.uuid4(), os.path.splitext(filename)[1])
