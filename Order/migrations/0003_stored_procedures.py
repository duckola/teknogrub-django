from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0002_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE PROCEDURE CreateOrder(
                IN user_id INT,
                IN canteen_id INT,
                IN total_amount DECIMAL(10, 2),
                IN payment_method VARCHAR(50)
            )
            BEGIN
                INSERT INTO Order_order (user_id, canteen_id, total_amount, payment_method, status, created_at, updated_at)
                VALUES (user_id, canteen_id, total_amount, payment_method, 'Pending', NOW(), NOW());
                SELECT LAST_INSERT_ID();
            END;
            """
        ),
        migrations.RunSQL(
            """
            CREATE PROCEDURE GetOrderDetails(
                IN order_id INT
            )
            BEGIN
                SELECT * FROM Order_orderitem WHERE order_id = order_id;
            END;
            """
        ),
    ]
