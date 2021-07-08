from api.router import router, extra_urlpatterns

urlpatterns = []
urlpatterns += router.urls
urlpatterns.extend(extra_urlpatterns)
