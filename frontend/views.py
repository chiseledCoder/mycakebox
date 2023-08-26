from django.shortcuts import render, HttpResponseRedirect, render_to_response, HttpResponse, get_object_or_404
# Create your views here.

def home(request):
	template = "index.html"
	context = {
	"site_name": "My Cake Box"
	}
	return render(request, template, context)