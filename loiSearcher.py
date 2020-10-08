# Run from same folder as LOIs.pickle. Searches LOI text for search word, and
# returns results with most occurrences of that word. Input a frontier to limit
# search, otherwise searches all LOIs.
#
# Can edit nResultsToShow to change number of results shown
# Can edit nPreviewChars to change how many characters are shown for results.
# Can set caseSensitive to 1 for case sensitive search results
import pickle

#For bolding text. From https://stackoverflow.com/a/17303428
class color:
  BOLD = '\033[1m'
  END = '\033[0m'

#How many results to show
nResultsToShow=10

#How many preview words to show
nPreviewChars=400

#Require case sensitivity
caseSensitive=0

#Open input file
inpFilename="LOIs.pickle"
f = open(inpFilename, 'rb')

#Load loiList, three columns: Frontier, Filename, Text
loiList = pickle.load(f)

#Ask user if they want to limit search to a specific frontier
frontiers=["AF","CF","CommF","CompF","EF","IF","NF","RF","TF","UF"]
try:
  print(color.BOLD+"\nFrontier choices: "+str(frontiers[:]))
  frontierToSearch=input("Enter fronter to search (blank for all):\n"+color.END)
  frontierToSearch=frontierToSearch.strip("'")
  frontierToSearch=frontierToSearch.strip('"')
except SyntaxError:
  pass
  
#Make subset of frontiers to search if requested
if frontierToSearch in frontiers:
  loiList = [loiList[i] for i in range(0,len(loiList)) if loiList[i][0]==frontierToSearch]

#Ask user what word to search for
try:
  searchWord=input(color.BOLD+"Enter word or phrase to search (case-insenstive):\n"+color.END)
except SyntaxError:
  pass

#Step through LOIs, searching for word (case insensitive).
matchingLOIs=[]
for loi in loiList:
  if caseSensitive==1:
    nTimes = loi[2].count(searchWord)
  else:
    nTimes = loi[2].lower().count(searchWord.lower())
  if nTimes>0:
    matchingLOIs.append([loi[0],loi[1],loi[2],nTimes])
    
#Sort by number of occurrences of the search word
matchingLOIs.sort(key = lambda x: x[3])
matchingLOIs.reverse()
print(color.BOLD+"\nFound "+str(len(matchingLOIs))+" matching LOIs"+color.END)

print("\n====================")
print("===SEARCH RESULTS===")
print("====================")

#Update results to display if fewer than nResultsToShow
if len(matchingLOIs)<nResultsToShow:
  nResultsToShow=len(matchingLOIs)
  
#Display top results
for i in range(0,nResultsToShow):
  #Check there are enough characters to display the intended preview length. If not, shorten it.
  if len(matchingLOIs[i][2]) < nPreviewChars:
    charsToDisplay=len(matchingLOIs[i][2])
  else:
    charsToDisplay=nPreviewChars
    
  #Print the Frontier - Filename
  print(color.BOLD +"\n"+str(i+1)+". "+matchingLOIs[i][0]+" - "+matchingLOIs[i][1] + color.END)
  print(matchingLOIs[i][2][0:charsToDisplay])
f.close()
