# Generated migration for adding included_corporations field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '__first__'),
        ('taxtools', '0025_corptaxperservicemoduleconfiguration_structure_type_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corptaxconfiguration',
            name='exempted_corps',
            field=models.ManyToManyField(blank=True, related_name='tax_exemptions', to='eveonline.evecorporationinfo'),
        ),
        migrations.AddField(
            model_name='corptaxconfiguration',
            name='included_corporations',
            field=models.ManyToManyField(blank=True, related_name='tax_inclusions', to='eveonline.evecorporationinfo'),
        ),
    ]
