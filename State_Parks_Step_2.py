##Code to be used to prep the EO Polys layer for inclusion in State Parks Biodiversity Assessment
# The final scoring will be done at the pixel level, so it is necessary to convert the polygon layers to raster
# However, there are numerous polygons which overlap, so we need to first take those areas of intersection
# Planarize them, and ensure that their score represents the sum of the scores of all the EOs that overlap that space
#Then those regions need to be recombined with the regions of no overlap
#The final poly layer should have no overlapping polygons, and can be used to convert to a raster

#Steps: 1- Intersect on original EO poly layer to find areas with more than one EO
#Steps: 2 - Identify areas with no overlapping polygons using Original EO layer, Intersect_pieces, and the Symmetrical Differences command
# Steps: 3- Identical pieces layer will have multiple copes of the same polygone (one for each EO in that space) Reduce to single poly with Delete Identitical
#Steps: 4- Delete Fields_ clean up the intersect pieces layer by removing all fields
#Steps 5- Add Unique ID Field
#Steps 6- Populate Unique ID Field
#Steps 7- Spatial Join the Intersect_pieces with the Original EO layer to create copies of the interesect pieces for every EO that overlapps them,
# all with a commonon Unique ID
#Steps 7A- Try to dissolve the Spatial Join Polys on the Unique ID field and SUM the Score Field (This failed in ArcMap)
#Steps 7B- Create Summary Statistics Table on the Unique ID field Sum the Score, ADD a field to the Intersect_Pieces layer, AddJoin the SUM score Field to the Intersect Pieces
#Steps 8- Alter the field so that the Score Field is named "Raster_score" for the SymDif pieces and the intersect_pieces
#Steps 9- Merge the SymDif pieces and the Intersect Pieces
#Steps 10- Polygon to Raster

import arcpy, time
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
#arcpy.env.workspace="D:\\GIS Projects\\StateParks\\Base_Layers.gdb"
arcpy.env.workspace="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb"
#wrk="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\"
wrk="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\"
todlt=[]  ##Set up list of temp files to delete at end of script
#EO_originals="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EO_9_03_2015_layer"

#EO_originals="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EOs_No_Blank_No_VLAccuracy"
#EO_originals="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\statewide_EOs_October"
#EO_originals="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\EOs_input"
EO_originals="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\EOs_input_6_16"

snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.extent="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster = "D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"



##Step 0- sub set the original EO features to only include scored features
EO_working_features=wrk+"Scored_EOs"
score_field="Composite_Score"
where_expression=''' "EO_Initial_Score" IS NOT NULL   '''
arcpy.FeatureClassToFeatureClass_conversion(EO_originals,wrk,"Scored_EOs",where_expression)

#Step 1 Intersect (416 seconds)(257 seconds when eliminate EOs with null values in critical fields)(211)(237_May)(224)
start_time=time.time()
intersect_pieces=wrk+"EO_intersect_pieces"
todlt.append(intersect_pieces)  ##Mark this file for deletion

print intersect_pieces
in_features=[EO_working_features]
arcpy.Intersect_analysis(in_features,intersect_pieces,"ALL","","")
elapsed_time=time.time()-start_time
print elapsed_time

#Step 2 Create Sym Diff Layer (641 seconds)(221 seconds when eliminate EOs with null values in critical fields)(236)(205_May)(202)
start_time=time.time()
sym_dif_pieces=wrk+"EO_sym_dif_pieces"
todlt.append(sym_dif_pieces)  ##Mark this file for deletion
print sym_dif_pieces
arcpy.SymDiff_analysis(EO_working_features,intersect_pieces,sym_dif_pieces)
elapsed_time=time.time()-start_time
print elapsed_time

#Step 3 Delete Duplicates BUT SAVE a Complete_version of the intersect_pieces (671 seconds)(128 seconds)(236)(100_May)(102)
start_time=time.time()
intersect_pieces_complete=wrk+"intersect_pieces_complete"
todlt.append(intersect_pieces_complete)  ##Mark this file for deletion
arcpy.CopyFeatures_management(intersect_pieces,intersect_pieces_complete)
arcpy.DeleteIdentical_management(intersect_pieces,"Shape")

elapsed_time=time.time()-start_time
print elapsed_time

#Step 4 Delete Fields  ##Note, only keeping the FID field makes this step unncessary (134 seconds)(196)(27_May)(19)
start_time=time.time()
field_list=arcpy.ListFields(intersect_pieces_complete)
original_fields=[f.name for f in arcpy.ListFields(intersect_pieces_complete)]
fields_to_preserve=["OBJECTID","Shape_Area","Shape_Length","Shape"]
fields_to_delete=[f.name for f in arcpy.ListFields(intersect_pieces_complete) if f.name not in fields_to_preserve]

arcpy.DeleteField_management(intersect_pieces,fields_to_delete)
    
elapsed_time=time.time()-start_time
print elapsed_time


#Step 5 Add Unique ID Field (.5 seconds)(.2_May)(.43)
start_time=time.time()
in_features=intersect_pieces
arcpy.AddField_management(in_features,"Unique_ID","LONG")
elapsed_time=time.time()-start_time
print elapsed_time

