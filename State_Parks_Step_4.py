#State Parks Step 4
##Combining rasters for multiple scored attributes into a composite score


import arcpy, time
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.extent="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster = "D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"


#eo_raster="D:\\GIS Projects\\StateParks\\EO_Processing.gdb\\EO_Raster_Scores_test_4_w_0"
#eo_raster="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_con"
#eo_raster="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_w_0"
eo_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_norm"
#resilience_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\Reslieince_NY_snap_0"
#matrix_forest_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\Matrix_binary_w_0"
#EDM_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\EDM_total_Richness_reclass"
#EDM_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_update_total_Richness"
#LCA_norm_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\LCA_inverse_norm_w_0"
#linkage_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\Linkage_w_0"
resilience_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\New_TNC_Scored"
forestblock_and_linkage_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Matrix_Forest_Scores_Complete"
#EDM_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_update_Richness_noNULL"
LCA_norm_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\LCA_inverse_norm_w_0_max_1"

#EDM_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_hyp345_norm_no0_for_add"
EDM_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_hyp344_norm_no0_for_add"

####Convert LCA, EDM, EO (0-10,0-40,0-2081) to 0-1
#LCA_norm_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\LCA_inverse_norm_w_0"
#eo_raster="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_w_0"
##input=LCA_norm_raster
##input=EDM_raster
#input=eo_raster
#ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
#ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
#print ras_min
#print ras_max
#
#max=float(ras_max[0])
#min=float(ras_min[0])
#
#range=max-min
#minus_data=arcpy.sa.Minus(input,0)
##reclass_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\LCA_inverse_norm_w_0")*1.0/(range)*1.0
##reclass_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_update_total_Richness")*1.0/(range)*1.0
#reclass_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_w_0")*1.0/(range)*1.0
#out_put_reclass=input+"_max_1"
#reclass_input.save(out_put_reclass)
#
#eo_raster="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_w_0_max_1"
#EDM_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_update_total_Richness_max_1"
#LCA_norm_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\LCA_inverse_norm_w_0_max_1"
#
#input=LCA_norm_raster
#ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
#ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
#print ras_min
#print ras_max
#



#component_list=[eo_raster,resilience_raster,matrix_forest_raster,EDM_raster,LCA_norm_raster,linkage_raster]
#component_list=[eo_raster,matrix_forest_raster,EDM_raster,LCA_norm_raster,linkage_raster]
component_list=[eo_raster,forestblock_and_linkage_raster,EDM_raster,LCA_norm_raster,resilience_raster]

##Check that all rasters have same column, rows, no NODATA values and are aligned
for in_raster in component_list:
    print in_raster
    print arcpy.GetRasterProperties_management(in_raster,"COLUMNCOUNT")
    print arcpy.GetRasterProperties_management(in_raster,"ROWCOUNT")
    print arcpy.GetRasterProperties_management(in_raster,"ANYNODATA")
    print arcpy.GetRasterProperties_management(in_raster,"BOTTOM")
    print arcpy.GetRasterProperties_management(in_raster,"MAXIMUM")
    print arcpy.GetRasterProperties_management(in_raster,"MINIMUM")
    
    
## Weight Matrix Forest Blocks by 25, Linkages by 15, and add rest togeter
wrk="D:\\GIS Projects\\StateParks\\Results.gdb\\"
out_name="Comprehensive_Score_Equal_Weight" 
out_raster=wrk+out_name   
#comp_score=(25*arcpy.sa.Raster(matrix_forest_raster))+(15*arcpy.sa.Raster(linkage_raster))+arcpy.sa.Raster(eo_raster)+arcpy.sa.Raster(resilience_raster)+arcpy.sa.Raster(EDM_raster)+arcpy.sa.Raster(LCA_norm_raster)

#comp_score=(25*arcpy.sa.Raster(matrix_forest_raster))+(15*arcpy.sa.Raster(linkage_raster))+arcpy.sa.Raster(eo_raster)+arcpy.sa.Raster(EDM_raster)+arcpy.sa.Raster(LCA_norm_raster)
out_name="Comprehensive_Score_Equal_Weight" 
out_raster=wrk+out_name   

