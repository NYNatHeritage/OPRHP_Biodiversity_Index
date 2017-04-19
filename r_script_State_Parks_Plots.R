sp_score<-read.csv("D:\\GIS Projects\\StateParks\\TiffsforR\\State_Park_Scores_0510411.csv",sep=",")

sp_score<-read.csv("D:\\GIS Projects\\StateParks\\BIG_State_Parks_Table.csv",sep=",")

sp_score<-sp_score[ which(sp_score$Include=='Y'),]

sp_score<-read.csv("D:\\GIS Projects\\StateParks\\BIG_State_Parks_Table_Yonly.csv",sep=",")
sp_score<-read.csv("D:\\GIS Projects\\StateParks\\BIG_State_Parks_Table_W_Prop_in_Top_n_226.csv",sep=",")
sp_score<-read.csv("D:\\GIS Projects\\StateParks\\State_Parks_Tables\\BIG_State_Parks_Table_345.csv",sep=",")
sp_score<-read.csv("D:\\GIS Projects\\StateParks\\Images_for_Report\\State_Parks_Corrected_Prop_High_Quality.csv",sep=",")

plot(sp_score$Comp_Score_AREA,sp_score$Comp_Score_SUM)
plot(log(sp_score$LCA_Score_MEAN),log(sp_score$Comp_Score_MEAN))


abline(lm(log(sp_score$Comp_Score_MEAN)~log(sp_score$LCA_Score_MEAN)))


plot(sp_score$Comp_Score_AREA,sp_score$Comp_Score_MEAN)
plot(log(sp_score$Comp_Score_AREA),log(sp_score$Comp_Score_MEAN))
abline(lm(log(sp_score$Comp_Score_MEAN)~log(sp_score$Comp_Score_AREA)))
summary(lm(log(sp_score$Comp_Score_MEAN)~log(sp_score$Comp_Score_AREA)))
model<-lm(log(sp_score$Comp_Score_MEAN)~log(sp_score$Comp_Score_AREA))
y<-log(sp_score$Comp_Score_MEAN)
x<-log(sp_score$Comp_Score_AREA)
plot(x,y)
model<-lm(y~x)
abline(model)ggplot(sp_score,a
summary(model)
newx<-seq(min(log(sp_score$Comp_Score_AREA)),max(log(sp_score$Comp_Score_AREA)),length.out=1000)
preds<-predict(model,newdata=data.frame(x=newx),interval=c('confidence'),level=0.90,type="response")
preds_preds<-predict(model,newdata=data.frame(x=newx),interval=c('prediction'),level=0.90,type="response")
lines(newx,preds[ ,3],lty='dashed',col='red')
lines(newx,preds[ ,2],lty='dashed',col='red')

lines(newx,preds_preds[ ,3],lty='dashed',col='blue')
lines(newx,preds_preds[ ,2],lty='dashed',col='blue')


textxy(log(sp_score$AREA),log(sp_score$MEAN),log(sp_score$Name,cex=0.5)
################
recreate this with ggplot
library(ggplot2)
library(ggrepel)

ggplot(sp_score,aes(x=log(sp_score$LCA_Score_MEAN),y=log(sp_score$Comp_Score_MEAN))) +
  geom_point(aes(color=factor(sp_score$Region_Name),size=sp_score$SUM_Shape_Area,shape=factor(sp_score$Category)))+
  
  scale_shape_manual(values=c(8,8,0,12,1,10))+
  scale_size_continuous(range=c(2,20),guide=FALSE)+
  scale_color_brewer(palette="Paired")+
  geom_smooth(method=lm)+
  geom_text_repel(
    aes(
      log(sp_score$LCA_Score_MEAN),log(sp_score$Comp_Score_MEAN),
      label=sp_score$Name,color=factor(sp_score$Region_Name)
      ),
    size=2,segment.color="black")+
  theme_dark()


summary(lm(log(sp_score$Comp_Score_MEAN)~sp_score$LCA_Score_MEAN))
summary(lm(log(sp_score$Comp_Score_MEAN)~sp_score$Comp_Score_AREA))
summary(lm(log(sp_score$Comp_Score_SUM)~sp_score$Comp_Score_AREA))
###
##Parks Plots
library(plyr)

sum_sp<-ddply(sp_score,~sp_score$Region_Name,summarize,mean=mean(Comp_Score_MEAN),lca=mean(LCA_Score_MEAN))

plot(log(sum_sp$lca),log(sum_sp$mean))

plot(sp_score$Region_Name,sp_score$Comp_Score_MEAN)

sp_score$Region<-as.factor(reorder(sp_score$Region,sp_score$Comp_Score_MEAN,median))
boxy<-ggplot(sp_score,aes(x=Region,y=Comp_Score_MEAN,fill=Region,group=Region))
boxy + 
  geom_hline(aes(yintercept=1.54),linetype="dotted")+
  geom_text(aes(x=12,y=1.54,label="NYS Mean: 1.54"),vjust=-1)+
  geom_hline(aes(yintercept=2.73),linetype="longdash")+
  geom_text(aes(x=11.75,y=2.73,label="State Park Mean: 2.73"),vjust=-1)+
  geom_boxplot(outlier.shape=NA,width=0.5,coef=0,alpha=0.4)+
  
  geom_point(shape=21,size=5)+
  scale_x_discrete(expand=c(0.05,0),limits=rev(levels(sp_score$Region)),breaks=c("1","2","3","4","5","7","8","9","10","11","12","13"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City",""))+
#   geom_text_repel(
#     aes(
#       x=(as.factor(reorder(Region,Comp_Score_MEAN,median))),y=Comp_Score_MEAN, 
#       label=sp_score$Name,color=factor(sp_score$Region_Name)
#     ),
#     size=5)+
  labs(x="Parks Region",y="Mean Biodiversity Index")+
  scale_fill_hue(l=45)+
  theme(plot.margin=unit(c(1,1,1,1),"cm"),panel.background = element_blank(),axis.line = element_line(colour = "black"),axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")
  

boxy<-ggplot(sp_score,aes(Region,LCA_Score_MEAN,group=Region))
boxy + 
  geom_boxplot()+
  geom_jitter(width=0.2) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14))

boxy<-ggplot(sp_score,aes(Region,log(EO_Score_SUM),group=Region))
boxy + 
  geom_boxplot()+
  geom_jitter(width=0.2) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14))

boxy<-ggplot(sp_score,aes(Region,log(Richness_Score_MEAN),group=Region))
boxy + 
  geom_boxplot()+
  geom_jitter(width=0.2) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14))

