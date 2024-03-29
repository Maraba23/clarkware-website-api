# Generated by Django 4.1 on 2022-12-26 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('version', models.CharField(blank=True, max_length=100, null=True)),
                ('dll', models.FileField(blank=True, null=True, upload_to='dlls/')),
                ('driver', models.FileField(blank=True, null=True, upload_to='driver/')),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Undetected', 'Undetected'), ('Updating', 'Updating'), ('Use at your own risk', 'Use at your own risk'), ('Detected', 'Detected')], max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('hwid', models.CharField(blank=True, max_length=100, null=True)),
                ('is_banned', models.BooleanField(default=False)),
                ('auth_token', models.CharField(max_length=100, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_premium', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_banned', models.BooleanField(default=False)),
                ('is_used', models.BooleanField(default=False)),
                ('time', models.IntegerField(default=0)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateTimeField()),
                ('end_date_loader', models.CharField(max_length=100, null=True)),
                ('days_left', models.IntegerField(default=0)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.profile')),
            ],
        ),
    ]
