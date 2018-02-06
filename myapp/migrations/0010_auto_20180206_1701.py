# Generated by Django 2.0.2 on 2018-02-06 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_updownfile_max_downloads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updownfile',
            name='expires_at',
            field=models.DateField(blank=True, null=True, verbose_name='Expiration date'),
        ),
        migrations.AlterField(
            model_name='updownfile',
            name='file',
            field=models.FileField(upload_to='uploaded_files/', verbose_name='Uploaded file'),
        ),
        migrations.AlterField(
            model_name='updownfile',
            name='slug',
            field=models.CharField(max_length=36, verbose_name='Secret URL Part'),
        ),
    ]