import os

from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

mongo_user = os.getenv("USER")
mongo_pass = os.getenv("DB_PASS")
domain = os.getenv("DOMAIN")
db_name = os.getenv("DB_NAME")

URI = f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}?retryWrites=true&w=majority&appName=Cluster0"

connect(host=f"""mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}?retryWrites=true&w=majority&appName=Cluster0""", ssl=True)