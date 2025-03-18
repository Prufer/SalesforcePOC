from datetime import datetime

from faker import Faker
import random

fake = Faker()

def generate_random_name():
    """Generates a random first name."""
    return fake.first_name()

def generate_random_mobile_local():
    """Generates a random local mobile number with a fixed prefix."""
    prefix = "049999"
    suffix = "".join(str(random.randint(0, 9)) for _ in range(4))
    return prefix + suffix

def generate_random_mobile_international():
    """Generates a random international mobile number with a fixed prefix."""
    prefix = "+91889999"
    suffix = "".join(str(random.randint(0, 9)) for _ in range(4))
    return prefix + suffix

def generate_random_word(length=5):
    """Generates a random lowercase word of given length."""
    return fake.word().lower()[:length]

def generate_paragraph(word_count=100):
    """Generates a random paragraph with the specified number of words."""
    return fake.paragraph(nb_sentences=5, variable_nb_sentences=True)

def get_execution_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def generate_random_org_name():
    prefix = "Auto_Org_"
    suffix = "".join(fake.city().title())
    timestamp = get_execution_timestamp()
    return f"{prefix}_{suffix}_{timestamp}"