comp_score=(2.0*arcpy.sa.Raster(matrix_forest_raster))+2.0*(arcpy.sa.Raster(linkage_raster))+2.0*arcpy.sa.Raster(eo_raster)+2.0*arcpy.sa.Raster(EDM_raster)+2.0*arcpy.sa.Raster(LCA_norm_raster)



out_name="Comprehensive_Score_1_1_5_2_1" 
out_raster=wrk+out_name   

comp_score=(1.0*arcpy.sa.Raster(matrix_forest_raster))+1.0*(arcpy.sa.Raster(linkage_raster))+5.0*arcpy.sa.Raster(eo_raster)+2.0*arcpy.sa.Raster(EDM_raster)+1.0*arcpy.sa.Raster(LCA_norm_raster)


comp_score.save(out_raster)

out_name="Comprehensive_Score_05_05_6_2_1" 
out_raster=wrk+out_name   

comp_score=(0.5*arcpy.sa.Raster(matrix_forest_raster))+0.5*(arcpy.sa.Raster(linkage_raster))+6.0*arcpy.sa.Raster(eo_raster)+2.0*arcpy.sa.Raster(EDM_raster)+1.0*arcpy.sa.Raster(LCA_norm_raster)


comp_score.save(out_raster)


out_name="Comprehensive_Score_05_05_10_2_1" 
out_raster=wrk+out_name   

comp_score=(0.5*arcpy.sa.Raster(matrix_forest_raster))+0.5*(arcpy.sa.Raster(linkage_raster))+10.0*arcpy.sa.Raster(eo_raster)+2.0*arcpy.sa.Raster(EDM_raster)+1.0*arcpy.sa.Raster(LCA_norm_raster)


comp_score.save(out_raster)

out_name="Comprehensive_Score_025_025_10_4_1" 
out_raster=wrk+out_name   

comp_score=(0.25*arcpy.sa.Raster(matrix_forest_raster))+0.25*(arcpy.sa.Raster(linkage_raster))+10.0*arcpy.sa.Raster(eo_raster)+4.0*arcpy.sa.Raster(EDM_raster)+1.0*arcpy.sa.Raster(LCA_norm_raster)


comp_score.save(out_raster)

####Adding in Resilience
wrk="D:\\GIS Projects\\StateParks\\Results.gdb\\"
out_name="Comprehensive_Score_05_10_4_1_1_July21" 
out_raster=wrk+out_name   

comp_score=(0.5*arcpy.sa.Raster(forestblock_and_linkage_raster))+10.0*arcpy.sa.Raster(eo_raster)+4.0*arcpy.sa.Raster(EDM_raster)+1.0*arcpy.sa.Raster(LCA_norm_raster)+1.0*arcpy.sa.Raster(resilience_raster)


comp_score.save(out_raster)

out_name="Comprehensive_Score_1_10_4_1_1_July18" 
out_raster=wrk+out_name   

comp_score=(1*arcpy.sa.Raster(forestblock_and_linkage_raster))+10.0*arcpy.sa.Raster(eo_raster)+4.0*arcpy.sa.Raster(EDM_raster)+1.0*arcpy.sa.Raster(LCA_norm_raster)+1.0*arcpy.sa.Raster(resilience_raster)


comp_score.save(out_raster)




out_name="Comprehensive_Score_025_10_4_1_1" 
out_raster=wrk+out_name   

comp_score=(0.25*arcpy.sa.Raster(forestblock_and_linkage_raster))+10.0*arcpy.sa.Raster(eo_raster)+4.0*arcpy.sa.Raster(EDM_raster)+1.0*arcpy.sa.Raster(LCA_norm_raster)+1.0*arcpy.sa.Raster(resilience_raster)


comp_score.save(out_raster)


out_name="Comprehensive_Score_025_10_4_05_05" 
out_raster=wrk+out_name   

