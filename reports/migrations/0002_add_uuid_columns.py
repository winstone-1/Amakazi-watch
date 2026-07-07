from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        # Add UUID column to IncidentReport
        migrations.AddField(
            model_name='incidentreport',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        # Add UUID column to Report
        migrations.AddField(
            model_name='report',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        # Remove the voicereport line - it doesn't exist!
    ]