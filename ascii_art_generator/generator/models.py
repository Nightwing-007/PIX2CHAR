from django.db import models
from django.contrib.auth.models import User
import os
import uuid

def get_upload_path(instance, filename):
    """Generate unique file path for uploaded images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)

class AsciiArt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default="Untitled")
    original_image = models.ImageField(upload_to=get_upload_path)
    ascii_result = models.TextField()
    width = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title or "ASCII Art"
