from django.shortcuts import render #type: ignore
from .models import Tweet
from .forms import TweetForm,Registrations
from django.shortcuts import get_object_or_404,redirect #type: ignore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def home(request):
    return render(request,"index.html")

#show tweet on main page
def display_tweet(request):
    tweets=Tweet.objects.all()
    return render(request,"tweets.html",{"tweets":tweets})



#create tweet 
@login_required
def Tweet_form(request):
    if request.method=="POST":
        form=TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect("display_tweet")
    else:
        form=TweetForm()
    return render(request,"form.html",{'form':form})

#edit created tweet 
@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("display_tweet")
    else:
        form = TweetForm(instance=tweet)
    return render(request, "form.html", {"form": form})



#Deleted Created tweet 
@login_required
def delete_tweet(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user) 
    if request.method=="POST":
        tweet.delete()
        return redirect("display_tweet")
    return render(request,"delete.html",{"tweet":tweet})

def Register(request):
    if request.method=='POST':
        form=Registrations(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect("display_tweet")
    
    else:
        form= Registrations()
    return render(request,"registration/register.html",{'form':form})