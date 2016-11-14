'''

Parse through the .aux and .main origin / destination data sets to find the population there during the day

'''
import pandas as pd
import numpy as np 
import csv

blocks = pd.read_csv('data/BLOCKID10.csv',header=0,converters={"BLOCKID10": lambda x: str(x)})
blocks.index = blocks["BLOCKID10"].values

files = ['ca_od_aux_JT00_2014.csv','ca_od_main_JT00_2014.csv']

for file in files:

	with open('data/'+file, 'rb') as f:
		reader = csv.DictReader(f)
		
		for row in reader:
		
			work_block = row["w_geocode"]
			home_block = row["h_geocode"]
			total_jobs = row["S000"]
			
			if work_block in blocks.index:
				if work_block != home_block:
					population =  blocks.ix[work_block]["POP10"]
					blocks.loc[work_block,"POP10"] = population + int(total_jobs)
				else:
					pass
			else:
				pass
				
			if home_block in blocks.index:
				if work_block != home_block:
					population =  blocks.ix[home_block]["POP10"]
					blocks.loc[home_block,"POP10"] = population - int(total_jobs)
				else:
					pass
			else:
				pass
				
		f.close()
	
blocks.to_csv("data/BLOCKID10_corrected.csv")