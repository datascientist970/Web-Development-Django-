from django.urls import path    #type: ignore
from . import views
urlpatterns = [
    path("tweet/",views.display_tweet,name='display_tweet'),
    path("create/",views.Tweet_form,name='Tweet_form'),
    path("<int:tweet_id>/edit/",views.edit_tweet,name='edit_tweet'),
    path("<int:tweet_id>/delete/",views.delete_tweet,name='delete_tweet'),
    path('home/', views.home, name='home'),
    path('registration/',views.Register,name='register'),

] 
