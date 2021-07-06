# Generated by Django 4.0.dev20210616072752 on 2021-06-22 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0018_remove_pathwaydiseaserelation_textblob_score_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='pathwaydiseaserelation',
            name='pathway_dis_pathway_8a0a63_idx',
        ),
        migrations.AddField(
            model_name='pathwaydiseaserelation',
            name='sentence',
            field=models.CharField(db_index=True, max_length=1000, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='pathwaydiseaserelation',
            unique_together={('pathway_name', 'disease_name', 'article_id', 'sentence')},
        ),
        migrations.AlterIndexTogether(
            name='pathwaydiseaserelation',
            index_together={('pathway_name', 'disease_name', 'article_id', 'sentence')},
        ),
        migrations.AddIndex(
            model_name='pathwaydiseaserelation',
            index=models.Index(fields=['pathway_name', 'disease_name', 'article_id', 'sentence'], name='pathway_dis_pathway_ed181c_idx'),
        ),
    ]
