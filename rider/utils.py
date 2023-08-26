import string
import random
from rider.models import Rider

def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
	the_id = "".join(random.choice(chars) for x in range(size))
	try:
		rider_id = Rider.objects.get(rider_id=the_id)
		id_generator()
	except Rider.DoesNotExist:
		return the_id