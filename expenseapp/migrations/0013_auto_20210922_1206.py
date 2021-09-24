# Generated by Django 3.2.5 on 2021-09-22 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenseapp', '0012_auto_20210921_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='deposit',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
