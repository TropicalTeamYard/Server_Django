# Generated by Django 2.2.3 on 2019-07-15 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tokens',
        ),
        migrations.AddField(
            model_name='user',
            name='exp',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='extras',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='tags',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'normal'), (1, 'admin'), (2, 'superadmin')], default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserBinding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('uid', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('state', models.PositiveSmallIntegerField(choices=[(0, 'success'), (1, 'fail')], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bindings', to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('software', models.CharField(max_length=32)),
                ('access_ip', models.CharField(max_length=32)),
                ('access_uid', models.CharField(max_length=64)),
                ('device_type', models.PositiveSmallIntegerField(choices=[(0, 'mobile'), (1, 'pc'), (2, 'web'), (3, 'pad')], default=0)),
                ('access_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='user.User')),
            ],
        ),
    ]
