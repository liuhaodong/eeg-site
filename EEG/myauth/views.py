from django.http import HttpResponse


def googleTokenReceiver(request):
    print request.POST  # TODO: parse and store the token
    return HttpResponse("Thanks")
