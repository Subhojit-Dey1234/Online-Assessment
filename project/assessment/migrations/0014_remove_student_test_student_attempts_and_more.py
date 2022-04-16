# Generated by Django 4.0.3 on 2022-04-15 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0013_student_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='test',
        ),
        migrations.AddField(
            model_name='student',
            name='attempts',
            field=models.ManyToManyField(blank=True, related_name='test_field', to='assessment.attempts'),
        ),
        migrations.AddField(
            model_name='test',
            name='marks_obtained',
            field=models.IntegerField(default=0),
        ),
    ]
