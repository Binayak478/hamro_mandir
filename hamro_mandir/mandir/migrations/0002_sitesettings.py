# Generated by Django 5.0 on 2025-02-25 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandir', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, help_text='Site logo (preferably square, at least 96x96px)', null=True, upload_to='site/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
    ]
