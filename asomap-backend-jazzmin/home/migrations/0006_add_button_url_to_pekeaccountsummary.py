# Generated manually for adding button_url to PeKeAccountSummary

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_slideritem'),
    ]

    operations = [
        migrations.AddField(
            model_name='pekeaccountsummary',
            name='button_url',
            field=models.URLField(blank=True, help_text='URL a la que redirige el botón', null=True, verbose_name='URL del botón'),
        ),
    ]