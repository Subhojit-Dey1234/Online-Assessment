# Generated by Django 4.0.6 on 2022-07-24 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0030_student_discipline_student_programme'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='city',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='state',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='city',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='state',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]