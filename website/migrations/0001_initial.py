# Generated by Django 2.0 on 2017-12-16 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]