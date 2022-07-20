import random
import sys
from faker import Faker
from ajax_table import db, User, Produto


def create_fake_users(n):
    """Generate fake users."""
    faker = Faker()
    for i in range(n):
        user = User(name=faker.name(),
                    age=random.randint(20, 80),
                    address=faker.address().replace('\n', ', '),
                    phone=faker.phone_number(),
                    email=faker.email())
        db.session.add(user)
    db.session.commit()
    print(f'Added {n} fake users to the database.')


def create_produto():
    """Generate fake users."""

    produto = Produto(name='dasdsa',
                preco=25,
                categoria= 'agasalho')

    db.session.add(produto)
    db.session.commit()
    print(f'Added produto to the database.')

if __name__ == '__main__':
    create_produto()
