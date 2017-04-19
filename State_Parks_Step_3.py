##Step 3- Combining rasters for final score for State Parks

##Need to 1- Reclassify continuous rasters to 0-10
##2. combine rasters with appropriate weighting

##1 Calculate statistics for the rasters to be reclassified
import arcpy, time
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.env.workspace="D:\\GIS Projects\\StateParks\\Base_Layers.gdb"
wrk="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\"
todlt=[]  ##Set up list of temp files to delete at end of script
EO_originals="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EO_9_03_2015_layer"
snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster=snap_raster

forest_priority="D:\\GIS Projects\\StateParks\\ForestPriority_sc.tif"
proj_forest="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Forest_Priority_proj"
coordinate_system="D:\\GIS Projects\\Coordinate_Systems\\NAD 1983 UTM Zone 18N.prj"
arcpy.ProjectRaster_management(forest_priority,proj_forest,coordinate_system,"BILINEAR")

in_raster=proj_forest
inMaskData=snap_raster
outExtractByMask=arcpy.sa.ExtractByMask(in_raster,inMaskData)
outExtractByMask.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Forest_Priority_proj_clip")

MFB_new_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Forest_Priority_proj_clip"

##Step 0- sub set the original EO features to only include scored features
#EO_working_features=wrk+"Scored_EOs_test"
#score_field="EO_Initial_Score"

##Normalize the rasters using raster algebra
LCA_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
Resilience_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\TNC_Resilience"


input=LCA_raster
input=MFB_new_raster
ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
print ras_min
print ras_max

max=float(ras_max[0])
min=float(ras_min[0])

range=max-min
minus_data=arcpy.sa.Minus(input,0)
reclass_input=arcpy.Raster(MFB_new_raster)*1.0/(range)*1.0
out_put_reclass=input+"_norm"
reclass_input.save(out_put_reclass)
MFB_new_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Forest_Priority_proj_clip_norm"

input=MFB_new_raster
ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
print ras_min
print ras_max



input="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\TNC_Resilience"
ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
print ras_min
print ras_max

max=float(ras_max[0])
min=float(ras_min[0])

range=max-min
minus_data=arcpy.sa.Minus(input,0)
reclass_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\TNC_Resilience")*10.0/(range)*1.0
out_put_reclass=input+"_norm"
snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
reclass_input.save(out_put_reclass)
###Need to Project 

TNC_new="D:\\GIS Projects\\StateParks\\newTNC_resilience\\Resilience_3_23_2016\\Resilience_Data.gdb\\Resilience_Set_Eco_OR"
TNC_new_projected=wrk+"TNC_Resilience_proj"
in_raster=TNC_new
out_raster=TNC_new_projected
coordinate_sys="D:\\GIS Projects\\Coordinate_Systems\\NAD 1983 UTM Zone 18N.prj"

arcpy.ProjectRaster_management(in_raster,out_raster,coordinate_sys)

###Ooops! Accidentally reclassifed the entire eastern seabord. Need to clip first
clipped_Resilience=wrk+"TNC_Resilience_proj_clipped"
snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster=snap_raster
clipped_out=arcpy.sa.ExtractByMask(TNC_new_projected,LCA_raster)
clipped_out.save(clipped_Resilience)

##Now Normalize New York State Resilience
input="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Resilience_NY"
input=clipped_Resilience
ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
print ras_min
print ras_max

max=float(ras_max[0])
min=float(ras_min[0])

range=max-min
minus_data=arcpy.sa.Minus(input,0)
reclass_input=((arcpy.Raster(clipped_Resilience)-(min))*1.0)/(range)*1.0
out_put_reclass=input+"_norm"
snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster=snap_raster
reclass_input.save(out_put_reclass)

input=out_put_reclass

##Combine the Rasters with Weights and Save as New Raster
raster_list=arcpy.ListRasters()
linkage_raster=raster_list[5]
matrix_forest=raster_list[6]
eo_raster=raster_list[10]
LCA_raster=raster_list[12]
Resilience_raster=raster_list[18]

start_time=time.time()
scores=arcpy.Raster(linkage_raster)*15.0+arcpy.Raster(matrix_forest)*25.0+arcpy.Raster(LCA_raster)+arcpy.Raster(Resilience_raster)+arcpy.Raster(eo_raster)
test_min=arcpy.GetRasterProperties_management(scores,"MINIMUM")
test_max=arcpy.GetRasterProperties_management(scores,"MAXIMUM")
print test_min
print test_max
scores.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Full_scores_test_2")
elapsed_time=time.time()-start_time
print elapsed_time



####Doesn't work  Need to make them all the same size
arcpy.env.snapRaster=snap_raster
linkage_save=arcpy.sa.ExtractByMask(linkage_raster,snap_raster)
linkage_save.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Linkage_binary_snap")

arcpy.env.snapRaster=snap_raster
matrix_save=arcpy.sa.ExtractByMask(matrix_forest,snap_raster)
matrix_save.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Matrix_forest_binary_snap")


arcpy.env.snapRaster=snap_raster
eo_raster_save=arcpy.sa.ExtractByMask(eo_raster,snap_raster)
eo_raster_save.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EO_scores_test_snap")

