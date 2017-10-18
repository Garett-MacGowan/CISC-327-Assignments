def main():
	sessionType = login()
	validAccountsList = readAccounts("") # Eventually this will be pulled from the backend.
	# Need to add a loop so that it keeps asking for valid input until it gets some
	transaction = input("Please enter a transaction code: ")
	if (transaction == "createacct"):
		if (sessionType == "machine"):
			print("Sorry, this transaction is unauthorized.")
		else:
			createacct() # Add validAccountsList to function call
	if (transaction == "deleteacct"):
		if (sessionType == "machine"):
			print("Sorry, this transaction is unauthorized.")
		else:
			deleteacct()
	if (transaction == "deposit"):
		deposit(sessionType)

def login():
	start = input("Type & Enter 'login' to login:")
	while (start != "login"): # Do not accept any other input except 'login'
		start = input("Please log in:")
	type = input("What type of session would you like?")
	while ((type != "machine") and (type != "agent")): # Do not accept any other input except 'machine' or 'agent'
		type = input("What type of session would you like?")
	return type

def readAccounts(filePath):
	validAccountsList = []
	try:
		file = open(filePath, "r")
	except IOError:
		print("Cannot open " + filePath)
	else:
		for line in file:
			if line[0] == 0:
				print("Invalid accounts list!")
				print("Contact an administrator to fix backend accounts list creation!")
				quit()
			if len(line) != 7:
				print("Invalid accounts list!")
				print("Contact an administrator to fix backend accounts list creation!")
				quit()
			validAccountsList.append(line)
	return validAccountsList
			
def createacct():
	check1 = False
	check2 = False
	while (check1 == False):
		number = input("Enter a new account number: ")
		if ((str(number[0]) == "0") or (str(number[(len(number)-1)]) == "0")): 
			print("The account number cannot start or end with 0")
		if (len(str(number)) != 7): 
			print("Make sure that the account number is composed of 7 digits")
		# check to see if number is already in the account file (it shouldn't be)
		else:
			check1 = True
	while (check2 == False):
		name = input("Enter a name for the account: ")
		if (((len(name)) < 3) or ((len(name)) > 30)):
			print("The name has to be between 3 and 30 alphanumeric characters.")
		if (((str(name))[0] == " ") or ((str(name))[(len(name)-1)] == " "):
				print("The name cannot begin or end with a space")
		else:
				check2 = True
	# add number and name info to transaction summary file
	# don't allow any transaction on new account

def deleteacct():
	number = input("Enter the account number to be deleted: ")
	#check that number is valid (its in the account file)
	name = input("Enter the name of the account: ")
	#add number and name to the transaction summary file

def deposit(sessionType):
	check1 = False
	check2 = False
	while (check1 == False):
		number = input("Enter the account number that you would like to deposit from: ")
		#check that the account number is in the account file
	while (check2 == False):
		amount = input("Enter the amount that you would like to withdraw in cents: ")
		if ((sessionType == "machine") and (amount > 100000)):
			print("Depositing more than $1000 is not authorized in ATM mode")
		if ((sessionType == "agent") and (amount > 99999999)):
			print("Depositing more than $999,999.99 is not authorized.")
		else:
				check2 = True

# def withdraw():
# def transfer():
# def logout():

main()

# git add <filename>
# git commit -m "message"
# git push origin master