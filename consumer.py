import json
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from model import Contact
from connection import connect


credentials = PlainCredentials("guest", "guest")
connection = BlockingConnection(ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue="email_mock", durable=True)
print("Waiting for messages. To exit press CTRL+C")

def send_email_message(email):
    print(f"Sending email message to {email}")


def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data["contact_id"]
    print(contact_id)
    contact = Contact.objects.get(id=contact_id)

    if not contact.sent_message:
        send_email_message(contact.email)
        contact.sent_message = True
        contact.save()
        print(f"Sent message to contact {contact.fullname}.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="email_mock", on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()



