import os, sys

def main():
    os.system('start cmd /K python QBASIC.py validAccounts.txt transactionSummary/transactionSummary0.txt')
    os.system('start cmd /K python QBASIC.py validAccounts.txt transactionSummary/transactionSummary1.txt')
    os.system('start cmd /K python QBASIC.py validAccounts.txt transactionSummary/transactionSummary2.txt')
    print("Hit 'Enter' to begin end of day processing...")
    input()
    mergeTransactions()
    # Run back office on mergedTransactionSummary.txt
    os.system('python QBASIC_Backend.py masterAccounts.txt mergedTransactionSummary.txt')
    clearTransactionSummary(os.path.join(sys.path[0], 'transactionSummary/transactionSummary0.txt'))
    clearTransactionSummary(os.path.join(sys.path[0], 'transactionSummary/transactionSummary1.txt'))
    clearTransactionSummary(os.path.join(sys.path[0], 'transactionSummary/transactionSummary2.txt'))

def clearTransactionSummary(filePath):
    open(filePath, 'w').close()

def mergeTransactions():
    mergedTransactions = []
    mergedTransactions = mergedTransactions + readTransactionSummaryFile(os.path.join(sys.path[0], 'transactionSummary/transactionSummary0.txt'))
    mergedTransactions = mergedTransactions + readTransactionSummaryFile(os.path.join(sys.path[0], 'transactionSummary/transactionSummary1.txt'))
    mergedTransactions = mergedTransactions + readTransactionSummaryFile(os.path.join(sys.path[0], 'transactionSummary/transactionSummary2.txt')) + ["EOS"]
    writeMergedTransactions(mergedTransactions, os.path.join(sys.path[0], 'mergedTransactionSummary.txt'))

def writeMergedTransactions(mergedTransactions, filePath):
    try:
        file = open(filePath, 'w')
    except IOError:
        print("Cannot open " + filePath)
    else:
        if (len(mergedTransactions) == 0):
            file.write('')
        else:
            for index in range(0, len(mergedTransactions)):
                file.write(mergedTransactions[index] + '\n')
    file.close()

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

main()
