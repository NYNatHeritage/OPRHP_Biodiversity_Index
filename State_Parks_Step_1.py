##This is part 1 of 3 in Scoring pixels for the State Parks Biodiversity Assessment

##Code needs to assign EOs scores based on their values in 3 fields: Precision, Last_Obs, and Type
#Those field names are "EST_REP_AC" (values "Very High","High",Medium,"Low","Very Low"),"LAST_OBS_D" (this is a string- will need some parsing to get a year),NAME_TYPE_" (either "C" or "A"/"P")

##Need to parse the string data field- some entries have yyyy-mm-dd and some have yyyy, so need a new field that has JUST the 4 digits, as an integer or date
##Also some values in this field have leading or trailing zeros. So first need to remove all those and THEN take the left most 4 digits and conver to integer date

#NOT "GROUP_NAME" = 'Fish' AND NOT "GROUP_NAME"= 'Freshwater Mussels' AND NOT "EO_RANK" = 'X?' AND NOT "EO_RANK"= 'X' AND NOT "ID_CONFRMD"= 'N' AND NOT "ERACCURACY" = 'Very Low' AND NOT "ERACCURACY" = ' '# The selection used to get sub-sample of eos to score for State Parks Project


import arcpy, time
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.env.workspace="D:\\GIS Projects\\StateParks\\Base_Layers.gdb"
wrk="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\"
todlt=[]  ##Set up list of temp files to delete at end of script
#EO_originals="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EO_9_03_2015_layer"
#EO_originals="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\EOs_No_Blank_No_VLAccuracy"
#EO_originals="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\statewide_EOs_October"
#EO_originals="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\EOs_input"

EO_originals="D:\\GIS Projects\\StateParks\\EO_Processing_2016.gdb\\EOs_input_6_16"


snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.extent="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster = "D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"



#precision_terms=["Very High","High","Medium","Low","Very Low"]
precision_terms=["Very High","High","Medium","Low"]

#precision_field="EST_REP_AC"
#precision_field="ERACCURACY"
precision_field="Precision"

#type_field="NAME_TYPE_"
type_field="ELEM_TYPE"
type_values=["A","P","C"]

#date_field="LAST_OBS_D"
date_field="LAST_DATE"

eo_rank_field="EO_RANK"
eo_rank_values=["A","A?","AB","B","B?","AC"]

#s_rank_field="S_RANK"
s_rank_field="S_RANK_CAT"
s_rank_values=["S1","S2","S3"]

#g_rank_field="G_RANK"
g_rank_field="G_RANK_CAT"
g_rank_values=["G1","G2","G3"]

year_class_field="Date_Class"

## There are some dates that are not in 'YYYY_MM_DD' format- they are '_05','_06' not sure how want to handle these (15 records)

##add a stripped Time data field with just the Year as an Integer to allow for numerical operations

arcpy.AddField_management(EO_originals,"Last_Obs_formatted","SHORT")
num_date_field="Last_Obs_formatted"
fields=[date_field,type_field,precision_field,num_date_field]

original_fields=[f.name for f in arcpy.ListFields(EO_originals)]
expanded_fields=[date_field,type_field,precision_field,num_date_field,eo_rank_field,s_rank_field,g_rank_field]
fields_to_preserve=["OBJECTID","EO_ID","SCIEN_NAME","COMMONNAME","Shape_Area","Shape_Length","Shape",date_field,type_field,precision_field,num_date_field,eo_rank_field,s_rank_field,g_rank_field]
fields_to_delete=[f.name for f in arcpy.ListFields(EO_originals) if f.name not in fields_to_preserve]

arcpy.DeleteField_management(EO_originals,fields_to_delete)

new_fields=[f.name for f in arcpy.ListFields(EO_originals)]
new_fields

where_clause='''NOT "LAST_DATE" LIKE 'no_date' AND NOT "LAST_DATE" LIKE '----%' AND NOT "LAST_DATE" ='' '''
with arcpy.da.UpdateCursor(EO_originals,fields,where_clause) as cursor:
#    counter=1
    for row in cursor:
