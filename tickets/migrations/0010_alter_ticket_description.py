# Generated by Django 3.2.14 on 2022-07-27 14:53

from django.db import migrations, models
import tickets.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_alter_ticket_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(validators=[tickets.validators.textfield_not_empty]),
        ),
    ]