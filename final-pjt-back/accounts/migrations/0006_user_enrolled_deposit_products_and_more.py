# Generated by Django 4.2.8 on 2024-05-23 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finlife', '0003_savingproducts_depositproducts_max_limit_and_more'),
        ('accounts', '0005_alter_user_goal_alter_user_address_alter_user_assets_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enrolled_deposit_products',
            field=models.ManyToManyField(blank=True, related_name='enrolled_users', to='finlife.depositproducts'),
        ),
        migrations.AddField(
            model_name='user',
            name='enrolled_saving_products',
            field=models.ManyToManyField(blank=True, related_name='enrolled_users', to='finlife.savingproducts'),
        ),
    ]