comp_score=(0.25*arcpy.sa.Raster(forestblock_and_linkage_raster))+10.0*arcpy.sa.Raster(eo_raster)+4.0*arcpy.sa.Raster(EDM_raster)+0.50*arcpy.sa.Raster(LCA_norm_raster)+0.50*arcpy.sa.Raster(resilience_raster)


comp_score.save(out_raster)




##Check raster

print arcpy.GetRasterProperties_management(comp_score,"COLUMNCOUNT")
print arcpy.GetRasterProperties_management(comp_score,"ROWCOUNT")
print arcpy.GetRasterProperties_management(comp_score,"ANYNODATA")
print arcpy.GetRasterProperties_management(comp_score,"MINIMUM")
print arcpy.GetRasterProperties_management(comp_score,"MAXIMUM")
print arcpy.GetRasterProperties_management(eo_raster,"MAXIMUM")


arcpy.sa.Rank()

comp_score.save(out_raster)

##Evaluate scores at state park level
tax_parcels="C:\\Users\\akconley\\Downloads\\NYS_Tax_Parcels_Shareable_Public_2015_0923.gdb\\NYS_Tax_Parcels_Shareable_Public\NYS_Tax_Parcels_Shareable_Public"
state_park_features="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\State_Parks_no_inholdings_dissolve"
state_park_features="D:\\GIS Projects\\StateParks\\oprhp.shp"
state_park_features="D:\\GIS Projects\\StateParks\\oprhp_16_diss.shp"
alterna_raster="D:\\GIS Projects\\StateParks\\Results.gdb\\Comprehensive_Score_6_03_2016_w_0"

out_raster="D:\\GIS Projects\\StateParks\\Results.gdb\\Comprehensive_Score_05_10_4_1_1_July21"
print arcpy.GetRasterProperties_management(out_raster,"COLUMNCOUNT")
out_table=wrk+"State_Park_Scores_0510411_July21"
#out_table=wrk+"Tax_Parcel_Score_w_TNC"
arcpy.sa.ZonalStatisticsAsTable(state_park_features,"NAME",out_raster,out_table)


out_raster="D:\\GIS Projects\\StateParks\\Results.gdb\\Comprehensive_Score_025_10_4_1_1"
out_table=wrk+"State_Park_Scores_02510411"
arcpy.sa.ZonalStatisticsAsTable(state_park_features,"NAME",out_raster,out_table)


out_raster="D:\\GIS Projects\\StateParks\\Results.gdb\\Comprehensive_Score_025_10_4_05_05"
out_table=wrk+"State_Park_Scores_0251040505"
arcpy.sa.ZonalStatisticsAsTable(state_park_features,"NAME",out_raster,out_table)

###Generate 1 mile buffer around parls
input_parks=state_park_features
output_parks="D:\\GIS Projects\\StateParks\\Results.gdb\\State_Parks_1mile"
distance="1 Miles"
type="OUTSIDE_ONLY"

arcpy.Buffer_analysis(input_parks,output_parks,distance,type)


#arcpy.sa.ZonalStatisticsAsTable(tax_parcels,"OBJECTID",alterna_raster,out_table)
 #State Parks Component Scores
#
wrk="D:\\GIS Projects\\StateParks\\Results.gdb\\"
state_park_features="D:\\GIS Projects\\StateParks\\oprhp_16_diss.shp"
components=[eo_raster,resilience_raster,forestblock_and_linkage_raster,EDM_raster,LCA_norm_raster]
components=[EDM_raster]

for raster in components:
    if "EO" in raster:
        name="EO_score"
    if "TNC" in raster:
        name="TNC_score"
    if "Matrix" in raster:
        name="MFB_and_Linkage_score"
    if "EDM" in raster:
        name="EDM_score_344"
    if "LCA" in raster:
        name="LCA_Score"
    print name
    out_table=wrk+"State_Parks_Scores_"+name
    arcpy.sa.ZonalStatisticsAsTable(state_park_features,"NAME",raster,out_table)

###Spatial Join
eo_to_join="D:\\GIS Projects\\StateParks\\EO_Processing.gdb\\Scored_EOs_test"
eo_to_join="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\EO_pieces_w_Scores"
eo_to_join="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EOs"