#Step 6 Populate Unique ID Field (11.9 seconds)(3.5_May)(2.2)
start_time=time.time()
fc=intersect_pieces
count=0
with arcpy.da.UpdateCursor(fc,"Unique_ID") as cursor:
    for row in cursor:
        row[0]=count
        count+=1
        cursor.updateRow(row)
    


elapsed_time=time.time()-start_time
print elapsed_time


###test
#with arcpy.da.UpdateCursor(fc,"Unique_ID") as cursor:
#    for row in cursor:
#        print row

#Step 7 Spatial Join (1051 seconds)(226 seconds after restart)(324)(209_May)(231)
start_time=time.time()

in_features=intersect_pieces
join_features=intersect_pieces_complete
spatial_join_pieces=wrk+"Spatial_Join_pieces"
todlt.append(spatial_join_pieces)  ##Mark this file for deletion
arcpy.SpatialJoin_analysis(in_features,join_features,spatial_join_pieces,"JOIN_ONE_TO_MANY","","","ARE_IDENTICAL_TO")

elapsed_time=time.time()-start_time
print elapsed_time

###Step 7A Moment of truth- Will Dissolve Work in PYTHON? ANSWER: NO," Invalid Topology [Maximum tolerance exceeded.]" Error Proceed to 7B
###Check Names of Fields
#field_list=arcpy.ListFields(spatial_join_pieces)
#for field in field_list:
#    print field.name
#    
###For this test, the "score" field will be "Join_Count"
#start_time=time.time()   
#in_features=spatial_join_pieces
#dissolved_pieces=wrk+"dissolved_pieces"
#todlt.append(dissolved_pieces)  ##Mark this file for deletion
#dissolve_field="Unique_ID"
#statistics_fields=[["Join_Count","SUM"]]    
#
#arcpy.Dissolve_management(in_features,dissolved_pieces,dissolve_field,statistics_fields)
#elapsed_time=time.time()-start_time
#print elapsed_time

#Step 7B Create Summary Statistics Table, add Field and Join score Field to the Intersect_pieces class (63 seconds)(11 seconds)(24)(11.8_May)(10)
start_time=time.time()
in_features=spatial_join_pieces
summary_table=wrk+"Summary_Scores_Intersect"
statistics_fields=[["Join_Count","SUM"],[score_field,"SUM"]]   
case_field="Unique_ID"
arcpy.Statistics_analysis(in_features,summary_table,statistics_fields,case_field)
elapsed_time=time.time()-start_time
print elapsed_time

## Step 8 Join the Summary Score to the Intersect feature class ##Add the Raster_Score_field to intersect_pieces
#arcpy.AddField_management(intersect_pieces,"Raster_Score","LONG")
#
#Join the Fields (118 seconds)
start_time=time.time()
field_list=arcpy.ListFields(summary_table)
for field in field_list:
    print field.name
start_time=time.time()
output_score_field="SUM_"+score_field
fields=["SUM_Join_Count","FREQUENCY",output_score_field]
arcpy.JoinField_management(intersect_pieces,"Unique_ID",summary_table,"Unique_ID",fields)
elapsed_time=time.time()-start_time
print elapsed_time

#Step 9: Merge (19 seconds)
#Prep features for merge be ensuring they have the same name for their score field
#Clean up Field in Intersect Pieces
arcpy.AlterField_management(intersect_pieces,output_score_field,"Raster_Score")

###Temporary- for test, add the field to the SYM DIF pieces. In the actual process, there will already be a Raster_Score for each EO, and we will use that field

#arcpy.AddField_management(sym_dif_pieces,"Raster_Score","LONG")
#expression=1
#arcpy.CalculateField_management(sym_dif_pieces,"Raster_Score",expression,"PYTHON")

##Instead, rename score field to "Raster_Score"
arcpy.AlterField_management(sym_dif_pieces,score_field,"Raster_Score")

inputs=[intersect_pieces,sym_dif_pieces]
merged_scored_EO_pieces=wrk+"EO_pieces_w_Scores"

start_time=time.time()
arcpy.Merge_management(inputs,merged_scored_EO_pieces)
elapsed_time=time.time()-start_time
print elapsed_time
##Step 10 Convert the polygon to raster (43 seconds)
start_time=time.time()

#Check fields to make sure the desired field is there
#field_list=arcpy.ListFields(merged_scored_EO_pieces)
#for field in field_list:
#    print field.name

in_features=merged_scored_EO_pieces
value_field="Raster_Score"
scored_EO_raster=wrk+"Scored_EO_raster_6_16"
cell_assignment="MAXIMUM_COMBINED_AREA"
#cell_assignment="CELL_CENTER"
cell_size=30
arcpy.env.extent="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster = "D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.PolygonToRaster_conversion(in_features,value_field,scored_EO_raster,cell_assignment,"Raster_Score",cell_size)

elapsed_time=time.time()-start_time
print elapsed_time
#Cleanup
if 'todlt' in dir():         
    for dl in todlt:             
        try:                  
		arcpy.Delete_management(dl)             
        except:                 
            arcpy.AddWarning('Could not delete temporary data ' + str(dl))  