#        if counter <=20:
            print row[0]
            raw_date=row[0]
            strip_date=raw_date.strip()
            fixed_date=strip_date[:4]
            num_date=int(fixed_date)
            #print num_date
#            counter+=1
            row[3]=num_date
            cursor.updateRow(row)

where_clause=''' "LAST_DATE" LIKE 'no_date' OR "LAST_DATE" LIKE '----%' OR "LAST_DATE" ='' '''
with arcpy.da.UpdateCursor(EO_originals,fields,where_clause) as cursor:
#    counter=1
    for row in cursor:
#        if counter<=20:
            print row[0]
#            counter+=1
            num_date=1801
            row[3]=num_date
            cursor.updateRow(row)
            

  


 
##Create Dictionary of Scores           
#scoring_table="D:\\GIS Projects\\StateParks\\Test_Scores.txt"
scoring_table="D:\\GIS Projects\\StateParks\\ScoringTable_5_16.csv"
scoring_table="D:\\GIS Projects\\StateParks\\ScoringTable_5_16.xlsx"
#scoring_table="D:\\GIS Projects\\StateParks\\Test_Scores_w_date.txt"


fields=["Date","Species","Precision","Points"]
scoring_dict={}
with arcpy.da.SearchCursor(scoring_table,fields) as rows:
    for row in rows:
        #print float(row[3])
        key_val_1=row[0]
        key_val_2=row[1]
        key_val_3=row[2]
        score=row[3]
        print score
        val_1=float(score)
        scoring_dict[key_val_1,key_val_2,key_val_3]=val_1
        
value=scoring_dict[3,'C','Very High']

##Key for the dictionary is [Date,Species,Precision]

date_test=1
species_test='C'
precision_test='Very High'

print scoring_dict[date_test,species_test,precision_test] #It works

##Need to re-assign the year field (where it isn't null) to 1-4 based on years
arcpy.AddField_management(EO_originals,"Year_Class","SHORT")
year_class_field="Year_Class"
fields=[date_field,type_field,precision_field,num_date_field,year_class_field]
where_clause=''' "Last_Obs_formatted" IS NOT NULL '''
with arcpy.da.UpdateCursor(EO_originals,fields,where_clause) as cursor:
    for row in cursor:
        year=row[3]
        if year>=2000:
            #print year
            row[4]=1
        elif 1980 <= year < 2000:
            #print year
            row[4]=2
        elif 1950 <= year <1980:
            row[4]=3
        elif 1800 <= year <1950:
            row[4]=4
        cursor.updateRow(row)
        
        
##Add a EO Initial Score
        
arcpy.AddField_management(EO_originals,"EO_Initial_Score","FLOAT")
score_field="EO_Initial_Score"
fields=[year_class_field,type_field,precision_field,score_field]
#where_clause=''' "Year_Class" IS NOT NULL AND "ELEM_TYPE" IS NOT NULL AND "ERACCURACY" IS NOT NULL AND NOT "ERACCURACY"='' AND NOT "ERACCURACY"='Unknown'  '''

where_clause=''' NOT "Precision"='Unknown' AND NOT "Precision"=' ' AND NOT "Date_Class"=0  '''

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})  
        
unique_values(EO_originals,"Precision")
unique_values(EO_originals,year_class_field)

for field in fields:
    print unique_values(EO_originals,field)

with arcpy.da.UpdateCursor(EO_originals,fields,where_clause) as cursor:  
#    counter=1    
    for row in cursor:
#     try:
            class_type=row[1]
            if class_type=='A' or class_type=='P':
                type='S'
            elif class_type=='C':
                type='C'
            year=row[0]
            prec=row[2]
            print (year,type,prec)
            score_value=scoring_dict[year,type,prec]
            print score_value
            row[3]=score_value
#            counter+=1
            cursor.updateRow(row)
            
## Add G Rank Score
unique_values(EO_originals,g_rank_field)            
            