out_features=wrk+"State_Parks_Contributing_EO_6_16_2016"

arcpy.SpatialJoin_analysis(state_park_features,eo_to_join,out_features,"JOIN_ONE_TO_MANY")

############Add area in top 10, 5,1, 05, 01%
top_ten="D:\\GIS Projects\\StateParks\\State_Parks_Tables\\state_parks_10_percent.csv"
top_five="D:\\GIS Projects\\StateParks\\State_Parks_Tables\\state_parks_5_percent.csv"
top_one="D:\\GIS Projects\\StateParks\\State_Parks_Tables\\state_parks_1_percent.csv"
top_05="D:\\GIS Projects\\StateParks\\State_Parks_Tables\\state_parks_05_percent.csv"
top_01="D:\\GIS Projects\\StateParks\\State_Parks_Tables\\state_parks_01_percent.csv"

tables=[top_ten,top_five,top_one,top_05,top_01]
for table in tables:
    for field in arcpy.ListFields(table): print field.name

state_parks="D:\\GIS Projects\\StateParks\\oprhp_16_diss.shp"
for field in arcpy.ListFields(state_parks): print field.name

start="D:\\GIS Projects\\StateParks\\BIG_State_Parks_Table.csv"
out_table=wrk+"State_Parks_Big_Table"
arcpy.CopyRows_management(start,out_table)



for table in tables:
    
    if "10_percent" in table:
        name="Area_Top_10_percent"
    if "_5_percent" in table:
        name="Area_Top_5_percent"
    if "_1_percent" in table:
        name="Area_Top_1_percent"
    if "_05_percent" in table:
        name="Area_Top_05_percent"
    if "_01_percent" in table:
        name="Area_Top_01_percent"
    print table
    print name
    out_table=wrk+name
    arcpy.CopyRows_management(table,out_table)
    

top_ten="D:\\GIS Projects\\StateParks\\Results.gdb\\Area_Top_10_percent"
top_five="D:\\GIS Projects\\StateParks\\Results.gdb\\Area_Top_5_percent"
top_one="D:\\GIS Projects\\StateParks\\Results.gdb\\Area_Top_1_percent"
top_05="D:\\GIS Projects\\StateParks\\Results.gdb\\Area_Top_05_percent"
top_01="D:\\GIS Projects\\StateParks\\Results.gdb\\Area_Top_01_percent"
tables=[top_ten,top_five,top_one,top_05,top_01]
state_parks="D:\\GIS Projects\\StateParks\\Results.gdb\\State_Parks_Big_Table"

for field in arcpy.ListFields(state_parks): print field.name

for table in tables:
    
    if "10_percent" in table:
        name="Area_Top_10_percent"
    if "_5_percent" in table:
        name="Area_Top_5_percent"
    if "_1_percent" in table:
        name="Area_Top_1_percent"
    if "_05_percent" in table:
        name="Area_Top_05_percent"
    if "_01_percent" in table:
        name="Area_Top_01_percent"
    print table
    print name
    out_table=wrk+name
    arcpy.JoinField_management(state_parks,"Name",table,"NAME",name)
    
for table in tables:
    
    if "10_percent" in table:
        name="Area_Top_10_percent"
        new_name="Prop_Top_10_percent"
    if "_5_percent" in table:
        name="Area_Top_5_percent"
        new_name="Prop_Top_5_percent"
    if "_1_percent" in table:
        name="Area_Top_1_percent"
        new_name="Prop_Top_1_percent"
    if "_05_percent" in table:
        name="Area_Top_05_percent"
        new_name="Prop_Top_05_percent"
    if "_01_percent" in table:
        name="Area_Top_01_percent"
        new_name="Prop_Top_01_percent"
    #arcpy.AddField_management(state_parks,new_name,"FLOAT")
    expression= "(!"+str(name)+"!)*1.0/(!Comp_Score_AREA!)*1.0"
    print expression
    arcpy.CalculateField_management(state_parks,new_name,expression,"PYTHON")