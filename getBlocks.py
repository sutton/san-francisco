'''

Find the block ids which are part of the following counties

Alameda 001
Contra Costa 013 
Marin 041 
Napa 055
San Francisco 075
San Mateo 081
Santa Clara 085
Solano 095
Sonoma 097

'''
from osgeo import ogr, osr
import pandas as pd

counties = ['001','013','041','055','075','081','085','095','097']
blocks = []
areas = []
pops = []

driver  = ogr.GetDriverByName('ESRI Shapefile') 
dataSource = driver.Open("data/tabblock2010_06_pophu/tabblock2010_06_pophu.shp")    # Get the contents of the shape file
layer = dataSource.GetLayer(0)    													# Get the shape file's first (and only) layer
destSR = osr.SpatialReference()

for c in counties:
	layer.SetAttributeFilter("COUNTYFP10 = '%s'" % c)

	for feature in layer:
		blocks.append(feature.GetField("BLOCKID10"))
		pops.append(feature.GetField("POP10"))
		geom = feature.GetGeometryRef()
		if not geom.IsEmpty():                 										# re-projection to get area in square meters 
			if str(feature.GetField("POP10")).isdigit():
				EPSG = 2226						   									# NAD83 / California zone 2 (ftUS)
				destSR.ImportFromEPSG(EPSG)        
				geom.TransformTo(destSR)           									# re-project
				areas.append(geom.GetArea())


df = pd.DataFrame({"BLOCKID10": blocks, "AREA (SQUARE FT)": areas,"POP10":pops})
df.to_csv("data/BLOCKID10.csv",index=False)
