# Generated by Django 4.2.6 on 2023-11-28 22:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, null=True)),
                ('image_categorie', models.ImageField(null=True, upload_to='products/categories')),
                ('image_categorie1', models.ImageField(null=True, upload_to='products/categories')),
            ],
        ),
        migrations.CreateModel(
            name='Finition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Images_site_lariparis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image1_accueil_hero', models.ImageField(null=True, upload_to='accueil')),
                ('image2_accueil_hero', models.ImageField(null=True, upload_to='accueil')),
            ],
        ),
        migrations.CreateModel(
            name='Lace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('price', models.FloatField(default=200.0)),
                ('stock', models.IntegerField(default=0)),
                ('short_description1', models.CharField(max_length=50)),
                ('short_description2', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image1', models.ImageField(null=True, upload_to='products')),
                ('image2', models.ImageField(null=True, upload_to='products')),
                ('categorie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.categorie')),
                ('choix_lace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.lace')),
                ('finition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.finition')),
                ('taille', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.taille')),
            ],
        ),
    ]