# Generated by Django 3.0.5 on 2020-04-13 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('srs', '0005_auto_20200413_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestreamConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField()),
                ('streamkey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='srs.Streamkey')),
            ],
        ),
    ]