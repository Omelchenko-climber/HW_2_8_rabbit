from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    fullname = StringField()
    phone_number = StringField()
    email = StringField()
    sent_message = BooleanField(default=False)
    message_method = StringField(choices=("SMS", "email"), default="email")