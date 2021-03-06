# Generated by Django 2.2.1 on 2019-05-21 11:38

import apps.user.models
import apps.user.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='email address')),
                ('username', models.CharField(error_messages={'unique': 'User with this username already exists.'}, help_text='Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.+-]+$'), 'Enter a valid username.', 'invalid')], verbose_name='username')),
                ('full_name', models.CharField(max_length=60, verbose_name='full name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('photo', models.FileField(blank=True, upload_to=apps.user.utils.UploadDir('photo'))),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='address')),
                ('phone', models.CharField(max_length=255, null=True, verbose_name='phone')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.user.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('primary_picture', models.ImageField(upload_to=apps.user.utils.UploadDir('product_images'))),
            ],
        ),
        migrations.CreateModel(
            name='TaskRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_label', models.CharField(max_length=30, verbose_name='task label')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('terminated_at', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'ordering': ('-started_at',),
            },
        ),
        migrations.CreateModel(
            name='Trending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrendingProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('trending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Trending')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-score',),
            },
        ),
        migrations.CreateModel(
            name='TrendingHashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Hashtag')),
                ('trending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Trending')),
            ],
            options={
                'ordering': ('-score',),
            },
        ),
        migrations.AddField(
            model_name='trending',
            name='hashtags',
            field=models.ManyToManyField(through='user.TrendingHashtag', to='user.Hashtag'),
        ),
        migrations.AddField(
            model_name='trending',
            name='profiles',
            field=models.ManyToManyField(through='user.TrendingProfile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProductPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to=apps.user.utils.UploadDir('product_images'))),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='user.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='following', through='user.Follow', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
