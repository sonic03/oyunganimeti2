import random
import string


def id_generator(size=11, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_id(instance):

    new_order_id=id_generator()

    Klass=instance.__class__
    qs_exists=Klass.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_id(instance)
    return new_order_id
