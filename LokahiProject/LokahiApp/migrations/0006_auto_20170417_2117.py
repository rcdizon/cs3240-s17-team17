# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 21:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LokahiApp', '0005_report_encrypted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textbox', models.TextField(max_length=10000)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='privacy',
            field=models.CharField(choices=[(b'Public', b'Public'), (b'Private', b'Private')], default=b'Public', max_length=10),
        ),
        migrations.AlterField(
            model_name='report',
            name='encrypted',
            field=models.CharField(choices=[(b'Yes', b'Yes'), (b'No', b'No')], default=b'No', max_length=4),
        ),
        migrations.AlterField(
            model_name='report',
            name='upload',
            field=models.FileField(blank=True, default=None, null=True, upload_to=b'media'),
        ),
    ]
