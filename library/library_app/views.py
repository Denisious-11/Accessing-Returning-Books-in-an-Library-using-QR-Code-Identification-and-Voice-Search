from django.shortcuts import render
from .models import *
import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
import re
import os
import cv2
from datetime import datetime
from threading import Thread
import threading
from datetime import date
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from datetime import date
from datetime import datetime
import qrcode
from django.views.decorators.csrf import csrf_exempt
import paho.mqtt.client as mqtt

client= mqtt.Client()
 
# issue=100

# Create your views here.

@never_cache
def show_index(request):
    return render(request, "login.html", {})


@never_cache
def logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    return render(request,'login.html')


def check_login(request):
	username = request.POST.get("username")
	password = request.POST.get("password")

	print(username)
	print(password)

	if username == 'admin' and password == 'admin':
		request.session["uid"] = "admin"
		return HttpResponse("<script>alert('Admin Login Successful');window.location.href='/show_home_admin/'</script>")
	
	else:
		return HttpResponse("<script>alert('Invalid');window.location.href='/show_index/'</script>")

@never_cache
###############ADMIN START
def show_home_admin(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		return render(request,'home_admin.html') 
	else:
		return render(request,'login.html')

@never_cache
def show_request_admin(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		req_list=Requests.objects.all()

		return render(request,'view_request_admin.html',{'req': req_list}) 
	else:
		return render(request,'login.html')

def approve(request):
	r_id=request.POST.get('r_id')
	username = request.POST.get("username")
	password = request.POST.get("password")
	name=request.POST.get("name")
	address=request.POST.get("address")
	age=request.POST.get("age")
	email=request.POST.get("email")

	obj10=Users.objects.filter(username=username,password=password,name=name,address=address,age=age,email=email)
	co=obj10.count()
	if co==1:
		obj1=Requests.objects.get(r_id=int(r_id))
		obj1.delete()
		return HttpResponse("<script>alert('User already exist ');window.location.href='/show_request_admin/'</script>")

	else:
		obj2=Users(username=username,password=password,name=name,address=address,age=age,email=email)
		obj2.save()
		obj3=Requests.objects.get(r_id=int(r_id))
		obj3.delete()
		return HttpResponse("<script>alert('Approved Successfully');window.location.href='/view_users_admin/'</script>")


def reject(request):
	r_id=request.POST.get('r_id')
	obj1=Requests.objects.get(r_id=int(r_id))
	obj1.delete()
	return HttpResponse("<script>alert('Rejected Successfully');window.location.href='/show_request_admin/'</script>")


@never_cache
def view_users_admin(request):
	if 'uid' in request.session:
		u_list=Users.objects.all()

		return render(request,'view_users_admin.html',{'req': u_list}) 
	else:
		return render(request,'login.html')


@never_cache
def view_add_book_admin(request):
	if 'uid' in request.session:
		return render(request,'view_add_book_admin.html') 
	else:
		return render(request,'login.html')

def generate_qrcode(b_id,book_name):

	# Data to be encoded
	data = '%s'%(b_id)
	print("\n *************************")
	print("data : ",data)
	 
	# Encoding data using make() function
	img = qrcode.make(data)
	path= 'library_app/static/QR CODE/%s.png' %(book_name)
	# Saving as an image file
	img.save(path)
	# Create your views here.

iden=1
def add_book(request):
	b_id = request.POST.get("b_id")
	book_name = request.POST.get("b_name")
	author_name=request.POST.get("author")
	publication=request.POST.get("publication")
	year=request.POST.get("year")
	rack_number=request.POST.get("rack_number")

	obj10=Books.objects.filter(b_id=b_id)
	co=obj10.count()
	if co==1:
		return HttpResponse("<script>alert('Book ID Already Taken');window.location.href='/view_add_book_admin/'</script>")

	else:
		global iden
		
		obj1=Books(b_id=b_id,book_name=book_name,author_name=author_name,publication=publication,year=year,rack_number=rack_number,identifer=iden)
		obj1.save()
		iden=iden+2

		generate_qrcode(b_id,book_name)
		return HttpResponse("<script>alert('Added Successfully');window.location.href='/view_books_admin/'</script>")


@never_cache
def view_books_admin(request):
	if 'uid' in request.session:
		b_list=Books.objects.all()

		return render(request,'view_books_admin.html',{'req': b_list}) 
	else:
		return render(request,'login.html')

def edit(request):
	b_id = request.POST.get("b_id")
	book_name = request.POST.get("book_name")
	author_name=request.POST.get("author_name")
	publication=request.POST.get("publication")
	year=request.POST.get("year")
	rack_number=request.POST.get("rack_number")

	obj1=Books.objects.get(b_id=int(b_id))
	obj1.book_name=book_name
	obj1.author_name=author_name
	obj1.publication=publication
	obj1.year=year
	obj1.rack_number=rack_number
	obj1.save()

	return HttpResponse("<script>alert('Edited Successfully');window.location.href='/view_books_admin/'</script>")

def delete(request):
	b_id=request.POST.get('b_id')
	obj1=Books.objects.get(b_id=int(b_id))
	obj1.delete()
	return HttpResponse("<script>alert('Deleted Successfully');window.location.href='/view_books_admin/'</script>")


@never_cache
def get_issue_requests_admin(request):
	if 'uid' in request.session:
		req_list=Book_issue.objects.filter(status="Pending")

		return render(request,'get_issue_request_admin.html',{'req': req_list}) 
	else:
		return render(request,'login.html')

def accept(request):
	issue_id=request.POST.get('issue_id')

	today = date.today()
	current_date = today.strftime("%d/%m/%Y")
	print("date =",current_date)

	obj1=Book_issue.objects.get(issue_id=int(issue_id))
	obj1.i_date=current_date
	get_rack_number=obj1.rack_number
	get_book_name=obj1.book_name
	obj1.status="Issued"
	obj1.save()

	obj100=Books.objects.get(book_name=get_book_name)
	input_val=obj100.identifer

	string_input_val=str(input_val)

	string_get_rack_number=str(get_rack_number)
	print("MY RACK NUMBER ::::>>>>>>",get_rack_number)
	print("Type : ",type(string_get_rack_number))


	client.publish("librarymanagement",string_input_val)


	#get_rack_number (RACK NUMBER SENT TO MQTT)

	return HttpResponse("<script>alert('Book Issued Successfully');window.location.href='/get_issue_requests_admin/'</script>")



def deny(request):
	issue_id=request.POST.get('issue_id')
	obj1=Book_issue.objects.get(issue_id=int(issue_id))
	obj1.delete()
	return HttpResponse("<script>alert('Deleted Successfully');window.location.href='/get_issue_requests_admin/'</script>")


@never_cache
def view_issue_details_admin(request):
	if 'uid' in request.session:
		req_list=Book_issue.objects.filter(status="Issued")

		return render(request,'view_issue_details_admin.html',{'req': req_list}) 
	else:
		return render(request,'login.html')


@never_cache
def get_return_requests_admin(request):
	if 'uid' in request.session:
		req_list=Book_return.objects.filter(status="Pending")

		return render(request,'get_return_requests_admin.html',{'req': req_list}) 
	else:
		return render(request,'login.html')

def verify(request):
	issue_id=request.POST.get('issue_id')
	b_id=request.POST.get('b_id')
	book_name=request.POST.get('book_name')
	name=request.POST.get('name')
	i_date=request.POST.get('i_date')
	rack_number=request.POST.get('rack_number')

	today = date.today()
	current_date = today.strftime("%d/%m/%Y")
	print("date =",current_date)


	obj1=Book_return.objects.get(issue_id=int(issue_id),book_name=book_name,name=name,status="Pending")
	obj1.r_date=current_date
	get_rack_number=obj1.rack_number
	get_my_book_name=obj1.book_name
	obj1.status="Returned"
	obj1.save()

	obj100=Books.objects.get(book_name=get_my_book_name)
	output_val=obj100.identifer
	int_output_val=int(output_val)
	final_val=int_output_val+1

	string_output_val=str(final_val)



	obj20=Book_issue.objects.get(issue_id=int(issue_id))
	obj20.delete()

	string_get_rack_number=str(get_rack_number)


	# client.publish("librarymanagement","my rack") 

	client.publish("librarymanagement", string_output_val) 

	#get_rack_number (RACK NUMBER SENT TO MQTT) {rack_number}

	return HttpResponse("<script>alert('Return Request Accepted');window.location.href='/get_return_requests_admin/'</script>")
	

@never_cache
def view_return_details_admin(request):
	if 'uid' in request.session:
		req_list=Book_return.objects.filter(status="Returned")

		return render(request,'view_return_details_admin.html',{'req': req_list}) 
	else:
		return render(request,'login.html')



@csrf_exempt
def register(request):
	name=request.POST.get("name")
	username=request.POST.get("username")
	address=request.POST.get("address")
	age=request.POST.get("age")
	email=request.POST.get("email")
	password=request.POST.get("password")

	response_data={}
	try:
		d = Requests.objects.filter(username=username)
		c = d.count()
		if c == 1:
			response_data['msg'] = "Already registered, Wait for Approval"
		else:
		    ob=Requests(name=name,username=username,address=address,email=email,password=password,age=age)
		    ob.save()

		    response_data['msg'] = "yes"
	except:
	    response_data['msg'] = "no"
	return JsonResponse(response_data)



@csrf_exempt
def find_login(request):
	username=request.POST.get("username")
	password=request.POST.get("password")

	try:
		ob=Users.objects.get(username=username,password=password)

		data={"msg":"User"}
		return JsonResponse(data,safe=False)
	except:
		data={"msg":"no"}
		return JsonResponse(data,safe=False)



@csrf_exempt
def get_user_details(request):
 
	username=request.POST.get("username")
	resplist=[]
	respdata={}
	ob=[Users.objects.get(username=username)]

	resplist=[]
	respdata={}
	for i in ob:
	    data={}
	    data["username"]=i.username
	    data["email"]=i.email
	    data["address"]=i.address
	    data["password"]=i.password
	    data["age"]=i.age
	    data["name"]=i.name

	    resplist.append(data)

	respdata["data"]=resplist
	print(respdata)
	return JsonResponse(respdata,safe=False)


@csrf_exempt
def update_user_details(request):
	username=request.POST.get("username")
	name=request.POST.get("name")
	email=request.POST.get("email")
	age=request.POST.get("age")
	password=request.POST.get("password")
	address=request.POST.get("address")
	print("username :::>>> ",username)


	response_data={}
	obj1=Users.objects.get(name=name)
	obj1.email=email
	obj1.age=age
	obj1.password=password
	obj1.address=address
	obj1.save()

	response_data['msg'] = "yes"

	return JsonResponse(response_data)



@csrf_exempt
def search_book_user(request):
	book_name=request.POST.get("book_name")
	book_name=book_name.lower()
	print(len(book_name))
	book_name=book_name.strip()
	print("Book name : ",book_name)
	print(type(book_name))
	print(len(book_name))
	try:
		resplist=[]
		respdata={}
		ob=[Books.objects.get(book_name=book_name)]

		resplist=[]
		respdata={}
		for i in ob:
		    data={}
		    data["b_id"]=i.b_id
		    data["book_name"]=i.book_name
		    data["author_name"]=i.author_name
		    data["publication"]=i.publication
		    data["year"]=i.year

		    resplist.append(data)

		respdata["data"]=resplist
		print(respdata)
		return JsonResponse(respdata,safe=False)
	except:
		respdata={"data":"no"}
		return JsonResponse(respdata,safe=False)


@csrf_exempt
def request_book(request):
	username=request.POST.get("username")
	book_name=request.POST.get("book_name")

	print(username,book_name)

	try:
		ob=Users.objects.get(username=username)
		my_name=ob.name

		ob1=Books.objects.get(book_name=book_name)
		my_book_id=ob1.b_id
		my_rack_number=ob1.rack_number

		
		current_date=""

		obj8=Book_issue.objects.filter(b_id=my_book_id,book_name=book_name,rack_number=my_rack_number,name=my_name)
		co=obj8.count()
		if co==1:
			obj11=Book_issue.objects.get(b_id=my_book_id,book_name=book_name,rack_number=my_rack_number,name=my_name)
			get_status=obj11.status
			if get_status=="Pending":
				data={"msg":"You are in pending list"}
				return JsonResponse(data,safe=False)
			else:
				data={"msg":"Already issued"}
				return JsonResponse(data,safe=False)
		else:
			# global issue
			status="Pending"
			obj10= Book_issue(b_id=my_book_id,book_name=book_name,rack_number=my_rack_number,name=my_name,i_date=current_date,status=status)
			obj10.save()
			# issue=issue+1

			data={"msg":"Success"}
			return JsonResponse(data,safe=False)
	except:
		data={"msg":"no"}
		return JsonResponse(data,safe=False)



@csrf_exempt
def get_my_books(request):
	username1=request.POST.get("username")

	obj100=Users.objects.get(username=username1)
	get_name=obj100.name

	resplist=[]
	respdata={}
	ob=Book_issue.objects.filter(name=get_name,status="Issued")
	for j in ob:
	    issue_id=j.issue_id
	    b_id=j.b_id
	    book_name=j.book_name
	    rack_number=j.rack_number
	    i_date=j.i_date
	    status=j.status

	    data={}
	    data["issue_id"]=issue_id
	    data["b_id"]=b_id
	    data["book_name"]=book_name
	    data["rack_number"]=rack_number
	    data["i_date"]=i_date
	    data["status"]=status

	    resplist.append(data)
	print(resplist)

	respdata["data"]=resplist
	print(respdata)
	return JsonResponse(respdata,safe=False)



@csrf_exempt
def get_info(request):
	b_id=request.POST.get("value")
	username=request.POST.get("username")

	obj30=Users.objects.get(username=username)
	get_name=obj30.name
	try:
		blk1=Book_issue.objects.get(b_id=int(b_id),name=get_name)
		issue_id=blk1.issue_id
		b_id=blk1.b_id
		book_name=blk1.book_name
		rack_number=blk1.rack_number
		i_date=blk1.i_date
		status=blk1.status

		if status=="Issued":

			data={}
			respdata={}
			resplist=[]
			data["issue_id"]=issue_id
			data["b_id"]=b_id
			data["book_name"]=book_name
			data["rack_number"]=rack_number
			data["i_date"]=i_date
			data["status"]=status

			resplist.append(data)

			respdata["data"]=resplist

			return JsonResponse(respdata,safe=False)
		else:
			respdata={"data":"no"}
			return JsonResponse(respdata,safe=False)
	except:
		respdata={"data":"not issued"}
		return JsonResponse(respdata,safe=False)

@csrf_exempt
def return_book(request):
	username=request.POST.get("username")
	book_name=request.POST.get("book_name")
	issue_id=request.POST.get("issue_id")
	b_id=request.POST.get("b_id")
	i_date=request.POST.get("i_date")
	rack_number=request.POST.get("rack_number")

	# try:
	ob=Users.objects.get(username=username)
	my_name=ob.name

	# ob1=Book_return.objects.get(book_name=book_name)
	# my_book_id=ob1.b_id
	# my_rack_number=ob1.rack_number

	
	current_date=""
	status="Pending"
	obj8=Book_return.objects.filter(b_id=b_id,issue_id=issue_id,book_name=book_name,rack_number=rack_number,name=my_name,i_date=i_date,status=status)
	co=obj8.count()
	if co==1:
		
		data={"msg":"You are in pending list"}
		return JsonResponse(data,safe=False)
	else:
		# global issue
		obj10= Book_return(b_id=b_id,issue_id=issue_id,book_name=book_name,rack_number=rack_number,name=my_name,i_date=i_date,r_date=current_date,status=status)
		obj10.save()
		# issue=issue+1

		data={"msg":"Success"}
		return JsonResponse(data,safe=False)
	# except:
	# 	data={"msg":"no"}
	# 	return JsonResponse(data,safe=False)



@csrf_exempt
def get_my_return_books(request):
	username1=request.POST.get("username")

	obj100=Users.objects.get(username=username1)
	get_name=obj100.name

	resplist=[]
	respdata={}
	ob=Book_return.objects.filter(name=get_name,status="Returned")
	for j in ob:
		return_id=j.return_id
		issue_id=j.issue_id
		b_id=j.b_id
		book_name=j.book_name
		rack_number=j.rack_number
		i_date=j.i_date
		r_date=j.r_date
		status=j.status

		data={}
		data["return_id"]=return_id
		data["issue_id"]=issue_id
		data["b_id"]=b_id
		data["book_name"]=book_name
		data["rack_number"]=rack_number
		data["i_date"]=i_date
		data["r_date"]=r_date
		data["status"]=status

		resplist.append(data)
	print(resplist)

	respdata["data"]=resplist
	print(respdata)
	return JsonResponse(respdata,safe=False)

@never_cache
def display_admin_scan_book(request):
	if 'uid' in request.session:

		return render(request,'admin_scan_book.html',) 
	else:
		return render(request,'login.html')



@never_cache
def admin_scan_book(request):
	print("hai")
	
	cap = cv2.VideoCapture('http://192.168.29.132:8081/video')#('rtsp://192.168.29.132:8081/1')
	# cap = cv2.VideoCapture(0)
	# initialize the cv2 QRCode detector
	detector = cv2.QRCodeDetector()


	while True:
		_, img = cap.read()
		# print(img)
		# detect and decode
		data, bbox, _ = detector.detectAndDecode(img)
		# check if there is a QRCode in the image
		if data:
			book_id=data
			break

		cv2.imshow("QRCODEscanner", img)
		if cv2.waitKey(1) == ord("q"):
			break
	cap.release()
	cv2.destroyAllWindows()

	print("Book id : ",book_id)
	book_details=Books.objects.get(b_id=int(book_id))
	# print(book_details)
	# print(book_details.book_name)
	try:
		issue_details=Book_issue.objects.filter(b_id=int(book_id))
	except:
		issue_details=[Book_issue.objects.filter(b_id=int(book_id))]

	return render(request,'scan_details.html',{'book_detail': book_details,'issue_detail':issue_details}) 


##############  mqtt start ############



def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    client.subscribe("librarymanagement")


def on_message(client, userdata, msg):##############
    print(msg.topic+" -- "+str(msg.payload))

    # tag_id=str(msg.payload)[2:-1]       #rfid extracting

    pass

client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
def run(n):
    client.loop_start()
t1 = threading.Thread(target=run, args=(10,))
t1.start()
t1.join()

##############  mqtt end ############