boxy<-ggplot(sp_score,aes(Region,Resilience_Score_MEAN,group=Region))
boxy + 
  geom_boxplot()+
  geom_jitter(width=0.2) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14))


boxy<-ggplot(sp_score,aes(Region,Richness_Score_MEAN,group=Region))
boxy + 
  geom_boxplot()+
  geom_jitter(width=0.2) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14))




boxy<-ggplot(sp_score,aes(Region,MFB_Linkage_Score_MEAN,group=Region))
boxy + 
  geom_boxplot()+
#  geom_jitter(width=0.2) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  geom_text_repel(
    aes(
      Region,MFB_Linkage_Score_MEAN,
      label=sp_score$Name,color=factor(sp_score$Region_Name)
    ),
    size=3,segment.color="black")+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")


boxy<-ggplot(sp_score,aes(x=as.factor(Region),y=Prop_Top_10_percent,group=Region))
boxy + 
  geom_boxplot(outlier.shape=NA)+
  geom_point(shape=1,size=4)+
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  geom_text_repel(data=subset(sp_score,Prop_Top_10_percent>0),
    aes(
      x=as.factor(Region),y=Prop_Top_10_percent,
      label=Name,color=factor(Region_Name)
    ),
    size=3,segment.color="black")+
  labs(x="Parks Region",y="Proportion of Park Area >= 90th Percentile")+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")


boxy<-ggplot(sp_score,aes(x=as.factor(Region),y=Prop_Top_10,group=Region))
boxy + 
  geom_boxplot(outlier.shape=NA)+
  geom_point(shape=1,size=4)+
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  geom_text_repel(data=subset(sp_score,Prop_Top_10>0),
                  aes(
                    x=as.factor(Region),y=Prop_Top_10,
                    label=Name,color=factor(Region_Name)
                  ),
                  size=3,segment.color="black")+
  labs(x="Parks Region",y="Proportion of Park Area >= 90th Percentile")+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")

boxy<-ggplot(sp_score,aes(x=as.factor(Region),y=Prop_Top_5,group=Region))
boxy + 
  geom_boxplot(outlier.shape=NA)+
  geom_point(shape=1,size=4)+
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  geom_text_repel(data=subset(sp_score,Prop_Top_5>0),
                  aes(
                    x=as.factor(Region),y=Prop_Top_5,
                    label=Name,color=factor(Region_Name)
                  ),
                  size=3,segment.color="black")+
  labs(x="Parks Region",y="Proportion of Park Area >= 95th Percentile")+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")


boxy<-ggplot(sp_score,aes(x=as.factor(Region),y=Prop_Top_1,group=Region))
boxy + 
  geom_boxplot(outlier.shape=NA)+
  geom_point(shape=1,size=4)+
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  geom_text_repel(data=subset(sp_score,Prop_Top_1>0),
                  aes(
                    x=as.factor(Region),y=Prop_Top_1,
                    label=Name,color=factor(Region_Name)
                  ),
                  size=3,segment.color="black")+
  labs(x="Parks Region",y="Proportion of Park Area >= 99th Percentile")+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")




boxy<-ggplot(sp_score,aes(x=as.factor(Region),y=Prop_Top_5_percent,group=Region))
boxy + 
  geom_boxplot(outlier.shape=NA)+
  geom_point(shape=1,size=4) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  geom_text_repel(data=subset(sp_score,Prop_Top_5_percent>0),
                  aes(
                    x=as.factor(Region),y=Prop_Top_5_percent,
                    label=Name,color=factor(Region_Name)
                  ),
                  size=3,segment.color="black")+
  labs(x="Parks Region",y="Proportion of Park Area >= 95th Percentile")+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")



