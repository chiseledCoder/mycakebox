from django.shortcuts import render, render_to_response, HttpResponseRedirect, Http404, HttpResponse, get_object_or_404

# Create your views here.
def rider_details(request, rider_id):
	rider = get_object_or_404(Rider, rider_id=rider_id)
	context = {

	}
	template = "rider/rider_details.html"
	return render(request, context)