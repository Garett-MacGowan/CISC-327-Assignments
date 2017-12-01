import sys, os
# Authors:
# Garett MacGowan: 10197107
# Areege Chaudhary: 10197607

# Note: In-code comments refer to content below the comment.

# This program is a simple command line driven bank simulatior. The available functinality are logging in as machine or agent, creating acounts, deleting accounts,
# depositing, withdrawing, transfering funds, and logging out. This submission contains only front end work, and thus only some of the systems funcionality is live.
# The program is intended to be run from console, calling "python QBASIC.py validAccounts.txt transactionSummary.txt" where both .txt's are in the directory or a
# subdirectory of QBASIC.py. The program takes validAccounts.txt as an input, as well as transactionSummary.txt (the daily transaction summary file), to be updated
# with any transactions that occur during the session. transactionSummary.txt is the only output of the front-end.

# Main handles all calls to the transactions of the banking system. It ensures proper execution of the login and logout functios, while also allowing account transactions
# to take place when logged in. It also manages loading the valid accounts list and transaction summary file into memory for use in the session.
def main():
	# Neither machine session or agent session has been selected yet.
	sessionType = None
	# Since no session has been selected, begin login reqest phase.
	while sessionType == None:
		sessionType = login()
		# Eventually this will be pulled from the backend.
		validAccountsList = readAccounts(os.path.join(sys.path[0], sys.argv[1]))
		# Reads transaction summary file into easy-to-use list (necessary for implementing certain transaction constraints).
		transactionSummaryFile = readTransactionSummaryFile(os.path.join(sys.path[0], sys.argv[2]))
		sessionTransactionSummaryFile = []
		# When the session type has been selected, allow for transaction requests.
		while (sessionType != None):
			transaction = input("Please enter a transaction code:")
			if (transaction == "createacct"):
				if (sessionType == "machine"):
					print("Sorry, this transaction is unauthorized.")
				else:
					# Appends necessary information to transaction summary file.
					sessionTransactionSummaryFile.append(createacct(validAccountsList))
			elif (transaction == "deleteacct"):
				if (sessionType == "machine"):
					print("Sorry, this transaction is unauthorized.")
				else:
					sessionTransactionSummaryFile.append(deleteacct(validAccountsList))
			elif (transaction == "deposit"):
				sessionTransactionSummaryFile.append(deposit(sessionType, validAccountsList))
			elif (transaction == "withdraw"):
				# Passing sessionTransactionSummaryFile to limit withdraw amount per machine session.
				sessionTransactionSummaryFile.append(withdraw(sessionType, validAccountsList, sessionTransactionSummaryFile))
			elif (transaction == "transfer"):
				sessionTransactionSummaryFile.append(transfer(sessionType, validAccountsList))
			elif (transaction == "logout"):
				transactionSummaryFile = transactionSummaryFile + sessionTransactionSummaryFile + ["EOS"]
				# Passes the session transaction summary file to the logout function to be written to the daily transaction summary file.
				# print(transactionSummaryFile)
				logout(transactionSummaryFile, os.path.join(sys.path[0], sys.argv[2]))
				sessionType = None
			else:
				print("Not a valid transaction code. Please try again:")

# readAccounts handles the reading of the valid accounts file to memory so that it may be used by certain transactions to work within constraints.
# readAccounts returns a list containing all of the valid account numbers.
def readAccounts(filePath):
	validAccountsList = []
	# Try/catch handles errors in reading files.
	try:
		file = open(filePath, 'r')
	except IOError:
		print("Cannot open " + filePath)
	else:
		for line in file:
			# Detects faulty accounts file.
			currentLine = line.strip('\n')
			if (currentLine[0] == 0):
				print("Invalid accounts list!")
				print("Contact an administrator to fix backend accounts list creation!")
				quit()
			if (len(currentLine) != 7):
				print("Invalid accounts list!")
				print("Contact an administrator to fix backend accounts list creation!")
				quit()
			validAccountsList.append(currentLine)
	file.close()
	return validAccountsList

# readTransactionSummaryFile handles reading the transaction summary file into memory so that it may be used by certain transactions to work within constraints.
# readTransactionSummaryFile returns a list containing all of the transactions for the day.
def readTransactionSummaryFile(filePath):
	transactionSummaryFile = []
	try:
		file = open(filePath, 'r')
	except IOError:
		print("Cannot open " + filePath)
	else:
		for line in file:
			currentLine = line.strip('\n')
			if (currentLine == "EOS"):
				return transactionSummaryFile
			transactionSummaryFile.append(currentLine)
	file.close()
	return transactionSummaryFile