###Reformatting rasters to eliminate NULLS, and Extracting to exact dimension of the LCA snap raster
#input="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_raster_test_3"
#in_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_raster_test_3"
#
#input="D:\\GIS Projects\\StateParks\\EO_Processing.gdb\\Scored_EO_raster_4"
#in_raster="D:\\GIS Projects\\StateParks\\EO_Processing.gdb\\Scored_EO_raster_4"
#ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
#ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
#print ras_min.getOutput(0)
#print ras_max.getOutput(0)
#
#out_classified_raster=wrk+"EO_scores_Binary"
#
#noNullRemapRange=arcpy.sa.RemapRange([[ras_min.getOutput(0),ras_max.getOutput(0),1],["NoData","NoData",0]])
#
#reclassified_raster=arcpy.sa.Reclassify(in_raster,"Value",noNullRemapRange)
#reclassified_raster.save(out_classified_raster)
#
#arcpy.CalculateStatistics_management(out_classified_raster)
#arcpy.env.extent="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
###ReCondition
#in_conditional_raster=arcpy.Raster(out_classified_raster)
#in_true_constant=0
##where_clause="VALUE == 0"
##in_false_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_raster_test_3"
#in_false_raster="D:\\GIS Projects\\StateParks\\EO_Processing.gdb\\Scored_EO_raster_4"
#con_raster=arcpy.sa.Con(in_conditional_raster <=0,in_true_constant,in_false_raster)
#out_con_raster=wrk+"EO_Raster_Scores_test_4_w_0"
#con_raster.save(out_con_raster)

EO_raster="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_raster_6_16"
outisNull=arcpy.sa.IsNull(EO_raster)
outisNull.save("D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_raster_6_16_NULL")
in_raster=arcpy.Raster("D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_raster_6_16_NULL")
con_raster=arcpy.sa.Con(in_raster == 1, 0, EO_raster)
input=con_raster
ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
print ras_min
print ras_max
out_con_raster=wrk+"Scored_EO_06_17_con"
con_raster.save(out_con_raster)

##Rescore EO raster to 0-1

input="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_con"
ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
print ras_min
print ras_max

max=float(ras_max[0])
min=float(ras_min[0])

range=max-min
minus_data=arcpy.sa.Minus(input,0)
reclass_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_con")*1.0/(range)*1.0
out_put_reclass="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_norm"
snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
reclass_input.save(out_put_reclass)

####Same for new TNC Layer and MFB Layer (MFB also needs to be conditioned so that all areas betwee0 and 0.6 are 0)
##MFB
matrix_linkages="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Forest_Priority_proj_clip_norm"
TNC_Resilience_layer="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\TNC_Resilience_proj_clipped_norm"

mfb_isNull=arcpy.sa.IsNull(matrix_linkages)
mfb_isNull.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Forest_Priority_NULL")
reclass_mfb_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Forest_Priority_NULL")
con_mfb_raster=arcpy.sa.Con(reclass_mfb_input==1,0,matrix_linkages)
con_mfb_raster.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Matrix_Forest_Scores_No_NULL")

input=arcpy.Raster("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Matrix_Forest_Scores_No_NULL")
elim_under_06=arcpy.sa.Con(input < 0.6,0,input)
elim_under_06.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Matrix_Forest_Scores_Complete")

###TNC
tnc_isNULL=arcpy.sa.IsNull(TNC_Resilience_layer)
tnc_isNULL.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\New_TNC_NULL")
reclass_TNC_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\New_TNC_NULL")
con_tnc_raster=arcpy.sa.Con(reclass_TNC_input==1,0,TNC_Resilience_layer)
con_tnc_raster.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\New_TNC_Scored")

###EDM
EDM_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_update_total_Richness_max_1"
EDM_isNULL=arcpy.sa.IsNull(EDM_raster)
EDM_isNULL.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_isNULL")
reclass_EDM_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_isNULL")
con_EDM_raster=arcpy.sa.Con(reclass_EDM_input==1,0,EDM_raster)
con_EDM_raster.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_update_Richness_noNULL")

#EDM_raster="D:\\GIS Projects\\StateParks\\state_parks_baselayers.gdb\\hyp_345_layer"
EDM_raster="D:\\GIS Projects\\StateParks\\state_parks_baselayers.gdb\\Minus_hyp_345"
EDM_isNULL=arcpy.sa.IsNull(EDM_raster)
EDM_isNULL.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_isNULL_07_21")

#input="D:\\GIS Projects\\StateParks\\state_parks_baselayers.gdb\\hyp_345_layer"
input="D:\\GIS Projects\\StateParks\\state_parks_baselayers.gdb\\Minus_hyp_345"

ras_min=arcpy.GetRasterProperties_management(input,"MINIMUM")
ras_max=arcpy.GetRasterProperties_management(input,"MAXIMUM")
print ras_min
print ras_max

max=float(ras_max[0])
min=float(ras_min[0])

range=max-min
minus_data=arcpy.sa.Minus(input,0)
#reclass_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\state_parks_baselayers.gdb\\hyp_345_layer")*1.0/(range)*1.0
reclass_input=arcpy.Raster("D:\\GIS Projects\\StateParks\\state_parks_baselayers.gdb\\Minus_hyp_345")*1.0/(range)*1.0

out_put_reclass="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_hyp344_norm"
snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster=snap_raster
reclass_input.save(out_put_reclass)
###Make version without null for calculations
con_edm_raster=arcpy.sa.Con(EDM_isNULL==1,0,out_put_reclass)
con_edm_raster.save("D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EDM_hyp344_norm_no0_for_add")


##############Round 2- May 2016
scored_EO_raster="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\Scored_EO_raste"
outIsNull=arcpy.sa.IsNull(scored_EO_raster)
eo_null_raster=wrk+"Scored_EO_IsNull"
outIsNull.save(eo_null_raster)

in_conditional_raster=arcpy.Raster(scored_EO_raster)
in_true_constant=0
con_raster=arcpy.sa.Con(in_conditional_raster ==1,in_true_constant,scored_EO_raster)
out_con_raster=wrk+"Scored_EO_con"
con_raster.save(out_con_raster)