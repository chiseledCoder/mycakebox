import string
import random
from .models import Customer

def customer_id_generator(size=5, chars=string.ascii_uppercase + string.digits):
	the_id = "".join(random.choice(chars) for x in range(size))
	try:
		customer_id = Customer.objects.get(customer_id=the_id)
		customer_id_generator()
	except Customer.DoesNotExist:
		return the_id