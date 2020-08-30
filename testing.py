import Log_entry
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

dict, dict2 = Log_entry.Find_pattern()
print("Data: ")
print(dict)
print(" ")
print(dict2)