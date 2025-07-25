# Generated by Django 5.2.3 on 2025-07-15 07:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app1_media_manger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writer_created', models.DateTimeField(auto_now_add=True)),
                ('writer_updated', models.DateTimeField(auto_now=True)),
                ('writermedia', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='app5_writer', to='app1_media_manger.writermedia')),
            ],
        ),
        migrations.CreateModel(
            name='WriterCoreDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.CharField(max_length=20)),
                ('born_date', models.DateField()),
                ('death_date', models.DateField(blank=True, null=True)),
                ('spouses', models.JSONField(blank=True, default=list)),
                ('children', models.JSONField(blank=True, default=list)),
                ('relatives', models.JSONField(blank=True, default=list)),
                ('otherwork', models.JSONField(blank=True, default=list)),
                ('writer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='writer_core_detail', to='app5_writer.writer')),
            ],
        ),
    ]
