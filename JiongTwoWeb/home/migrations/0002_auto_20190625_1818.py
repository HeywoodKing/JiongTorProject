# Generated by Django 2.2.2 on 2019-06-25 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jtarticle',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jtarticle',
            name='cover_image_url',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='article/%Y/%m', verbose_name='封面图片'),
        ),
    ]