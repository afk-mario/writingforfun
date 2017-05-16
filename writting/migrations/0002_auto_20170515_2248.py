# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-15 22:48
from __future__ import unicode_literals

import adminsortable.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('writting', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['order', 'slug']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['order', 'slug']},
        ),
        migrations.AddField(
            model_name='entry',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='post',
            name='entry',
            field=adminsortable.fields.SortableForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='writting.Entry'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]