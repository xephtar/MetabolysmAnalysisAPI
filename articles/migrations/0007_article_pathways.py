# Generated by Django 3.1.4 on 2021-02-09 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20210210_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='pathways',
            field=models.ManyToManyField(to='articles.Pathway'),
        ),
    ]
