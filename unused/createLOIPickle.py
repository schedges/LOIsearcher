# Creates pickled list of LOIs. Format of list is [["Frontier","Filename","Text"]].
#
# Only included to show how pickled data set was created, you do not need to run this
# if LOIs.pickle already exists.
#
# Assumes the folder this script is called from contains subfolders corresponding to the
# frontier names filled with PDFs.
import os
import pdfplumber
import string
import re
import pickle

#These should be subfolders in the directory this script is called from
frontiers=["AF","CF","CommF","CompF","EF","IF","NF","RF","TF","UF"]

outfile="LOIs.pickle"

#List to hold LOIs
loiList=[]

#Step through frontier folders
for frontier in frontiers:

  #Make sure it's a folder
  if os.path.isdir(frontier):
    #Get all PDF files
    files = [i for i in os.listdir(frontier) if i.endswith(".pdf")]
    files.sort()
    
    #Step through PDF files
    for i,file in enumerate(files):
    
      #User feedback
      if i%10==0:
        print("On file "+str(i)+" of "+str(len(files))+" of frontier "+frontier)
        
      #Open PDF
      try:
        pdf = pdfplumber.open(frontier+"/"+file)
      except:
        pass
        
      #Get pages
      pages = pdf.pages
      
      #Make string to hold text
      string=""
      
      #Step through pages adding text to string
      for page in pages:
        string+=page.extract_text(x_tolerance=1)
        
      #Remove newline
      string=string.replace("\n"," ")
      
      #Remove extra white spaces--not sure this is necessary.
      string=" ".join(string.split())
        
      #Add to list
      loiList.append([frontier,file,string])
      
#Write file
f = open(outfile,'wb')
pickle.dump(loiList,f)
f.close()

