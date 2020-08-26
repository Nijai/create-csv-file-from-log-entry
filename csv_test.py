# Python program to convert  
# CSV to HTML Table 
  
  
import pandas as pd 


def Convert_start(filename, newfilename):
	# to read csv file named "samplee" 
	print("Creating HTML file named: ", newfilename)
	a = pd.read_csv(filename) 
  
	# to save as html file 
	# named as "Table" 
	a.to_html(newfilename) 
  
	# assign it to a  
	# variable (string) 
	html_file = a.to_html() 