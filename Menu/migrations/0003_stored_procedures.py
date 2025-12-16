from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0002_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE PROCEDURE CreateMenuItem(
                IN canteen_id INT,
                IN category_id INT,
                IN name VARCHAR(255),
                IN description TEXT,
                IN ingredients VARCHAR(500),
                IN price DECIMAL(10, 2),
                IN image_url VARCHAR(100),
                IN is_available BOOLEAN
            )
            BEGIN
                INSERT INTO Menu_menuitem (canteen_id, category_id, name, description, ingredients, price, image_url, is_available)
                VALUES (canteen_id, category_id, name, description, ingredients, price, image_url, is_available);
                SELECT LAST_INSERT_ID();
            END;
            """
        ),
        migrations.RunSQL(
            """
            CREATE PROCEDURE UpdateMenuItem(
                IN item_id INT,
                IN canteen_id INT,
                IN category_id INT,
                IN name VARCHAR(255),
                IN description TEXT,
                IN ingredients VARCHAR(500),
                IN price DECIMAL(10, 2),
                IN image_url VARCHAR(100),
                IN is_available BOOLEAN
            )
            BEGIN
                UPDATE Menu_menuitem
                SET
                    canteen_id = canteen_id,
                    category_id = category_id,
                    name = name,
                    description = description,
                    ingredients = ingredients,
                    price = price,
                    image_url = image_url,
                    is_available = is_available
                WHERE id = item_id;
            END;
            """
        ),
    ]
