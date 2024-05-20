import random
import string

def generate_institution_number(institution_identifier, db_number, sequence_number_length, alphanumeric_length):
    # Generate sequential number
    sequential_number = str(random.randint(1, 10 ** sequence_number_length)).zfill(sequence_number_length)

    # Generate random alphanumeric code
    alphanumeric_code = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=alphanumeric_length))

    # Combine institution identifier, sequential number, and alphanumeric code
    institution_number = f"{institution_identifier}{db_number}-{sequential_number}-{alphanumeric_code}"

    return institution_number
