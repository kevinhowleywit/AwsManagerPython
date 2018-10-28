#!/usr/bin/env python3
#part of the code in some functions was inspired by the labs for this module.
import sys
import boto3
import botocore
import paramiko
import time
import subprocess
import webbrowser

#Main menu. prints out a list. User responds with a number
def mainMenu():
	print("1. Create EC2 instance")
	print("2. Create S3 bucket")
	print("3. Terminate EC2 instance")
	print("4. List EC2 instance")
	print("5. Delete S3 bucket")
	print("6. Put Image in bucket")
	print("7. List Buckets")
	print("8. Delete Bucket Contents")
	print("9. Copy up monitoring scripts")
	print("0. Quit")

	selection=int(input("Enter choice: "))
	if selection==1:
		createEC2()
	elif selection==2:
		createS3()
	elif selection==3:
		terminateEC2()
	elif selection==4:
		listEC2()
	elif selection==5:
		terminateS3()
	elif selection==6:
		putImage()
	elif selection==7:
		listBuckets()
	elif selection==8:
		deleteBucketContents()
	elif selection==9:
		copyScripts()
	
	elif selection==0:
		exit
	else:
		print("Invalid choice.....")
		mainMenu()

def createEC2():
#function to create instance in default security group
	print("Specify the existing key name")
	key_name=input()
#key must already exist in aws
	print("Creating EC2......... ")

	ec2 = boto3.resource('ec2')
	instance = ec2.create_instances(
    ImageId='ami-047bb4163c506cd98',
    MinCount=1,
    MaxCount=1,
    SecurityGroups=['default'],
    UserData='''#!/bin/bash
                sudo yum update -y
                sudo yum install python36 -y
                sudo yum install nginx -y
                sudo service nginx start
                touch /home/ec2-user/testfile''',
    KeyName=key_name,
    InstanceType='t2.micro')


	print ("An instance with ID", instance[0].id, "has been created.")
	time.sleep(5)
	instance[0].reload()
	





	print (instance[0].id)
	print("Public IP:  ", instance[0].public_ip_address)

	print("")
	mainMenu()

def createS3():
	#creates a bucket with user specified name
	s3 = boto3.resource("s3")
	print("Enter the bucket name")
	bucket_name = input()
	print("Bucket will be named " + bucket_name)
	print("")
	try:
		response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint':'eu-west-1'}, ACL="public-read")
		print("Creating S3 .....")
		print(response)

	except Exception as error:
		print(error)

	mainMenu()

def terminateS3():
	#terminates a bucket that the user specifies
	s3 = boto3.resource("s3")
	print("Enter the name of the bucket to be deleted")
	bucket_name = input()
	bucket = s3.Bucket(bucket_name)
	try:
		response=bucket.delete()
		print("Deleting Bucket......")
		print(response)
		print("")
	except Exception as error:
		print(error)

	mainMenu()

def putImage():
	s3=boto3.resource("s3")
	#user must specify the name of the bucket and the image
	#image must be in the directory of the of this file 
	print("Specify the name of the bucket")
	bucket_name=input()
	print("")
	print("Specify the name of the image")
	object_name=input()
	#key paired with the instance must be here to allow the scp commands to work
	print("Specify the KeyName")
	key_name=input()
	#the ip must be specified to allow the command to happen below
	print("Specify the public ip of the instance to put the image")
	public_ip=input()
	try:
		response=s3.Object(bucket_name,object_name).put(Body=open(object_name,'rb'), ACL="public-read")
		#print(response)
		#sleeps and generates a link to the image uploaded
		#sleep to allow time for it to upload
		print("........................")
		print("Wait 10 seconds for link")
		time.sleep(10)
		#this is the generated link for the image
		link_image = "https://s3-eu-west-1.amazonaws.com/"+bucket_name+"/"+object_name
		print(link_image)
		print("creating nginx page with image.........")
		#generates a html with the img source set to get the image from the s3 bucket
		subprocess.run("echo '<html lang='en'><head><meta charset='utf-8'><title>The HTML5 Herald</title></head><body><h1>Image</h1><img src='" + link_image + "'></</body></html>' >  index1.html", check=True,shell=True)
		#scp the generated html up to the nginx directory
		#waits 3 seconds to allow the file to be generated
		time.sleep(3)
		subprocess.run("scp -i "+key_name+".pem index1.html ec2-user@"+public_ip+":.",check=True,shell=True)
		time.sleep(3)
		#move_command
		subprocess.run("ssh -i "+key_name+".pem ec2-user@"+public_ip+" sudo mv index1.html /usr/share/nginx/html",shell=True)
		#tells the user to navigate to the nginx webpage
		print("Navigate to "+public_ip+"/index1.html")
	
		

	except Exception as error:
		print(error)


	mainMenu()

def deleteBucketContents():
	s3 = boto3.resource("s3")
	#function empties the bucket contents which allows it to be deleted later
	print("Enter the bucket name you want to empty")
	bucket_name = input()
	bucket = s3.Bucket(bucket_name)
	for key in bucket.objects.all():
		try:
			response=key.delete()
			print(response)
		except Exception as error:
			print(error)


	mainMenu()



def listBuckets():
	#function lists the buckets 
	s3 = boto3.resource("s3")
	for bucket in s3.buckets.all():
		print(bucket.name)
		print("----")

		try:
			#this also lists the items in all the buckets negating the need for a seperate list contents function
			for item in bucket.objects.all():
				print(item.key)

		except:
			print("Access denied")

	mainMenu()


def terminateEC2():
	#terminates the ec2 instace
	#user must specify the the id to allow this to take place
	print("Enter the instance id please: ")
	instance_id=input()
	print("")
	print(instance_id)
	print("")
	ec2 = boto3.resource('ec2')
	instance = ec2.Instance(instance_id)
	response = instance.terminate()
	print("Terminating instance.......")
	print("")
	print(response)
	print("")



	mainMenu()

def listEC2():
	#prints the state of instances, the public dns and the public ipv4 address
	ec2 = boto3.resource('ec2')
	for instance in ec2.instances.all():

		print(instance.id, instance.state)
		print(instance.public_dns_name)
		print(instance.public_ip_address)

	print("")
	mainMenu()

#old function now integrated into my list buckets function
#def listBucketContents():
#	s3 = boto3.resource("s3")
#	print("enter the name of the bucket to check")
#	bucket_name=input()
#	bucket = s3.Bucket(bucket_name)
#
#	for object in bucket.objects.all():

  
 #   		print(object.key)

def copyScripts():
	#user must specify the key to allow the command to work
	print("Specify the key name")
	key_name=input()
	#specify the ip of the instance to build the command
	print("Specify the public IP of the instance.")
	public_ip=input()
	#cmd2 = "scp -i Assignment1KeyPair.pem check_webserver.py ec2-user@" + ip_address + ":"
	#using the parameters, it copies up the scripts to check status of the machine and a script to check is nginx running
	copycommand="scp -i "+key_name+".pem check_webserver.py check_machine_status.py ec2-user@"+public_ip+":."
	print(copycommand)
	
	runcommand1= "ssh -i "+key_name+".pem ec2-user@"+public_ip+" python3 check_machine_status.py"

	runcommand2= "ssh -i "+key_name+".pem ec2-user@"+public_ip+" python3 check_webserver.py"

	p=subprocess.run(copycommand,shell=True)
	time.sleep(2)
	subprocess.run(runcommand1,shell=True)
	time.sleep(2)
	subprocess.run(runcommand2,shell=True)
	mainMenu()

#main routine
mainMenu()
