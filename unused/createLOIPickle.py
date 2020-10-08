import os
import pdfplumber
import string
import re
import pickle

frontiers=["AF","CF","CommF","CompF","EF","IF","NF","RF","TF","UF"]


outfile="LOI_db.zip"
loiList=[]

#Step through frontier folders
for frontier in frontiers:

  if os.path.isdir(frontier): #Make sure it's a folder
    #Get all PDF files
    files = [i for i in os.listdir(frontier) if i.endswith(".pdf")]
    files.sort()
    
    #Step through PDF files
    for i,file in enumerate(files):
    
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
      #Remove extra white spaces--is this necessary?
      string=" ".join(string.split())
        
      #Add to list
      loiList.append([frontier,file,string])
      
#Write file
f = open(outfile,'wb')
pickle.dump(loiList,f)
f.close()