# This function prompts the user to start the session by entering 'login'. At this point, no other input
# but log in should be accepted. Once the user has successfully logged in, the function prompts the user
# to enter the type of session they would like. If their input is neither "machine" nor "agent", the function
# continues to prompt them until a valid input is recieved.
def login():
	start = input("Enter 'login' to login:")
	# Do not accept any other input except 'login'.
	while (start != "login"): 
		start = input("Please log in:")
	type = input("What type of session would you like?")
	# Do not accept any other input except 'machine' or 'agent'.
	while ((type != "machine") and (type != "agent")):
		type = input("What type of session would you like?")
	# Return information about the type of session it is.
	return type 

# This function takes an account file as a parameter. It asks the user for an account number and a name for the
# new account. It then checks to see if the account number is valid (doesn't start with a 0, is composed of 7 digits and
# is not already in the accounts file). Once a valid account number is recieved, the function asks for an account name 
# and checks to see if it is valid (is between 3 and 30 alphanumeric characters and doesn't begin or end with a space).
# Once a valid account name and number is recieved, the function adds a line to the transaction summary file.
def createacct(accountsFile):
	check1 = False
	check2 = False
	restart = False
	while (check1 == False):
		# Does not advance to next input prompt until a valid account number is recieved.
		number = input("Enter a new account number:")
		if (str(number[0]) == "0"): 
			print("The account number cannot start with 0.")
		elif (len(number) != 7): 
			print("Make sure that the account number is composed of 7 digits.")
		elif (number.isdigit() == False):
			print("The account number must be made up of digits.")
		else:
			for line in accountsFile: # Check to see if number is already in the account file.
				if (line == number):
					print("That account number is already in use!")
					restart = True
					break
			if (restart == True):
				continue
			else:
				check1 = True
			
	# Does not add to transaction summary file until a valid name is recieved.
	while (check2 == False):
		name = input("Enter a name for the account:")
		if (((len(name)) < 3) or ((len(name)) > 30)):
			print("The name must be within 3 and 30 characters long.")
		elif (((str(name))[0] == " ") or ((str(name))[(len(name)-1)] == " ")):
			print("The name cannot begin or end with a space.")
		elif (all(x.isalnum() or x == ' ' for x in name) == False):
			print("The name must be made up of alphanumeric characters only.")
		else:
			check2 = True
	# Create a string for a line in the transaction summary file.
	transactionLine = "NEW " + number + " 000" + " 0000000 " + name
	return transactionLine

# This function first asks the user for an account number. It then checks to see if that number is valid (it's in the 
# accounts file). After that, it asks for the corresponding account name and adds a line to the transaction summary file.
def deleteacct(accountsFile):
	check1 = False
	# Does not advance to next input prompt until a valid account number is recieved.
	while (check1 == False):
		number = input("Enter the account number to be deleted:")
		for line in accountsFile:
			if (line == number):
				check1 = True
		if (check1 == False):
			print("Cannot find that account in our system.")
	name = input("Enter the name of the account:")
	# Create a string for a line in the transaction summary file.
	transactionLine = "DEL " + number + " 000" + " 0000000 " + name
	return transactionLine

# This function asks for an account number to deposit to and checks to see if it is valid (its in the account file). It 
# then asks for an amount to deposit (in cents). After checking to see if that amount is valid (not more than $1000 in 
# ATM mode and not more than $999,999.99 in agent mode), it adds a line to the transaction summary file.
def deposit(sessionType, accountsFile):
	check1 = False
	check2 = False
	# Does not advance to next input until a valid input is recieved.
	while (check1 == False):
		number = input("Enter the account number that you would like to deposit to:")
		if (number == "0000000"):
			print("Cannot deposit to the special account number.")
			continue
		for line in accountsFile: # Check that the account number is in the account file.
			if (line == number):
				check1 = True
		if (check1 == False):
			print("Cannot find that account in our system.")
	# Does not advance to adding to transaction summary file until a valid input is recieved.
	while (check2 == False):
		amount = input("Enter the amount that you would like to deposit in cents:")
		if ((sessionType == "machine") and (int(amount) > 100000)):
			print("Depositing more than $1000 is not authorized in ATM mode.")
		elif ((sessionType == "agent") and (int(amount) > 99999999)):
			print("Depositing more than $999,999.99 is not authorized.")
		else:
			check2 = True
	# Create a string for a line in the transaction summary file.
	transactionLine = "DEP " + number + " " + amount + " 0000000 " + "***"
	return transactionLine

