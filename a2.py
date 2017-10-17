def main():
	login()
	

def login():
	start = input("Type & Enter 'login' to login:")
	while (start != "login"): #do not accept any other input except 'login'
		start = input("Please log in:")
	type = input("What type of session would you like?")
	while ((type != "machine") and (type != "agent")): #do not accept any other input except 'machine' or 'agent'
		type = input("What type of session would you like?")
	#read accounts file

#def readAccounts(file):

def createacct(type):
	if (type == "machine"):
		print("Sorry, this transaction is unauthorized.")
	else:
		number = input("Enter a new account number: ")
		#check to see if number is 7 digits, doesnt begin with zero and isn't already in the account file
		name = input("Enter a name for the account: ")
		#check that length of account number is between 3 and 30 alphanumeric chars and that it doesnt begin or end with a space
		#add number and name info to transaction summary file
		#don't allow any transaction on new account

def deleteacct(type):
	if (type == "machine"):
		print("Sorry, this transaction is unauthorized.")
	else:
		number = input("Enter the account number to be deleted: ")
		#check that number is valid
		name = input("Enter the name of the account: ")
		#add number and name to the transaction summary file

# def deposit():
# def withdraw():
# def transfer():

main()
