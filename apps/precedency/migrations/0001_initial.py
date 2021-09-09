# Generated by Django 3.2.5 on 2021-09-09 19:47

from django.conf import settings
import django.contrib.postgres.fields.citext
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Precedence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', django.contrib.postgres.fields.citext.CICharField(max_length=65, unique=True, verbose_name='title')),
            ],
            options={
                'verbose_name': 'Precedency',
                'verbose_name_plural': 'Precedence',
            },
        ),
        migrations.CreateModel(
            name='UsersPrecedency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('attitude', models.PositiveSmallIntegerField(choices=[(1, 'Negative'), (2, 'Positive')], db_index=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)], verbose_name='attitude')),
                ('importance', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='importance')),
                ('precedency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='precedency.precedence', verbose_name='precedency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Users precedency',
                'verbose_name_plural': 'Users precedence',
                'unique_together': {('precedency', 'user')},
            },
        ),
    ]
