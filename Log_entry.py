import re
import sys
import csv
import operator
from collections import OrderedDict 
import csv_test as c


def csv_file_creater(filename, fields, csv_data):
	# writing to csv file  
	with open(filename, 'w', newline='') as csvfile:  
		# creating a csv writer object  
		csvwriter = csv.writer(csvfile)  
        
		# writing the fields  
		csvwriter.writerow(fields)  
        
		# writing the data rows  
		csvwriter.writerows(csv_data) 
	c.Convert_start(filename, filename+".html")
	csv_data.clear()
	fields.clear()
	

def user_statistics_csv(per_user, fields):
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
	csv_file_creater(filename, fields, data_csv)

def error_count_csv(error):
	val2 = 0
	fields = []
	fields.append("Error")
	fields.append("Count")
	filename = "error_message.csv"
	csv_file_creater(filename, fields, error)


def Find_pattern():
	dict = {}
	dict2 ={}
	fields = []
	fields.append("Username")
	with open("test.txt", "r+") as f:
		lines = f.readlines()
		for line in lines:			
			if re.search(r"INFO ([\w ]*) ", line) != None:
				result = re.search(r"INFO ([\w ]*) ", line)   #msg after info
				count = result[0].find('O')
			elif re.search(r"ERROR ([\w ]*) ", line) != None:
				result = re.search(r"ERROR ([\w ]*) ", line) #msg after ERROR
				count = result[0].find('OR')
				#r=result[0][0:count+2]   #ERROR
				dict2[str(result[0][count+2:-1]).strip()] = dict2.get(str(result[0][count+2:-1]).strip(),0)+1
			else: 
				continue
				
				
			result3= re.search(r" \([a-z.]+?\)", line) #USername
			
			if result3[0][2:-1] not in dict:   #result3[0][2:-1] is Username
				r=result[0][0:count+2] #INFO/ERROR
				dict[result3[0][2:-1]] = {str(r): dict.get(str(r),0)+1}
				print("Unique User: ", result3[0][2:-1], "with new ",r," No.:", dict.get(str(r),0)+1)
				print(" ")	
				if str(r) not in fields :
					fields.append(str(r))
			else:
				r=result[0][0:count+2] #INFO/ERROR			
				for k1,v1 in dict.items():
					for k2, v2 in v1.items():
						if str(result3[0][2:-1]).strip() == str(k1).strip() and r == str(k2):
							dict[result3[0][2:-1]].update({str(r): dict.get(str(r),v2)+1})
							print("Existing User: ", k1, "with new ",r," No.: ", dict.get(str(r),v2)+1)
							print(" ")
							break
						elif str(result3[0][2:-1]).strip() == str(k1).strip() and r not in v1:
							dict[result3[0][2:-1]].update({str(r): dict.get(str(r),0)+1})
							print("Existing User: ", k1, "with new ",r," No.: ", dict.get(str(r),0)+1)
							print(" ")
							break
						
				if str(r) not in fields :
					fields.append(str(r))
	per_user = sorted(dict.items())
	error = sorted(dict2.items(), key=lambda x: x[1], reverse=True)
	user_statistics_csv(per_user, fields)
	error_count_csv(error)

 
Find_pattern()
