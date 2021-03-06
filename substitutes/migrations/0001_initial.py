# Generated by Django 2.2.1 on 2019-05-20 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImportReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=20)),
                ('lenght', models.IntegerField()),
                ('received_products', models.IntegerField()),
                ('accepted_products', models.IntegerField()),
                ('rejected_names', models.IntegerField()),
                ('rejected_images', models.IntegerField()),
                ('rejected_url', models.IntegerField()),
                ('rejected_creator', models.IntegerField()),
                ('rejected_stores', models.IntegerField()),
                ('rejected_brands', models.IntegerField()),
                ('rejected_nutriscore', models.IntegerField()),
                ('rejected_nutriments_unit_g', models.IntegerField()),
                ('rejected_nutriments_energy_unit', models.IntegerField()),
                ('rejected_nutriments_energy_kcal', models.IntegerField()),
                ('rejected_nutriments_energy_kj', models.IntegerField()),
                ('rejected_categories', models.IntegerField()),
                ('rejected_ingredients', models.IntegerField()),
            ],
            options={
                'verbose_name': 'import report',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.URLField(max_length=300)),
                ('url', models.URLField(max_length=300)),
                ('creator', models.CharField(max_length=100)),
                ('brands', models.CharField(max_length=100)),
                ('stores', models.TextField()),
                ('nutriscore', models.IntegerField()),
                ('categories', models.TextField()),
                ('ingredients', models.TextField()),
                ('nutriments', models.TextField()),
            ],
            options={
                'verbose_name': 'product',
                'ordering': ['name'],
            },
        ),
    ]
