# Generated by Django 4.0.3 on 2022-04-13 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0002_remove_test_questions_test_questions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='questions',
        ),
        migrations.AddField(
            model_name='test',
            name='questions',
            field=models.ManyToManyField(related_name='question', to='assessment.question'),
        ),
    ]