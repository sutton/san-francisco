'''

Create the counties topojson 

shapefile from http://www.arcgis.com/home/item.html?id=2f227372477d4cddadc0cd0b002ec657

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
import numpy as np

## Get Daily Population File 
popDensity = pd.read_csv("data/county_population_density.csv",header=0,converters={"Unnamed: 0": lambda x: str(x)})
popDensity.index = popDensity["Unnamed: 0"]
popDensity["Population Density (SQ MILES)"] = popDensity["POP10"]/(popDensity["AREA (SQUARE FT)"] *.0000000358701)

## Get only the following counties
counties = ['001','013','041','055','075','081','085','095','097']

driver  = ogr.GetDriverByName('ESRI Shapefile') 
dataSource = driver.Open("data/CA_counties/CA_counties.shp")    # Get the contents of the shape file
layer = dataSource.GetLayer(0)    													# Get the shape file's first (and only) layer

## Get the output Layer's Feature Definition
featureDefn = layer.GetLayerDefn()

outDriver = ogr.GetDriverByName('GeoJSON')
outDataSource = outDriver.CreateDataSource('county.json')
outLayer = outDataSource.CreateLayer('county.json', geom_type=ogr.wkbPolygon )

## create a new feature
outFeature = ogr.Feature(featureDefn)
for c in counties:
	layer.SetAttributeFilter("COUNTYFP = '%s'" % c)
	
	## Set new geometry
	for feature in layer:
			geom = feature.GetGeometryRef()
			outFeature.SetField('COUNTYFP',c)
			outFeature.SetField('COUNTYNS',popDensity.ix[c]["Population Density (SQ MILES)"])
			outFeature.SetGeometry(geom)

			# Add new feature to output Layer
			outLayer.CreateFeature(outFeature)

			# destroy the feature
			outFeature.Destroy

outDataSource.Destroy()
