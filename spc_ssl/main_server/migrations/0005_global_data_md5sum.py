# Generated by Django 2.1.2 on 2018-11-21 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_server', '0004_auto_20181008_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='global_data',
            name='md5sum',
            field=models.CharField(default='NULL', max_length=50),
            preserve_default=False,
        ),
    ]
