def current_uri(request):
  return {
    'current_uri': request.build_absolute_uri(),
    'current_host': request.get_host(),
  }