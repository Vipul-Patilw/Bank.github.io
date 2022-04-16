#pylint:disable=E0602
#pylint:disable=E0001
from ast import With
from base64 import decode, urlsafe_b64decode, urlsafe_b64encode
from distutils.log import error
from email import message
from quopri import decodestring
from threading import local
from django.shortcuts import redirect, render
from django.http import HttpResponse
from requests import request
from bankingSolutuon.models import Login 
#from bankingSolutuon.models import Sign
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from bankingSolutuon.models import Credit
from bankingSolutuon.models import Withdraw
from bankingSolutuon.models import SendMoney
from bankingSolutuon.models import MobileRecharge
from bankingSolutuon.models import Operator
from bankingSolutuon.models import ChangePassword
from django.contrib import messages
import re
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from bankproject import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail

# Create your views here.

a = 0.00
b=""
class changePassword(PasswordChangeView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('password_success')




def password_success(request):
	messages.info(request,"Password Changed Successfully")
	return render (request, 'setting.html')
#	global b
	#if request.method =="POST":
	#	password = request.POST.get('password')
	#	pass3 = request.POST.get('pass3')
		#pass4 = request.POST.get('pass4')
		#changepass =  ChangePasdword (password=password, pass3=pass3, pass4=pass4)
	#	changepass.save()
	#	if b == str(password):
	#		if len(password)>=6 and re.#search(r"[A-Z][a-z]+[@_!#$%^&*()?/}{~:]+[0-9]",password):
	#			message.success(request,"password change successfully")
			#	return redirect ("/home")
		#	else:
			#		messages.error(request,"password should be at least 8 character long. contain both uppercase and lowercase character, at least one alpha numeric and one special charecter  (eg:Test@123)")
			#		return redirect ('/changepass')
	#	else:
	#		message.error(request,"old password doesn't matched")
			

def index(request):
	

		if request.method =="POST":
		
			full_name = request.POST.get('full_name')
			bank_name = request.POST.get('bank_name')
			mobile_number= request.POST.get('mobile_number')
			account_number= request.POST.get('account_number')
			card_number= request.POST.get('card_number')
			email = request.POST.get('email')
			password= request.POST.get('password')
			gender = request.POST.get('gender')
			country = request.POST.get('country')
			birthdate = request.POST.get('birthdate')
			password2 = request.POST.get('password2')
			try:
				myuser = User.objects.create_user(account_number,email,password)
				myuser.first_name = full_name
				myuser.last_name = bank_name
				#myuser.email = mobile_number
				myuser.is_active = False
				myuser.save()
				#welcome email
				#email_sub = "welcome to Bank_Pay"
				#email_body = 'Hello ' + (myuser.first_name).title() + "," + "\n\nWelcome to Bank-Pay\nCongrats! your account is created successfully\nThanks for visiting our application.\n Please confirm your email address in order to activate your account link is given below\n\n Thank You"
				#from_email= settings.EMAIL_HOST_USER
				#to_email = [myuser.email]
				#send_mail(email_sub,email_body,from_email,to_email,fail_silently= True)

				#confirmation email
				current_site = get_current_site(request)
				email_sub2 = 'Activate your BANK-PAY Account'
				message2 = render_to_string('email_confirmation.html',{
					'name': myuser.first_name, 
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
					'token': generate_token.make_token(myuser)
					})
				email = EmailMessage(
					email_sub2,
					message2,
					settings.EMAIL_HOST_USER,
					[myuser.email],
					)
				
				email.fail_silently= True
				email.send()
			#	context={ "bank": bank_name,
			#	"mobile": mobile_number,
			#	"card":card_number}
				Account = ["1234 5678 986 7800","345 1234 5678 986","256 5778 786 7600","486 6678 986 6800","446 2678 286 3800","556 7678 786 7800","156 5658 966 7300","856 5478 926 7800","416 5078 986 3830","356 6678 686 9850","226 4648 586 6800","656 7678 986 6800","456 5478 946 7840","156 2678 386 800"]
			
				if len(password)>=6 and re.search(r"[A-Z][a-z]+[@_!#$%^&*()?/}{~:]+[0-9]",password) and password==password2:
					pass
				else:
					messages.error(request,"password should be at least 8 character long. contain both uppercase and lowercase character, at least one alpha numeric and one special charecter  (eg:Test@123)/confirm password should matched with password")
					return redirect("/sign")
		        	
				for i in Account:
					if i == str(account_number):
						messages.success(request, full_name.title())
						return render(request, 'gotologin.html')
						
						
				else: 		
						messages.error(request," Account number is not valid")	
						return redirect("/sign")
			except:
				messages.error(request,"this account is already registered with another name")
				return redirect ('/sign')
				
		#return render(request, 'logininfo.html')	
		return render(request, 'logininfo.html')
	
	#  return HttpResponse("vipul patil")

def gotologin(request):
	return render (request,'gotologin.html')	
def sign(request):

	if request.method =="POST":
		Loginpassword= request.POST.get('Loginpassword')
		account_number1 = request.POST.get('account_number1')
		user = authenticate(username=account_number1, password=Loginpassword)
		if user is not None:
			login(request, user)
			
			#full_name = user.first_name
			return  render(request, "home.html", )
		else:
	#	if str(Loginpassword) == str(b):
		#	messages.error(request,"password matched")
		#	return redirect('/login')    			
	  
			messages.error(request, "Please enter correct account number and  password ")
			return redirect('/login')    
		#	return render(request,'index.html')   
	return render(request,'index.html')
	
def home(request):
		global a
		if request.user.is_anonymous:
			return redirect ("/login")

		if request.method =="POST":
			amount = request.POST.get('amount')
			credit = Credit(amount=amount)
			credit.save()
		
			a += float(amount)
			messages.success(request, amount)
			return redirect('/home')
			
		
		#	if b == user:
				#	return render (request,'sendMoney.html')
			
			
	
		return render (request,"home.html")	


	
def withdraw(request):
	global a
	if request.method =="POST":
		amount2 = request.POST.get('amount2')
		withdraw = Withdraw(amount2=amount2)
		withdraw.save()
		if a < float(amount2):
				messages.error(request, amount2 + " Can't be Withdraw from your account,  you don't have sufficient balance")
				return redirect ("withdraw.html")
		else:
			a -= float(amount2)
			messages.success(request, amount2 + ", withdraw from your account successfully" )
			return render (request,"withdraw.html")	
	return render (request,"withdraw.html")


def balance(request):
	global a
	messages.info(request, a)
	credits = Credit.objects.all()
	withdraws = Withdraw.objects.all()
	moneysends = SendMoney.objects.all()
	recharges = MobileRecharge.objects.all()
	return render (request,'balance.html', { 'credits': credits,'withdraws': withdraws,'moneysends': moneysends,'recharges': recharges})
	
def setting(request):
	return render (request,'setting.html')
		
def sendMoney(request):
	global a
	#if request.method =="POST":
		#	pass1 = request.POST.get('pass1')
			#user = authenticate( password=pass1)

		#	if user is not None:
		#		SendMoney(request, user)
			#	return render(request, 'sendMoney.html')
			
		#	else:
		#		messages.error(request, "wrong password ")
			#	return redirect('/home')



	if request.method =="POST":
			amount = request.POST.get('amount')
			account_number=request.POST.get('account_number')
			send = SendMoney (amount=amount, account_number=account_number)
			send.save()
			if a < float(amount):
				messages.error(request, "you don't have sufficient balance")
				return redirect ("/send")
			else:
				a -= float(amount)
				messages.info(request, amount,account_number)
				return render (request,'sendDetails.html')
	return render (request,'sendMoney.html')


def operator(request):

	if request.method =="POST":
		operator = request.POST.get('operator')
		mobile_number = request.POST.get('mobile_number')
		operators =  Operator(operator=operator, mobile_number=mobile_number)
		operators.save()
		return redirect ('/recharge')
	return render (request,'operator.html')

def recharge (request):
	global a
	if request.method =="POST":
			amount = request.POST.get('amount')

			recharge =  MobileRecharge(amount=amount)
			recharge.save()
			if float(amount) > a: 
				messages.error(request, amount+ " recharge failed ")
				return redirect ("/recharge.html")
			elif float(amount) == 1099.0:
				a -= float(amount)
				messages.success(request, amount + " recharge succesfull")
				a += 50.0
				messages.success(request, "Congrats! you get Rs 50 cashback on recharge of 1099")
				return render (request,'recharge.html')
			else:
				a -= float(amount)
				messages.success(request, amount + " recharge succesfull")
				return render (request,'recharge.html')
				
	return render (request,'recharge.html')
	
def personalDetails (request):
	return render (request,'personalDetails.html')

def about (request):
	return render (request,'about.html')

def privacy (request):
	return render (request,'privacy.html')



def admin(request):
	return render(request,"admin.html")

def logoutuser(request):
	logout (request)
	return redirect ("/login")

def activate(request, uidb64, token):
	try:
		uid = decodestring(urlsafe_base64_decode(uidb64))
		myuser = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		myuser = None

	if myuser is not None and generate_token.check_token(myuser, token):
		myuser.is_active = True
		myuser.save()
		login(request,myuser)
		return redirect('/login')
		
	else:
		return render(request, 'activation_failed.html')
		

