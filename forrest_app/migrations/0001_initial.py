# Generated by Django 4.1.3 on 2022-12-04 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminBotUser',
            fields=[
                ('telegram_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nickname', models.TextField(blank=True)),
                ('full_name', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.TextField()),
                ('full_name', models.TextField()),
                ('default_room', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('second_name', models.TextField()),
                ('last_name', models.TextField()),
                ('contact', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TextField()),
                ('end', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.TextField()),
                ('week_day', models.IntegerField(choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')])),
                ('week_type', models.BooleanField(choices=[(True, 'Четная'), (False, 'Нечетная')])),
                ('discipline', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forrest_app.discipline')),
                ('time', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forrest_app.time')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('exp_date', models.TextField()),
                ('description', models.TextField()),
                ('subject', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forrest_app.discipline')),
                ('type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forrest_app.homeworktype')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_chat_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('admins', models.ManyToManyField(blank=True, null=True, related_name='groups', to='forrest_app.adminbotuser')),
            ],
        ),
        migrations.AddField(
            model_name='discipline',
            name='teacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forrest_app.teacher'),
        ),
    ]