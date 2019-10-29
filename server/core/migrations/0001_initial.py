# Generated by Django 2.2.6 on 2019-10-25 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_id', models.CharField(max_length=12)),
                ('error', models.TextField(blank=True, null=True)),
                ('download_path', models.CharField(max_length=250)),
                ('subset', models.CharField(blank=True, max_length=12, null=True)),
                ('url', models.CharField(blank=True, max_length=250, null=True)),
                ('label', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]