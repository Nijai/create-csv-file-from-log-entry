import re
import sys
import csv
import operator
from collections import OrderedDict 
import csv_test as c
import time
from multiprocessing import Pool, TimeoutError, Process, freeze_support, Lock
import os
import subprocess
import multiprocessing
import psutil




def csv_file_creater(filename, fields, csv_data):
	# writing to csv file 
	with open(filename, 'w', newline='') as csvfile:  
		# creating a csv writer object  
		csvwriter = csv.writer(csvfile)  
        
		# writing the fields  
		csvwriter.writerow(fields)  
        
		# writing the data rows  
		csvwriter.writerows(map(lambda x: [x], csv_data)) 
	c.Convert_start(filename, filename+".html")
	csv_data.clear()
	
	

def user_statistics_csv(per_user):
	""" Function which cook data for preparation of user_statistics_csv file"""
	val1 = 0
	val2 = 0
	data_csv = []
	
	for k1,v1 in per_user:
		for k2, v2 in v1.items():
			if str(k2).strip() == 'INFO':
				val1 = int(v2) + val1
			elif str(k2).strip() == 'ERROR':
				val2 = int(v2) +val2
		data_csv.append([str(k1),val1,val2])
		val1 = 0
		val2 = 0
	
	filename = "user_statistics.csv"
	#print("Calling csv_file_creater in user_statistics_csv")
	#print(" ")
	csv_file_creater(filename, fields_user_message(), data_csv)

def error_count_csv(error):
	""" Function which cook data for preparation of error_count_csv file"""
	#Function to keep track of Types of Error and their No. of occurrences. 
	val2 = 0
	filename = "error_message.csv"
	#print("Calling csv_file_creater in error_count_csv")
	csv_file_creater(filename, fields_error_message(), error)

def fields_error_message():
	#print("feilds2 appending")
	fields2 = []
	fields2.append("Error")
	fields2.append("Count")
	return fields2


def fields_user_message():
	#print("feilds appending")
	fields = []
	fields.append("Username")
	fields.append("INFO")
	fields.append("ERROR")
	return fields



def Find_pattern(lines):
	""" Function to find specific pattern in log file."""
	dict = {}
	dict2 ={}
	fields = []
	fields.append("Username")
	
	for line1 in lines:	
		for line in line1 :	
			if re.search(r"INFO ([\w ]*) ", line) != None:
				r = "INFO"
				keyword1= (re.search(r" \(([a-z.]+?)\)", line)).group(1) #Username
			elif re.search(r"ERROR ([\w ]*) ", line) != None:
				r = "ERROR"
				keyword = "ERROR"
				before_keyword, keyword, after_keyword = line.partition(keyword)
				keyword1 = (re.search(r"\(([a-z.]+?)\)", after_keyword)).group(0)
				before_keyword1, keyword1, after_keyword1 = after_keyword.partition(keyword1)
				keyword1 = (re.search(r"\(([a-z.]+?)\)", after_keyword)).group(1)
				dict2[str(before_keyword1).strip()] = dict2.get(str(before_keyword1).strip(),0)+1   #Counter of Error messages. 
			else: 
				continue
				
			
			if keyword1 not in dict:   #if Username not in dictionary 
				dict[keyword1] = {str(r): dict.get(str(r),0)+1} #New User
				#print("Unique User: ", keyword1, "with new ",r," No.:", dict.get(str(r),0)+1)
			else:		
				for k1,v1 in dict.items():
					for k2, v2 in v1.items():
						if keyword1 == str(k1).strip() and r == str(k2):
							#print("Existing User: ", k1, "with incremented ",r," No.: ", dict.get(str(r),v2)+1, "was ", v2)
							dict[keyword1].update({str(r): dict.get(str(r).strip(),v2)+1})
							#Existing user with incremented INFO/ERROR msg.
							break
						elif keyword1 == str(k1).strip() and r not in v1:
							#print("Existing User: ", k1, "with new ",r," No.: ", dict.get(str(r),0)+1, "was ", v2)
							dict[str(keyword1).strip()].update({str(r): dict.get(str(r).strip(),0)+1})   #Existing user with new INFO/ERROR.
							break	
	per_user = sorted(dict.items()) #Sort dict alphabetically by Username
	error = sorted(dict2.items(), key=lambda x: x[1], reverse=True) #Sorting dict2 in reverse order of count
	user_statistics_csv(per_user) 
	error_count_csv(error)

 
if __name__ == '__main__':
	start_time = time.time()
	freeze_support()
	with open("test.txt", "r+") as f:
			lines = f.readlines() 
	n = int(len(lines) / (multiprocessing.cpu_count() - 2))
	data = [lines[i:i + n] for i in range(0, len(lines), n)]
	Find_pattern(data)
	print("--- %s seconds ---" % (time.time() - start_time))
	process = psutil.Process(os.getpid())
	print(process.memory_info().rss)
	