# Generated by Django 3.2.16 on 2024-09-02 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_alter_follow_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('following', 'user'), name='unique_following'),
        ),
    ]
