# Generated by Django 4.0.dev20210615210523 on 2021-06-15 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_alter_article_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='annotations',
            field=models.JSONField(blank=True, null=True),
        ),
    ]