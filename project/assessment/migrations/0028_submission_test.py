# Generated by Django 4.0.6 on 2022-07-14 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0027_submission_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test', to='assessment.test'),
        ),
    ]