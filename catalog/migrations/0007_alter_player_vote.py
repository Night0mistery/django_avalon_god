# Generated by Django 3.2.5 on 2021-07-28 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20210728_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='vote',
            field=models.CharField(choices=[('agree', 'I agree with the chief!'), ('disagree', 'I don`t agree with the chief!')], default='I agree with the chief!', help_text="Choose 'agree' if the chief`s proposal sounds OK for you.", max_length=20),
        ),
    ]
