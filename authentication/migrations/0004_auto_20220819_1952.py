# Generated by Django 4.1 on 2022-08-19 19:52

from django.db import migrations


class Migration(migrations.Migration):
    def load_initial_data(apps, schema_editor):
        # get our model
        # get_model(appname, modelname)
        role_model = apps.get_model('authentication', 'role')
        role_model.objects.create(
            id='9db782df-6704-458a-8bcd-426103e7808d', description="admin")
        role_model.objects.create(
            id='9df225e8-d882-49ea-9e79-5d9797bcca1c', description="leader")
        role_model.objects.create(
            id='e7e430f1-9a63-4485-b56c-20fc8a16a7b9', description="user")

    dependencies = [
        ('authentication', '0003_alter_permission_id_alter_role_id_and_more'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
