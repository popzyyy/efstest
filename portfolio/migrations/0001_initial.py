# Generated by Django 3.2.7 on 2021-09-09 16:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('cust_number', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=200)),
                ('cell_phone', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('shares', models.DecimalField(decimal_places=1, max_digits=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='portfolio.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('acquired_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('acquired_date', models.DateField(default=django.utils.timezone.now)),
                ('recent_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recent_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='portfolio.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Funds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('minimum_purchase', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateField(default=django.utils.timezone.now)),
                ('purchase_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recent_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('present_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funds', to='portfolio.customer')),
            ],
        ),
    ]
