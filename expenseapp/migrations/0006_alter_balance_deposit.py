# Generated by Django 3.2.5 on 2021-09-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenseapp', '0005_auto_20210918_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='deposit',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
