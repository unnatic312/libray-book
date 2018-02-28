# Generated by Django 2.0.1 on 2018-02-01 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_auto_20180201_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Books'),
        ),
        migrations.AlterField(
            model_name='books',
            name='auther',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Auther'),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_data',
            field=models.FileField(null=True, upload_to='library/'),
        ),
        migrations.AlterField(
            model_name='books',
            name='publication',
            field=models.ManyToManyField(to='library.Publication'),
        ),
    ]