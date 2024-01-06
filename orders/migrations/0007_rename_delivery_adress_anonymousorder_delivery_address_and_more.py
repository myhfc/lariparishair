# Generated by Django 4.2.6 on 2024-01-05 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_remove_anonymousorder_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anonymousorder',
            old_name='delivery_adress',
            new_name='delivery_address',
        ),
        migrations.RenameField(
            model_name='classicorder',
            old_name='delivery_adress',
            new_name='delivery_address',
        ),
        migrations.RemoveField(
            model_name='classicorder',
            name='cart',
        ),
        migrations.AddField(
            model_name='anonymousorder',
            name='articles',
            field=models.ManyToManyField(to='orders.article'),
        ),
        migrations.AddField(
            model_name='anonymousorder',
            name='delivery_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='anonymousorder',
            name='tax',
            field=models.FloatField(default=0.2),
        ),
        migrations.AddField(
            model_name='classicorder',
            name='articles',
            field=models.ManyToManyField(to='orders.article'),
        ),
        migrations.AddField(
            model_name='classicorder',
            name='delivery_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='classicorder',
            name='tax',
            field=models.FloatField(default=0.2),
        ),
        migrations.CreateModel(
            name='userDeliveryAdress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_adress', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.delivery')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]