from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0002_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE PROCEDURE CreateUserPaymentMethod(
                IN user_id INT,
                IN method_type VARCHAR(20),
                IN account_name VARCHAR(100),
                IN account_number VARCHAR(20),
                IN masked_card_number VARCHAR(20),
                IN expiry_date VARCHAR(5),
                IN is_default BOOLEAN
            )
            BEGIN
                INSERT INTO Payment_userpaymentmethod (user_id, method_type, account_name, account_number, masked_card_number, expiry_date, is_default)
                VALUES (user_id, method_type, account_name, account_number, masked_card_number, expiry_date, is_default);
            END;
            """
        ),
        migrations.RunSQL(
            """
            CREATE PROCEDURE DeleteUserPaymentMethod(
                IN method_id INT
            )
            BEGIN
                DELETE FROM Payment_userpaymentmethod WHERE id = method_id;
            END;
            """
        ),
    ]
