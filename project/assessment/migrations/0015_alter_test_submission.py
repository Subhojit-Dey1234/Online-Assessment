# Generated by Django 4.0.3 on 2022-04-15 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0014_remove_student_test_student_attempts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='submission',
            field=models.ManyToManyField(blank=True, related_name='submission_field', to='assessment.attempts'),
        ),
    ]
