import string
import random
from .models import Booking

def booking_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	the_id = "".join(random.choice(chars) for x in range(size))
	try:
		tracking_id = Booking.objects.get(booking_id=the_id)
		booking_id_generator()
	except Booking.DoesNotExist:
		return the_id