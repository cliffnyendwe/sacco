import uuid

def get_activation_code(size = 10):
    code = str(uuid.uuid4()).replace('-', '')
    return code.upper()[:size].upper()
    
def ordinal_day(n):

    suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']

    if n < 0:
        n *= -1

    n = int(n)

    if n % 100 in (11,12,13):
        s = 'th'
    else:
        s = suffix[n % 10]

    return str(n) + s