# checkSessionLimit checks to make sure that no more than $1000 has been withdrawn from a particular account during the
# current session. This function is used in the withdraw function when in ATM mode. If over $1000 has been withrawn from
# the account in the current session, the function returns False, otherwise, it returns True.
def checkSessionLimit(accountNumber, amount, sessionTransactionSummaryFile):
	withdrawnSum = 0
	for element in sessionTransactionSummaryFile:
		#Parse the line in the sessionTransactionSummary file into a list.
		currentElement = element.split(" ")
		# take the sum of the withdrawls for the given account number.
		if ((currentElement[0] == "WDR") and (currentElement[1] == accountNumber)):
			withdrawnSum += int(currentElement[2])
	# If the sum of the session withdrawls plus the requested withrawl amount exceeds 1000, return False.
	if ((withdrawnSum + amount) > 100000):
		return False
	else:
		return True

# This function asks for an account number to withdraw from and checks to see if it is valid (its in the account file). It 
# then asks for an amount to withdraw (in cents). After checking to see if that amount is valid (not more than $1000 in 
# ATM mode and not more than $999,999.99 in agent mode), it adds a line to the transaction summary file.
def withdraw(sessionType, accountsFile, sessionTransactionSummaryFile):
	check1 = False
	check2 = False
	# Does not advance to next input prompt until a valid input is recieved.
	while (check1 == False):
		number = input("Enter the account number that you would like to withdraw from:")
		# Check that the account number is in the account file.
		for line in accountsFile:
			if (line == number):
				check1 = True
		if (check1 == False):
			print("Cannot find that account in our system.")
	# Does not advance to writing in transaction summary file until a valid input is recieved.
	while (check2 == False):
		amount = input("Enter the amount that you would like to withdraw in cents:")
		if ((sessionType == "machine") and (int(amount) > 100000)):
			print("Withdrawing more than $1000 is not authorized in ATM mode.")
		elif ((sessionType == "agent") and (int(amount) > 99999999)):
			print("Withdrawing more than $999,999.99 is not authorized.")
		elif ((sessionType == "machine") and (checkSessionLimit(number, int(amount), sessionTransactionSummaryFile) == False)):
			print("You may not withdraw more than $1000 per ATM session.")
			continue
		else:
			check2 = True
	# Create a string for a line in the transaction summary file.
	transactionLine = "WDR " + number + " " + amount + " 0000000 " + "***"
	return transactionLine

# This function asks the user to input two account numbers and checks if they are valid (are in the accounts file). It
# then asks for a amount to be transferred and checks if it is valid (not greater than $1000 in ATM mode and not greater
# than $999,999.99 in agent mode). Once it recieves valid inputs, it adds a line to the transation summary file.
def transfer(sessionType, accountsFile):
	check1 = False
	check2 = False
	check3 = False
	# Does not advance to next input prompt until a valid account number is recieved.
	while (check1 == False):
		number1 = input("Enter the account number that you would like to transfer from:")
		for line in accountsFile:
			if (line == number1):
				check1 = True
		if (check1 == False):
			print("Cannot find that account in our system.")
	# Does not advance to next input prompt until a valid account number is recieved.
	while (check2 == False):
		number2 = input("Enter the account number that you would like to transfer to:")
		for line in accountsFile:
			if (line == number2):
				check2 = True
		if (check2 == False):
			print("Cannot find that account in our system.")
	# Does not add to transaction summary file until a valid amount value is recieved.
	while (check3 == False):
		amount = input("Enter the amount that you would like to transfer (in cents):")
		if ((sessionType == "machine") and (int(amount) > 100000)):
			print("Transferring more than $1000 is not authorized in ATM mode.")
		elif ((sessionType == "agent") and (int(amount) > 99999999)):
			print("Transferring more than $999,999.99 is not authorized.")
		else:
			check3 = True
	# Create a string for a line in the transaction summary file.
	transactionLine = "XFR " + number1 + " " + amount + " " + number2 + " ***"
	return transactionLine

# logout handles writing the new daily transaction summary file so that it may be used by the backend.
def logout(transactionSummaryFile, filePath):
	try:
		file = open(filePath, 'w')
	except IOError:
		print("Cannot open " + filePath)
	else:
		if (len(transactionSummaryFile) == 0):
			file.write('')
		else:
			for index in range(0, len(transactionSummaryFile)):
				file.write(transactionSummaryFile[index] + '\n')
	file.close()

main()
