# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=999)),
                ('public', models.BooleanField(default=False)),
                ('duration', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('true', models.IntegerField()),
                ('predicted', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LabelType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marketer', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name=b'owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Raw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('sensor', models.CharField(max_length=99)),
                ('attention', models.CharField(max_length=10)),
                ('sigqual', models.CharField(max_length=10)),
                ('rawwave', models.CharField(max_length=4000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=999)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('content_start_sec', models.IntegerField()),
                ('content_end_sec', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('data', models.CharField(max_length=999)),
                ('session', models.ForeignKey(related_name=b'session_tags', to='data_store.Session')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('question', models.CharField(max_length=999)),
                ('answer', models.CharField(max_length=999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoContent',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='data_store.Content')),
                ('video_url', models.CharField(max_length=999)),
            ],
            options={
            },
            bases=('data_store.content',),
        ),
        migrations.CreateModel(
            name='VideoSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=999)),
                ('content', models.CharField(max_length=9999)),
                ('group', models.ForeignKey(related_name=b'video_series', to='data_store.ContentGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matching_email', models.CharField(max_length=999)),
                ('user', models.OneToOneField(related_name=b'viewer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tag',
            name='subject',
            field=models.ForeignKey(related_name=b'confusion_data', to='data_store.Viewer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='subject',
            field=models.ForeignKey(related_name=b'survey_answers', to='data_store.Viewer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='content',
            field=models.ForeignKey(related_name=b'sessions', to='data_store.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='viewers',
            field=models.ManyToManyField(related_name=b'sessions', to='data_store.Viewer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raw',
            name='subject',
            field=models.ForeignKey(related_name=b'raw_data', to='data_store.Viewer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='label',
            name='label_type',
            field=models.ForeignKey(related_name=b'labels', to='data_store.LabelType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='label',
            name='tag',
            field=models.ForeignKey(related_name=b'labels', to='data_store.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentlabel',
            name='content',
            field=models.ForeignKey(related_name=b'labels', to='data_store.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentlabel',
            name='label_type',
            field=models.ForeignKey(related_name=b'content_labels', to='data_store.LabelType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentgroup',
            name='owners',
            field=models.ManyToManyField(related_name=b'content_groups', to='data_store.Owner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentgroup',
            name='viewers',
            field=models.ManyToManyField(related_name=b'content_groups', to='data_store.Viewer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='group',
            field=models.ForeignKey(related_name=b'content', to='data_store.ContentGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='invited_viewers',
            field=models.ManyToManyField(related_name=b'invited_content', to='data_store.Viewer'),
            preserve_default=True,
        ),
    ]
