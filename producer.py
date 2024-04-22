import json
import random

import pika.spec
from faker import Faker
from pika import BlockingConnection, ConnectionParameters, PlainCredentials, BasicProperties

from model import Contact
from connection import connect


credentials = PlainCredentials("guest", "guest")
connection = BlockingConnection(ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange="send_mock", exchange_type="direct")
channel.queue_declare(queue="email_mock", durable=True)
channel.queue_bind(exchange="send_mock", queue="email_mock")

def main():
    fake = Faker()
    for _ in range(10):
        fullname = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        message_method = "SMS" if bool(random.randbytes(1)) else "email"
        contact = Contact(
            fullname=fullname,
            email=email,
            phone_number=phone_number,
            message_method=message_method
        )
        contact.save()

        channel.basic_publish(
            exchange="",
            routing_key="email_mock",
            body=json.dumps({"contact_id": str(contact.id)}).encode(),
            properties=BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )


if __name__ == '__main__':
    main()
