from peewee import SqliteDatabase, Model, CharField, AutoField, IntegerField, fn
import random
import json

# Initialize DB
db = SqliteDatabase('verybaseddb.db')

# Define Models
class User(Model):
    id = AutoField()
    name = CharField(unique=False)
    class Meta:
        database = db

class Product(Model):
    product = CharField(unique=False)
    product_id = AutoField()
    class Meta:
        database = db

class Order(Model):
    order_n = AutoField()
    user_id = IntegerField()
    product_id = IntegerField()
    class Meta:
        database = db

def update_order_product(order_n, new_product_id):
    """
    Update the product_id for a specific order_n in the Order table.
    user_id remains unchanged.
    """
    try:
        order = Order.get(Order.order_n == order_n)
        old_product_id = order.product_id
        order.product_id = new_product_id
        order.save()
        print(f"Order {order_n}: product_id updated from {old_product_id} to {new_product_id}")
    except Order.DoesNotExist:
        print(f"Order {order_n} does not exist.")

# Connect and create tables
db.connect()
db.drop_tables([Order])
db.create_tables([User, Product, Order], safe=True)

# Add predefined users (no duplicates)
names = ['Charlie', 'Kolya', 'Vasja', 'Ktoto', 'Ivan', 'Tung Sahur', 'Boris']
for name in names:
    User.get_or_create(name=name)

# Load users from JSON file (no duplicates)
with open('users.json', 'r') as file:
    users_data = json.load(file)
for entry in users_data:
    User.get_or_create(name=entry['name'])

# Load products from JSON file (no duplicates)
with open('products.json', 'r') as file:
    product_data = json.load(file)
for entry in product_data:
    Product.get_or_create(product=entry['product'])

# Get all existing user and product IDs
user_ids = [user.id for user in User.select(User.id)]
product_ids = [prod.product_id for prod in Product.select(Product.product_id)]

# Generate random orders
for _ in range(10):
    Order.create(
        user_id=random.choice(user_ids),
        product_id=random.choice(product_ids)
    )

# Count how many times each product_id appears in the Order table
print("\nProduct order counts:")
query = (Order
         .select(Order.product_id, fn.COUNT(Order.product_id).alias('count'))
         .group_by(Order.product_id)
         .order_by(Order.product_id))
for entry in query:
    print(f"Product ID {entry.product_id} appears {entry.count} times")

# Example: Update the product_id for the first order to a new product_id
if Order.select().count() > 0:
    first_order = Order.select().order_by(Order.order_n).first()
    new_product_id = random.choice(product_ids)
    update_order_product(first_order.order_n, new_product_id)

db.close()
