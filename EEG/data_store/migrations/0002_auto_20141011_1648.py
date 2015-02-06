# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessiontag',
            name='session',
            field=models.ForeignKey(related_name=b'session_tags', to='data_store.Session', null=True),
        ),
    ]
