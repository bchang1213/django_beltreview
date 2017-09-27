# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import bcrypt

from .models import *

# Create your views here.
def index(request):
	return render(request, "belt_review/index.html")

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		user = User.objects.get(email=request.POST['email'])
		if user:
			if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
				messages.error(request, 'Account with those credentials could not be found.')
				return redirect('/')
			else:
				if user:
					request.session['user'] = user.id
					messages.success(request, 'Login Successful!')
					return	redirect('/books')
					# return redirect(reverse('success',kwargs ={'user_id':user.id}))


def register(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags= tag)
		return redirect('/')
	else:
		user = User.objects.create()
		user.name = request.POST['name']
		user.alias = request.POST['alias']
		user.email =request.POST['email']
		# user.dob =request.POST['dob']
		user.userlevel = "normal"
		user.password =bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		user.save()
		messages.success(request, 'User created. Please login!')
		return redirect('/')


def loggedin(request):
	context={
	'user': User.objects.get(id = request.session['user']),
	'reviews': Review.objects.all(),
	'books': Book.objects.all(),
	}
	return render(request, "belt_review/books.html", context)

def logout(request):
	del request.session['user']
	return redirect('/')

def bookform(request):
	context={
		'authors': Book.objects.all()
	}
	return render(request, "belt_review/bookform.html", context)

def submit(request):
	if len(request.POST['author1']):
		book = Book.objects.create(title=request.POST['booktitle'], author=request.POST['author1'])
		book.save()
	elif not len(request.POST['author1']):
		book = Book.objects.create(title=request.POST['booktitle'], author=request.POST['author'])
		book.save()
	review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'],book_id=book.id, user_id=request.session['user'])
	review.save()
	return redirect(reverse('specificbook',kwargs ={'book_id':book.id}))

def reviewsubmit(request):
	review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'],book_id=request.POST['bookid'], user_id=request.session['user'])
	review.save()
	return redirect(reverse('specificbook',kwargs ={'book_id':request.POST['bookid']}))

def specificbook(request, book_id):
	context = {
	"book": Book.objects.get(id = book_id),
	'reviews': Review.objects.filter(book_id = book_id)
	}
	return render(request, "belt_review/specificbook.html", context)

def users(request, user_id):
	context = {
	'user': User.objects.get(id = user_id),
	'reviews': Review.objects.filter(user_id = user_id).count(),
	'postedreviews': Review.objects.filter(user_id = user_id),
	}
	return render(request, "belt_review/users.html", context)
	
def delete(request, book_id, review_id):
	review = Review.objects.get(id = review_id)
	review.delete()
	return redirect(reverse('specificbook',kwargs ={'book_id':book_id}))
