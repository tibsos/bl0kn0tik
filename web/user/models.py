import os

from django.db import models as m

from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

from uuid import uuid4 as u4

from app.models import Notepad, Note

def upload_avatar(instance, filename):

    file_extension = filename.split('.')[-1]
    new_filename = f"{u4}.{file_extension}"

    return os.path.join('uploads/profile/avatar', new_filename)

class Profile(m.Model):

    user = m.OneToOneField(User, on_delete = m.CASCADE, related_name = 'profile')

    forgot_password_token = m.CharField(max_length = 100)

    premium = m.BooleanField(default = True)
    
    
    name = m.CharField(max_length = 199)
    
    initials = m.CharField(max_length = 3)
    
    avatar = m.ImageField(upload_to = upload_avatar, null = True)


    active_notepad = m.ForeignKey(Notepad, on_delete = m.DO_NOTHING, null = True)
    active_note = m.ForeignKey(Note, on_delete = m.DO_NOTHING, null = True)

    def __str__(self):
        
        return self.name

    class Meta:

        ordering = ['-name']

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        Profile.objects.create(user = instance)