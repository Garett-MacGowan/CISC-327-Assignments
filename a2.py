def main():
	sessionType = login()

	transaction = input("Please enter a transaction code: ")
	if (transaction == "createacct"):
		if (sessionType == "machine"):
			print("Sorry, this transaction is unauthorized.")
		else:
			createacct()
	

def login():
	start = input("Type & Enter 'login' to login:")
	while (start != "login"): #do not accept any other input except 'login'
		start = input("Please log in:")
	type = input("What type of session would you like?")
	while ((type != "machine") and (type != "agent")): #do not accept any other input except 'machine' or 'agent'
		type = input("What type of session would you like?")
	return type

#def readAccounts(file):

def createacct():
	if (type == "machine"):
		print("Sorry, this transaction is unauthorized.")
	else:
		number = input("Enter a new account number: ")
		if ((str(number[0]) == "0") or (str(number[(len(number)-1)]) == "0")): 
			print("The account number cannot start or end with 0")
		if (len(str(number)) != 7): 
			print("Make sure that the account number is composed of 7 digits")
		#check to see if number is already in the account file (it shouldn't be)
		name = input("Enter a name for the account: ")
		if (name)
		#check that length of account number is between 3 and 30 alphanumeric chars and that it doesnt begin or end with a space
		#add number and name info to transaction summary file
		#don't allow any transaction on new account
		transaction = input("Please enter a transaction code: ")

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