arcpy.AddField_management(EO_originals,"G_Rank_Score","SHORT")
g_score_field="G_Rank_Score"            
g_fields=[year_class_field,g_rank_field,g_score_field]
where_clause=''' "EO_Initial_Score" IS NOT NULL '''
with arcpy.da.UpdateCursor(EO_originals,g_fields,where_clause) as cursor:
#    counter = 1
    for row in cursor:
#        if counter<=20:
            g_rank=row[1]
#            print g_rank
#            counter+=1            
            if "G1" in g_rank:
                print g_rank
                #points=50
                #points=25
                points=40
            elif "G2" in g_rank:
                print g_rank
                #points=35
                #points=20
                points=35
            elif "G3" in g_rank:
                print g_rank
                #points=15                
                points=20
            else:
                points=0
            row[2]=points
            cursor.updateRow(row)
                
## Add S Rank SCore
unique_values(EO_originals,s_rank_field)  
arcpy.AddField_management(EO_originals,"S_Rank_Score","SHORT")
s_score_field="S_Rank_Score"            
s_fields=[year_class_field,s_rank_field,s_score_field]
where_clause=''' "EO_Initial_Score" IS NOT NULL '''
with arcpy.da.UpdateCursor(EO_originals,s_fields,where_clause) as cursor:
#    counter = 1
    for row in cursor:
#        if counter<=20:
            s_rank=row[1]
#            print g_rank
#            counter+=1            
            if "S1" in s_rank:
#                print s_rank
                points=25
            elif  "S2" in s_rank:
#                print s_rank
                points=20
            elif "S3" in s_rank:
#                print s_rank
                points=10
            else:
                points=0
            row[2]=points
            cursor.updateRow(row)

#Get list of EO Rank values
unique_values(EO_originals,eo_rank_field)  
eo_rank_field
eo_fields=[year_class_field,eo_rank_field]
rank_list=[]
with arcpy.da.SearchCursor(EO_originals,eo_fields,where_clause) as cursor:
    for row in cursor:
        print row
        value_rank=row[1]
        print value_rank
        if value_rank not in rank_list:
            print value_rank
            rank_list.append(value_rank)



                         
## Add EO Rank Score
arcpy.AddField_management(EO_originals,"EO_Rank_Score","SHORT")
eo_score_field="EO_Rank_Score"            
eo_fields=[year_class_field,eo_rank_field,eo_score_field]
where_clause=''' "EO_Initial_Score" IS NOT NULL '''
with arcpy.da.UpdateCursor(EO_originals,eo_fields,where_clause) as cursor:
#    counter = 1
    for row in cursor:
#        if counter<=20:
            eo_rank=row[1]
#            print eo_rank
#            counter+=1            
            if eo_rank == "A":
#                print eo_rank
                points=25
            elif eo_rank =="A?":
                points=25
            elif eo_rank == "AB":
#                print eo_rank
                points=20
            elif eo_rank=="B":
#                print eo_rank
                points=15
            elif eo_rank== "B?":
                points=15
            elif eo_rank == "AC":
                points=20
            else:
                points=0
            row[2]=points
            cursor.updateRow(row)
            
## Calculate Combined score
arcpy.AddField_management(EO_originals,"Composite_Score","FLOAT")
total_score_field="Composite_Score"
            
scoring_fields=[year_class_field,score_field,g_score_field,s_score_field,eo_score_field,total_score_field]
where_clause=''' "EO_Initial_Score" IS NOT NULL '''
with arcpy.da.UpdateCursor(EO_originals,scoring_fields,where_clause) as cursor:
#    counter=1
    for row in cursor:
#        if counter<=20:
            i_score=row[1]
            g_score=row[2]
            s_score=row[3]
            eo_score=row[4]
            comp_score=float(i_score)+float(g_score)+float(s_score)+float(eo_score)
            #print i_score,g_score,s_score,eo_score,comp_score
#            counter +=1
            row[5]=comp_score
            cursor.updateRow(row)
           
              