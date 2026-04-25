# Generated manually for adding button URLs to DebitCardPromo

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_add_button_url_to_pekeaccountsummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitcardpromo',
            name='primary_button_url',
            field=models.URLField(blank=True, help_text='URL a la que redirige el botón principal', null=True, verbose_name='URL del botón principal'),
        ),
        migrations.AddField(
            model_name='debitcardpromo',
            name='secondary_button_url',
            field=models.URLField(blank=True, help_text='URL a la que redirige el botón secundario', null=True, verbose_name='URL del botón secundario'),
        ),
    ]