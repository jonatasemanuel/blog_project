# Generated by Django 2.2.3 on 2023-01-30 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_post', models.CharField(max_length=255)),
                ('date_post', models.DateTimeField(default=django.utils.timezone.now)),
                ('content_post', models.TextField()),
                ('excerpt_post', models.TextField()),
                ('image_post', models.ImageField(blank=True, null=True, upload_to='post_img/%Y/%m/%D')),
                ('published_post', models.BooleanField(default=False)),
                ('author_post', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('categorie_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='categories.Categorie')),
            ],
        ),
    ]
