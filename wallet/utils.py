import random
import string


def generate_account_number():
    return "44" + (str(random.randrange(00000000, 99999999)))


def generate_reference_id():
    letter = list(string.ascii_letters, )
    alphanumeric = list(string.digits) + letter
    return ''.join(random.sample(alphanumeric, 20))
