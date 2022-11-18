import os

from django.db import models as m

from django.contrib.auth.models import User

from uuid import uuid4 as u4

class Notepad(m.Model):

    uid = m.UUIDField(default = u4)

    creator = m.ForeignKey(User, on_delete = m.CASCADE)

    title = m.CharField(max_length = 100)

    color = m.CharField(max_length = 10)

    notes = m.ManyToManyField('Note', blank = True)

    updated_at = m.DateTimeField(auto_now = True)
    created_at = m.DateTimeField(auto_now_add = True)

    def __str__(self):

        if self.notes:

            return f"{self.creator.username} notepad with {self.notes.count()} notes"

        else: 

            return f"{self.creator.username} notepad with 0 notes"

class Note(m.Model):

    uid = m.UUIDField(default = u4)

    creator = m.ForeignKey(User, on_delete = m.CASCADE)

    active = m.BooleanField(default = True)

    pinned = m.BooleanField(default = False)

    title = m.CharField(max_length = 300, blank = True)
    content = m.TextField(max_length = 1000000, blank = True)
    images = m.ManyToManyField('Image', blank = True)

    updated_at = m.DateTimeField(auto_now = True)
    created_at = m.DateTimeField(auto_now_add = True)

    def __str__(self):

        if self.title:

            return f"{self.creator.username}: '{self.title}'"

        else:

            return f"Unnamed by {self.creator.username}"

def upload_image(instance, filename):

    file_extension = filename.split('.')[-1]
    new_filename = f"{u4}.{file_extension}"

    return os.path.join('uploads/note/images', new_filename)


class Image(m.Model):

    uid = m.UUIDField(default = u4)

    file = m.ImageField(upload_to = upload_image)

    uploaded_at = m.DateTimeField(auto_now_add = True)

    class Meta:

        ordering = ['-uploaded_at']