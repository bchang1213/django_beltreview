from __future__ import unicode_literals

from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# DATE_STR_REGEX = re.compile(r'^[0-9]{2}-[0-9]{2}-[0-9]{4}$')
# Create your models here.

class UserManager(models.Manager):
	def login_validator(self, postData):
		errors = {}
		if not EMAIL_REGEX.match(postData['email']) or len(postData['password']) < 8:
			errors['email']="Please enter valid credentials."
		return errors

	def basic_validator(self, postData):
		errors = {}
# VALIDATING THE name
		if len(postData['name']) == 0:
			errors['name']="Please enter your name"
# VALIDATING alias
		if len(postData['alias']) == 0:
			errors['alias']="Please enter your alias"
# VALIDATING EMAIL
		if not EMAIL_REGEX.match(postData['email']):
			errors['email']="Please enter a valid email"

# VALIDATING PASSWORD
		if len(postData['password']) == 0:
			errors['password']="Please enter a password"
		else:
			if len(postData['password']) < 8:
				errors['password']= "Password must be at least 8 characters."

			if not any([letter.isupper() for letter in postData['password']]):
				errors['password1']= "Password must contain at least one uppercase letter."

			if not any([letter.isdigit() for letter in postData['password']]):
				errors['password2']= "Password must contain at least one number."

			if not any([letter in "!@#$%^&*()-_=+~`\"'<>,.?/:;\}{][|" for letter in postData['password']]):
				errors['password3']= "Password must contain at least one special character."

			if postData['password'] != postData['passconf']:
				errors['password4']= 'Password and confirmation fields must match.'
		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	# dob = models.DateField(auto_now=False, auto_now_add=False)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __repr__(self):
		return ("<User object: id:{} {} {}>".format(self.id, self.first_name, self.last_name))

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
	review = models.TextField()
	rating = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	book = models.ForeignKey(Book, related_name = "reviews")
	user = models.ForeignKey(User, related_name = "reviews")









