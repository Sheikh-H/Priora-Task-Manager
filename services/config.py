from services.database import initialise_database
from services.auth import generate_secrets
from dotenv import load_dotenv

load_dotenv()


def initialise():
    initialise_database()
    generate_secrets()
