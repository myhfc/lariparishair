# Generated by Django 4.2.6 on 2024-01-05 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_texture'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sous_categorie_PERRUQUE',
            field=models.CharField(blank=True, choices=[('LACE WIG', 'Lace Wig'), ('BOB WIG', 'Bob Wig'), ('PERRUQUE SANS COLLE', 'Perruque Sans Colle'), ('PERRUQUE BANDEAU', 'Perruque Bandeau')], max_length=25, null=True),
        ),
    ]