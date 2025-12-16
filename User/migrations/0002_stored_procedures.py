from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE PROCEDURE CreateUser(
                IN username VARCHAR(150),
                IN password VARCHAR(128),
                IN email VARCHAR(254),
                IN first_name VARCHAR(150),
                IN last_name VARCHAR(150),
                IN id_number VARCHAR(50),
                IN role_id INT
            )
            BEGIN
                INSERT INTO User_users (username, password, email, first_name, last_name, id_number, role_id, is_superuser, is_staff, is_active, date_joined)
                VALUES (username, password, email, first_name, last_name, id_number, role_id, 0, 0, 1, NOW());
            END;
            """
        ),
    ]
