# Generated by Django 2.2 on 2023-12-13 20:39
from typing import List
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies: List[str] = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('address_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'category',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('datetime_taken', models.DateTimeField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'reading',
                'ordering': ['-datetime_taken'],
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('amber_high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amber_low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=50)),
                ('red_high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('red_low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('seconds_valid', models.IntegerField()),
            ],
            options={
                'db_table': 'source',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='SourceShare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('address_id', models.IntegerField()),
                ('end_date', models.DateTimeField(null=True)),
                ('start_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'source_share',
                'ordering': ['address_id'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('abbreviation', models.CharField(max_length=5)),
                ('address_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'unit',
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='unit',
            index=models.Index(fields=['address_id'], name='unit_address_id'),
        ),
        migrations.AddIndex(
            model_name='unit',
            index=models.Index(fields=['id'], name='unit_id'),
        ),
        migrations.AddIndex(
            model_name='unit',
            index=models.Index(fields=['name'], name='unit_name'),
        ),
        migrations.AddField(
            model_name='sourceshare',
            name='source',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='shares',
                to='plot.Source',
            ),
        ),
        migrations.AddField(
            model_name='source',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='sources',
                to='plot.Category',
            ),
        ),
        migrations.AddField(
            model_name='source',
            name='unit',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='sources',
                to='plot.Unit',
            ),
        ),
        migrations.AddField(
            model_name='reading',
            name='source',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='readings',
                to='plot.Source',
            ),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['address_id'], name='category_address_id'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['id'], name='category_id'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='category_name'),
        ),
        migrations.AddIndex(
            model_name='sourceshare',
            index=models.Index(fields=['address_id'], name='source_share_address_id'),
        ),
        migrations.AddIndex(
            model_name='sourceshare',
            index=models.Index(fields=['end_date'], name='source_share_end_date'),
        ),
        migrations.AddIndex(
            model_name='sourceshare',
            index=models.Index(fields=['id'], name='source_share_id'),
        ),
        migrations.AddIndex(
            model_name='sourceshare',
            index=models.Index(fields=['start_date'], name='source_share_start_date'),
        ),
        migrations.AddIndex(
            model_name='source',
            index=models.Index(fields=['amber_high'], name='source_amber_high'),
        ),
        migrations.AddIndex(
            model_name='source',
            index=models.Index(fields=['amber_low'], name='source_amber_low'),
        ),
        migrations.AddIndex(
            model_name='source',
            index=models.Index(fields=['description'], name='source_description'),
        ),
        migrations.AddIndex(
            model_name='source',
            index=models.Index(fields=['id'], name='source_id'),
        ),
        migrations.AddIndex(
            model_name='source',
            index=models.Index(fields=['red_high'], name='source_red_high'),
        ),
        migrations.AddIndex(
            model_name='source',
            index=models.Index(fields=['red_low'], name='source_red_low'),
        ),
        migrations.AddIndex(
            model_name='source',
            index=models.Index(fields=['seconds_valid'], name='source_seconds_valid'),
        ),
        migrations.AddIndex(
            model_name='reading',
            index=models.Index(fields=['datetime_taken'], name='reading_datetime_taken'),
        ),
        migrations.AddIndex(
            model_name='reading',
            index=models.Index(fields=['id'], name='reading_id'),
        ),
        migrations.AddIndex(
            model_name='reading',
            index=models.Index(fields=['value'], name='reading_value'),
        ),
    ]
