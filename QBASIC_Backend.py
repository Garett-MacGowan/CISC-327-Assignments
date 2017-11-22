import sys, os

# Authors:
# Garett MacGowan: 10197107
# Areege Chaudhary: 10197607

# Note: In-code comments refer to content below the comment.

# This program is the back-end for QBASIC.py. It provides processing for the Master Accounts File, given a Transaction Summary File and the previous day's Master
# Accounts File. It ouputs a new Master Accounts file, as well as a new Valid Accounts file once all of the processing is completed. Transactions which are handled by
# the QBASIC_Backend.py include creating an account, deleting an account, depositing to an account, withdrawing from an account, and transferring from one account to another.
# QBASIC_Backend.py is intended to be run from console. It is called in the form "python QBASIC_Backend.py masterAccounts.txt transactionSummary.txt" where both .txt
# files are in the directory or a subdirectory of QBASIC_Backend.py.

# Main handles cycling through the transaction summary file and updating the master accounts file through the transaction handler functions. Once all of the transactions
# have been applied, the master accounts file and valid accounts file is written to the QBASIC_Backend.py directory.
def main():
    # Read the master accounts file and transaction summary files into lists.
    masterAccounts = readMasterAccounts(os.path.join(sys.path[0], sys.argv[1]))
    transactionSummary = readTransactionSummary(os.path.join(sys.path[0], sys.argv[2]))
    #print(masterAccounts)
    #print(transactionSummary)
    # Loop through the transactions in the transaction summary list and apply them to the master accounts list
    for index in range(0, len(transactionSummary)):
        transaction = transactionSummary[index][0]
        if (transaction == "DEP"):
            masterAccounts = depositHandler(masterAccounts, transactionSummary[index][1], transactionSummary[index][2])
        if (transaction == "WDR"):
            masterAccounts = withdrawHandler(masterAccounts, transactionSummary[index][1], transactionSummary[index][2])
        if (transaction == "XFR"):
            masterAccounts = transferHandler(masterAccounts, transactionSummary[index][1], transactionSummary[index][2], transactionSummary[index][3])
        if (transaction == "NEW"):
            masterAccounts = newAccHandler(masterAccounts, transactionSummary[index][1], transactionSummary[index][4])
        if (transaction == "DEL"):
            masterAccounts = deleteAccHandler(masterAccounts, transactionSummary[index][1], transactionSummary[index][4])
    writeValidAccounts(masterAccounts, os.path.join(sys.path[0], "newValidAccounts.txt"))
    writeMasterAccounts(masterAccounts, os.path.join(sys.path[0], "newMasterAccounts.txt"))

# depositHandler ensures the account that money is being deposited into is contained within the master accounts file and deposits the amount if the account is found.
# The function will log any errors that occur to standard output.
def depositHandler(masterAccounts, accountNum, amount):
    for index in range(0, len(masterAccounts)):
        if (masterAccounts[index][0] == accountNum):
            masterAccounts[index][1] = str(int(masterAccounts[index][1]) + int(amount))
            return masterAccounts
    print("Account number " + accountNum + " was not found.")
    return masterAccounts

# withdrawHandler ensures the account that money is being withdrawn from is contained within the master accounts file. If the account is found, it also checks that
# the account that is being withdrawn from will not go into negative balance after the withdraw. If the account doesn't go into negative balance, the money is withdrawn.
# The function will log any errors that occur to standard output.
def withdrawHandler(masterAccounts, accountNum, amount):
    for index in range(0, len(masterAccounts)):
        if (masterAccounts[index][0] == accountNum):
            if (int(masterAccounts[index][1]) - int(amount) < 0):
                print("Attempted to withdraw more than is available from account " + accountNum + ".")
                return masterAccounts
            else:
                masterAccounts[index][1] = str(int(masterAccounts[index][1]) - int(amount))
                return masterAccounts
    print("Account number " + accountNum + " was not found.")
    return masterAccounts

# transferHandler ensures that the accounts that money is being transferred between are contained within the master accounts file. If the account being withdrawn from does
# not go into a negative balance, and both accounts are found in the master accounts file, the money is transferred. The function will log any errors that occur to standard
# output.
def transferHandler(masterAccounts, accountNumOne, amount, accountNumTwo):
    accountOneFound = False
    accountTwoFound = False
    accountOneIndex = 0
    accountTwoIndex = 0
    index = 0
    while (accountOneFound == False and accountTwoFound == False and index < len(masterAccounts)):
        if (masterAccounts[index][0] == accountNumOne):
            accountOneIndex = index
            accountOneFound = True
        if (masterAccounts[index][0] == accountNumTwo):
            accountTwoIndex = index
            accountTwoFound = True
        index += 1
    if (accountOneFound == True and accountTwoFound == True):
        if (int(masterAccounts[accountOneIndex][1]) - int(amount) < 0):
            print("Attempted to trasfer more than is available from account " + accountNumOne + ".")
            return masterAccounts
        else:
            # Transferring specified amount.
            masterAccounts[accountOneIndex][1] = str(int(masterAccounts[accountOneIndex][1]) - int(amount))
            masterAccounts[accountTwoIndex][1] = str(int(masterAccounts[accountTwoIndex][1]) + int(amount))
            return masterAccounts
    else:
        if (accountOneFound == False):
            print("Account number " + accountNumOne + " was not found.")
        else:
            print("Account number " + accountNumTwo + " was not found.")
        return masterAccounts

