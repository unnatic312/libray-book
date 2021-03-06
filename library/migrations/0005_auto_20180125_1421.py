# Generated by Django 2.0.1 on 2018-01-25 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='users',
        ),
        migrations.AlterField(
            model_name='books',
            name='auther',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Auther'),
        ),
        migrations.AlterField(
            model_name='books',
            name='publication',
            field=models.ManyToManyField(to='library.Publication'),
        ),
        migrations.AddField(
            model_name='bookreview',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Books'),
        ),
    ]
