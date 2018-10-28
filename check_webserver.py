import sys
import subprocess



def menu():
        
       	print("1. Check nginx status")
        print("0. Quit")

        selection=int(input("Enter choice: "))
        if selection==1:
                check_nginx()
        elif selection==0:
                exit
        else: 
                print("Not a valid option")
                menu()

def check_nginx():
        print("Checking nginx status.......")
        p=subprocess.run('sudo service nginx status', shell=True)
        if p.returncode != 0:
        	ask_to_start_nginx()
        else: 
        	exit

def ask_to_start_nginx():
        print("Do you want to start nginx?")
        print("1. Yes")
        print("0. No")
        selection=int(input("Enter choice: "))
        if selection==1:
        	p=subprocess.run('sudo service nginx start',shell=True)
        elif selection==0:
        	exit
        else:
        	print("Invalid choice")
        	ask_to_start_nginx()
#main Process
menu()