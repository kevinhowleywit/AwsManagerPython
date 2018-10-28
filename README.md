# AwsManagerPython
Manage aws ec2 instances and s3 buckets with this code. 

Developer Operations assignment 1 - Kevin Howley 20078896.
Some code taken from developer operations lab work provided by lecturers. 


This submission contains 3 python scripts: run_newwebserver.py, check_machine_status.py, check_webserver.py.
The run_newwebserver.py can create, list and terminate ec2 instances.
It can create, empty and delete s3 buckets. An image can be uploaded to the s3 bucket and is automatically put on the ec2's nginx webserver. 
It uploads monitoring scripts to the instance when that function is called. 

When the program runs it prints a menu and you must pick the number relative to the option you want to use. 
The key is not hard coded. The key you specify when it asks for it, must be already in your options of keys within to start instances. 
When an instance starts, it automatically goes in to the default security group. I have this set allow all traffic in. You may need to adjust your default one to allow the program to function properly. When the ec2 instance starts up, there is a config file to install everything needed to allow the program to function properly. You may need to wait a few minutes for all the required packages to install. 

The buckets that get created through this program are going to be set to public and the same with the objects that get uploaded to them.
When you upload an image, you must specify the an instance ip and the key relating to that instance. This is so it can build a command to run.  The bucket name and image name must also be specified. The image must be in the same directory as the python program that is being run. I have included testImage.jpg with this submission which you can test. The program will generate a link for you to go to s you can see the image in the nginx webserver. 

Another option is to upload monitoring scripts. This gives some basic information about the machine and its current status. It also checks whether nginx is running or not. If it isnt it asks whether you would like to start it.  