# newAccHandler ensures that new account numbers are not already present in the master accounts file. If they are, an error message is logged to standard output. If the account
# number is not already existing, the new account is inserted in ascending order in the master accounts list.
def newAccHandler(masterAccounts, accountNum, accountName):
    # Checking if account number is already in use.
    if (len(masterAccounts) != 0):
        for index in range(0, len(masterAccounts)):
            if (masterAccounts[index][0] == accountNum):
                print("Cannot create account " + accountNum + ". It has already been taken.")
                return masterAccounts
    # Inserting new account in sorted order.
    if (len(masterAccounts) == 0):
            masterAccounts.append([accountNum, "0", accountName])
            return masterAccounts
    for index in range(0, len(masterAccounts)):
        if (int(masterAccounts[index][0]) > int(accountNum)):
            masterAccounts.insert(index-1, [accountNum, "0", accountName])
            return masterAccounts
        if (index == len(masterAccounts) - 1):
            masterAccounts.append([accountNum, "0", accountName])
            return masterAccounts

# deleteAccHandler ensures that the account requesting to be deleted is an existing account, and that the account doesn't have a positive balance before deleting it. Additionally,
# it checks whether the account name given matches the account number. If all of these checks pass, the account is deleted from the master accounts list.
def deleteAccHandler(masterAccounts, accountNum, accountName):
    for index in range(0, len(masterAccounts)):
        if (masterAccounts[index][0] == accountNum):
            if (masterAccounts[index][2] == accountName):
                if (int(masterAccounts[index][1]) == 0):
                    del masterAccounts[index]
                    return masterAccounts
                else:
                    print("Cannot delete account " + accountNum + ". It has a positive balance.")
                    return masterAccounts
            else:
                print("Cannot delete account " + accountNum + ". Account name: " + accountName + " does not match.")
                return masterAccounts
    print("Cannot delete account " + accountNum + ". Account was not found.")
    return masterAccounts

# writeMasterAccounts handles writing the new master accounts file as a .txt document, where the name and path of the document is defined in main. 
def writeMasterAccounts(masterAccounts, filePath):
    try:
       file = open(filePath, 'w')
    except IOError:
        print("Cannot open " + filePath)
    else:
        if (len(masterAccounts) == 0):
            file.write('')
        else:
            for index in range(0, len(masterAccounts)-1):
                currentAccount = ' '.join(masterAccounts[index])
                file.write(currentAccount + '\n')
            currentAccount = ' '.join(masterAccounts[index+1])
            file.write(currentAccount)
    file.close()

# writeValidAccounts handles writing the valid accounts to a .txt document, where the name and path of the document is defined in main.
def writeValidAccounts(masterAccounts, filePath):
    try:
       file = open(filePath, 'w')
    except IOError:
        print("Cannot open " + filePath)
    else:
        if (len(masterAccounts) == 0):
            file.write('')
        else:
            for index in range(0, len(masterAccounts)):
                file.write(masterAccounts[index][0] + '\n')
            file.write("0000000")
    file.close()

# readMasterAccounts returns a 2d array in the format [[accountNum, balance, accountName], [..., ..., ...]] which represents the contents of each line in the master accounts file.
def readMasterAccounts(filePath):
    masterAccounts = []
    try:
        file = open(filePath, 'r')
    except:
        print("Cannot open " + filePath)
    else:
        accountsRead = 0
        for line in file:
            currentLine = line.strip('\n')
            masterAccounts.append(currentLine.split(' '))
            # If the account name contains more than one word, ensure the words are contained within the same indice of the list.
            if (len(masterAccounts[accountsRead]) > 3):
                name = ' '.join(masterAccounts[accountsRead][2:len(masterAccounts[accountsRead])])
                masterAccounts[accountsRead][2] = name
                del masterAccounts[accountsRead][3:]
            accountsRead += 1
    file.close()
    return masterAccounts

# readTransactionSummary returns a 2d array in the format [[transactionCode, firstAccountNum, amount, secondAccountNum, accountName], [..., ..., ..., ..., ...]] which represents the contents
# of each line in the transaction summary file.
def readTransactionSummary(filePath):
    transactionSummary = []
    try:
        file = open(filePath, 'r')
    except:
        print("Cannot open " + filePath)
    else:
        transactionsRead = 0
        for line in file:
            currentLine = line.strip('\n')
            # If EOS is found, we are done.
            if (currentLine == "EOS"):
                continue
            transactionSummary.append(currentLine.split(' '))
            # If the account name contains more than one word, ensure the words are contained within the same indice of the list.
            if (len(transactionSummary[transactionsRead]) > 5):
                name = ' '.join(transactionSummary[transactionsRead][4:len(transactionSummary[transactionsRead])])
                transactionSummary[transactionsRead][4] = name
                del transactionSummary[transactionsRead][5:]
            transactionsRead += 1
    file.close()
    return transactionSummary

main()
