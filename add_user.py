# add_user.py

from peewee import SqliteDatabase, Model, CharField, AutoField
import sys

# Initialize DB
db = SqliteDatabase('verybaseddb.db')

# Define User model (must match your main script)
class User(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        database = db

def add_user(username):
    db.connect()
    user = User.create(name=username)
    print(f"Added user: {user.id} - {user.name}")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_user.py <username>")
    else:
        username = sys.argv[1]
        add_user(username)
