# Generated by Django 4.1.5 on 2023-05-15 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_friendrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_profile_picture.jpg', upload_to='profile_pictures'),
        ),
    ]