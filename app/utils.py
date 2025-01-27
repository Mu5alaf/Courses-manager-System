import os

def image_upload(instance, filename):
    _, extension = os.path.splitext(filename)
    extension = extension.lstrip(".").lower()
    return f"course/images/{instance.id}.{extension}"

def video_upload(instance, filename):
    _, extension = os.path.splitext(filename)
    extension = extension.lstrip(".").lower()
    return f"course/videos/{instance.id}.{extension}"