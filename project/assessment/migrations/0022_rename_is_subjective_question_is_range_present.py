# Generated by Django 4.0.3 on 2022-04-18 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0021_rename_is_subjected_question_is_subjective_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='is_subjective',
            new_name='is_range_present',
        ),
    ]
