from django.core.validators import RegexValidator
from django.db import models


class Subject(models.Model):
    """This model includes details of Subjects"""
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)


class Teacher(models.Model):
    """This model have all the teacher properties"""
    phone_number_validation = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, validators=[phone_number_validation], null=True, blank=True)
    room_number = models.CharField(max_length=10, null=True, blank=True)
    subjects_taught = models.ManyToManyField('Subject', blank=True, related_name='teachers')
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", default="profile_pictures/placeholder-profile-image.jpeg")