boxy<-ggplot(sp_score,aes(x=as.factor(Region),y=Prop_Top_1_percent,group=Region))
boxy + 
  geom_boxplot(outlier.shape=NA)+
  geom_point(shape=1,size=4) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  geom_text_repel(data=subset(sp_score,Prop_Top_1_percent>0),
                  aes(
                    x=as.factor(Region),y=Prop_Top_1_percent,
                    label=Name,color=factor(Region_Name)
                  ),
                  size=3,segment.color="black")+
  labs(x="Parks Region",y="Proportion of Park Area >= 99th Percentile")+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")



boxy<-ggplot(sp_score,aes(x=as.factor(Region),y=Area_Top_1_percent,group=Region))
boxy + 
  geom_boxplot(outlier.shape=NA)+
  geom_point(shape=1,size=4) +
  scale_x_discrete(breaks=c("1","2","3","4","5","7","8","9","10","11","12"),labels=c("Niagra","Allegany","Genesee","Finger Lakes","Central","Taconic","Palisades","Long Island","Thousand Islands","Saratoga/Capital District","New York City"))+
  geom_text_repel(data=subset(sp_score,Area_Top_1_percent>0),
                  aes(
                    x=as.factor(Region),y=Area_Top_1_percent,
                    label=Name,color=factor(Region_Name)
                  ),
                  size=3,segment.color="black")+
  labs(x="Parks Region",y="Park Area >= 99th Percentile")+
  theme(axis.text.x = element_text(angle = 30, vjust = 1, hjust=1,size=14),legend.position="none")




summary(lm(sp_score$Comp_Score_MEAN~sp_score$LCA_Score_MEAN+sp_score$EO_Score_MEAN+sp_score$Richness_Score_MEAN+sp_score$Resilience_Score_MEAN+sp_score$MFB_Linkage_Score_MEAN))


summary(lm(sp_score$Comp_Score_MEAN~sp_score$EO_Score_MEAN+sp_score$Richness_Score_MEAN+sp_score$LCA_Score_MEAN+sp_score$Resilience_Score_MEAN+sp_score$MFB_Linkage_Score_MEAN))


anova(lm(sp_score$Comp_Score_MEAN~sp_score$LCA_Score_MEAN+sp_score$EO_Score_MEAN+sp_score$Richness_Score_MEAN+sp_score$Resilience_Score_MEAN+sp_score$MFB_Linkage_Score_MEAN)))



hist(log(sp_score$AREA))
hist((sp_score$AREA))

model<-(lm(log(sp_score$MEAN)~log(sp_score$AREA)))

sp_score$resid<-model$resid
write.table(sp_score,file="D:\\GIS Projects\\StateParks\\TiffsforR\\State_Park_Scores_0510411_w_resid.csv")

plot(sp_score$SUM,sp_score$MEAN)
plot(log(sp_score$SUM),log(sp_score$MEAN))
abline(lm(log(sp_score$MEAN)~log(sp_score$SUM)))
sp_score$resid<-model$resid


plot(sp_score$MAX,sp_score$MEAN)
plot(log(sp_score$MAX),log(sp_score$MEAN))
abline(lm(log(sp_score$MEAN)~log(sp_score$MAX)))
model_2<-lm(log(sp_score$MEAN)~log(sp_score$MAX))
sp_score$resid_2<-model_2$resid

plot(sp_score$MIN,sp_score$MEAN)
plot(log(sp_score$MIN),log(sp_score$MEAN))
abline(lm(log(sp_score$MEAN)~log(sp_score$MIN)))
model_3<-lm(log(sp_score$MEAN)~log(sp_score$MIN))
sp_score$resid_3<-model_3$resid


plot(sp_score$MIN,sp_score$MAX)
plot(log(sp_score$MIN),log(sp_score$MAX))
abline(lm(log(sp_score$MAX)~log(sp_score$MIN)))
model_3<-lm(log(sp_score$MEAN)~log(sp_score$MIN))
sp_score$resid_3<-model_3$resid

##################
##Which individual component is max

sub_parks<-sp_score[,c("Name","Region","Comp_Score_MEAN","LCA_Score_MEAN","Resilience_Score_MEAN","MFB_Linkage_Score_MEAN","EO_Score_MEAN","Richness_Score_MEAN")]
sub_sub_parks<-sp_score[,c("LCA_Score_MEAN","Resilience_Score_MEAN","MFB_Linkage_Score_MEAN","EO_Score_MEAN","Richness_Score_MEAN")]

test<-princomp(sub_sub_parks)
#library("stats")
biplot(test)
test2<-prcomp(sub_sub_parks)
biplot(test2)
test2$rotation

max_factor<-apply(sub_parks[,2:6],1,which.max)


##sum(sp_score$Area_Top_1_percent)/1272739500
##sum(sp_score$Area_Top_5_percent)/6337584000
##sum(sp_score$Area_Top_10_percent)/12699473400
