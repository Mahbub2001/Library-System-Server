# Generated by Django 5.1 on 2024-08-24 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_review_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
