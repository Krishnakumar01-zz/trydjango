from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from .models import Scorecard
from .forms import ScoreForm

# Create your views here.
def home(request):
	title='Welcome'
	order_by = request.GET.get('order_by', 'marks')
	leaderboard=Scorecard.objects.all().order_by(order_by).reverse()
	context={
		'title':title,
		'leaderboard':leaderboard
		}
	return render(request,'leaderboard/home.html',context)

def link(request,pk):
	board=get_object_or_404(Scorecard,pk=pk)
	return render(request,'leaderboard/link.html',{'board':board})

def signup(request):
	if request.method=='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			username=form.cleaned_data.get('username')
			password=form.cleaned_data.get('password1')
			obj=form.save()
			user=authenticate(username=username,password=password)
			
			login(request,user)
			return redirect('home')	
	else:
		form=UserCreationForm()
		return render(request,'leaderboard/signup.html',{'form':form})

def	signin(request):
	if request.method=='POST':
		form=AuthenticationForm(request.POST)
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
	else:
		form=AuthenticationForm()
		return render(request,'leaderboard/signin.html',{'form':form})

def create(request):
	if request.method=='POST':
		form=ScoreForm(request.POST)
		if form.is_valid():
			board=form.save(commit=False)
			board.creator=request.user
			board.save()
			return redirect('link',pk=board.pk)
	else:
		form=ScoreForm()
		return render(request,'leaderboard/create.html',{'form':form})

def edit(request,pk):
	board=get_object_or_404(Scorecard,pk=pk)
	if request.method=='POST':
		form=ScoreForm(request.POST,instance=board)
		if form.is_valid() and request.user==board.creator:
			board=form.save(commit=False)
			board.save()
			return redirect('link',pk=board.pk)
		else:
			message='Sorry you cant edit'
			return render(request,'leaderboard/failure.html',{'message':message})
	else:
		form=ScoreForm(instance=board)
		return render(request,'leaderboard/create.html',{'form':form})

def delete(request,pk):
	board=get_object_or_404(Scorecard,pk=pk)
	if board.creator==request.user:
		board.delete()
		return redirect('home')
	else:
		message='You cant delete'
		return render(request,'leaderboard/failure.html',{'message':message})

def signout(request):
	logout(request)
	return redirect('signin')

