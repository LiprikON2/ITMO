# Generated by Django 3.1.1 on 2020-09-17 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_auto_20200914_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permalink',
            fields=[
                ('key', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('refersTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.note', unique=True)),
            ],
        ),
    ]