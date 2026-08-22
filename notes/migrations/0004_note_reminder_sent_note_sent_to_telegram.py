from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_note_user_notegroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='reminder_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='sent_to_telegram',
            field=models.BooleanField(default=False),
        ),
    ]
