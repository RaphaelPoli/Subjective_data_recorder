#Url<-"https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Frestaurants.xml"
#download.file(Url, "resto.xml")
library(xlsx)
library(lubridate)
library ("ggplot2")

#corr correlation statistique (comprendre les maths)
#autocorrelation
#les variables n'étant pas continues, il faudrait les représenter avec autre chose que le temps en x

file<-"lucid_dream_data_2018-2019_v2.xls"

replace_na<- function(x){
        #print (x)
        if ((x=="NA")||is.na(x)){
               # print("Found NA")
                return(NA)
        }
        else{
                #print("Found number")
                return(as.numeric(x))
                
        }
}

replace_na_column<-function(column){
        i=-1
        for (number in column){
                i=i+1
               # print (number)
                column[i]=replace_na(number)
                }
        return (column)
}


DF<-read.xlsx(file, sheetIndex=1, rowIndex=3:200, stringsAsFactors=F)


#converting numeric columns to numeric class (from usually chr)
numeric_columns<-names(DF)[10:53]#47

DF[numeric_columns] <- lapply(DF[numeric_columns], replace_na_column)#replaces NA strings by NA values
DF[numeric_columns] <- lapply(DF[numeric_columns], as.numeric)#converts numbers

#numeric_columns=names(DF)[50:59]#47
#DF[numeric_columns] <- lapply(DF[numeric_columns], replace_na_column)
#DF[numeric_columns] <- lapply(DF[numeric_columns], as.numeric)


# creating a date object column
Date_of_observation <- dmy(DF$Date)
#Date_of_observation2 <- dmy(vector2$Date)
#Bed_Time<-hm(DF$bed.time)

DF$date_object<-Date_of_observation
#vector2$date_object<-Date_of_observation2



# calculating indice lilian
DF$number_of_results<-rowSums(DF[,names(DF)[30:41]],na.rm=T)
DF$number_of_problems<-rowSums(DF[,names(DF)[42:53]],na.rm=T)
DF$indice_lilian<-(DF$number_of_result+1)/(DF$number_of_problems+1)
# ploting indice lilian
indice_lilian_plot<-ggplot(DF,aes(date_object,indice_lilian))
print (indice_lilian_plot+geom_point()+geom_smooth(na.rm=T))


# plotting rest rate
#ce serait bien d'avoir les points sieste et les points matin d'une autre couleur
#ou bien de créer un graph a trois facettes sur la colonne type de ligne
p<-ggplot(DF,aes(date_object,rest.rate.on.10))
print (p+geom_point()+geom_smooth())
#+geom_vline(aes(xintercept=dmy("5 12 2018"))))

# reading data for diner rate
#vector<-subset(DF,light.evening.meal!="NA")
#mean_diner<-mean(as.integer(vector$light.evening.meal))
#vector2<-subset(DF,rest.rate!="NA")
#mean_rest<-mean(as.integer(vector$rest.rate))


#this plot shows when the rest rate linear model crosses the mean
#plot(x=DF$date_object,y=DF$rest.rate, pch=19,ylim=c(0,13))
#abline(h=mean(DF$rest.rate, na.rm=T),col="light green",lwd=1)

#lm is not reluctant on NAs
#abline(lm(formula=rest.rate~date_object,data=DF),col="dark green",lwd=1)
#DF$date_num = as.numeric(DF$date_object,data, as.Date(DF$date_object,data), units="days") 
#lo <- loess(DF$rest.rate.on.10~DF$date_num,DF,na.rm=T)
#smoolines(predict(lo), col='red', lwd=2)
#smoothingSpline = smooth.spline(DF$rest.rate.on.10,DF$date_num, spar=0.35,na.rm=T)
#lines(smoothingSpline)


DFevening=subset(DF,row.type=="evening")
DFevening$light_evening_meal_higher=DFevening$light.evening.meal+1
diner<-ggplot(DFevening,aes(date_object,light_evening_meal_higher))
print (diner+geom_point()+geom_smooth(na.rm=T))

DFevening$Moon.intensity=DFevening$Moon.intensity+1
Moon1<-ggplot(DFevening,aes(date_object,Moon.intensity))
print (Moon1+geom_point()+geom_smooth(na.rm=T))


DFevening$Moon.Harmonies=DFevening$Moon.Harmonies+1
Moon2<-ggplot(DFevening,aes(date_object,Moon.Harmonies))
print (Moon2+geom_point()+geom_smooth(na.rm=T))

#pas sûr que ça ne soit pas mieux avec un nombre d'aspects plutôt qu'un pourcentage
DFevening$Good_moon=(DFevening$Moon.Harmonies+1)/(DFevening$Moon.dysharmony+1)


Moon3<-ggplot(DFevening,aes(date_object,Good_moon))
print (Moon3+geom_point()+geom_smooth(na.rm=T))


DF_tireness<-subset(DF,!is.na(tireness))
tire<-ggplot(DF_tireness,aes(date_object,tireness))
print (tire+geom_point()+geom_smooth(na.rm=T))


DF_f_s<-subset(DF,!is.na(food_satisfaction))
f_s<-ggplot(DF_f_s,aes(date_object,food_satisfaction))
print (f_s+geom_point()+geom_smooth(na.rm=T))


DF_vividness<-subset(DF,!is.na(Vividness_rate))
vivid<-ggplot(DF_vividness,aes(date_object,Vividness_rate))
print (vivid+geom_point()+geom_smooth(na.rm=T))
#print (max(DF_vividness$Vividness_rate))
#print (which(DF_vividness$Vividness_rate==max(DF_vividness$Vividness_rate)))
print ("Date of the most vivid dream in the period (decalage de un jour constate")
print (DF_vividness[which(DF_vividness$Vividness_rate==max(DF_vividness$Vividness_rate))+1,]$date_object)
#Il faudrait creer un tableau avec les dates des reves les plus vivid classe par ordre descendant.
library(plyr)
dates_vivid=data.frame(DF_vividness$Vividness_rate, DF_vividness$date_object,DF_vividness$Consecutive.days.of.good.rest)
DF_v<-arrange(dates_vivid,DF_vividness.Vividness_rate)
print (tail(DF_v))
#DF$Agitation<-sapply(DF$Agitation,replace_na)#ca ca marche
#DF[29]<-sapply(DF[29], replace_na)#ca ca marche pas (seule la premier ligne est prise)
#str(DFDF[,16:41]<-sapply(DF,replace_na)
#DF[,16:41]<-sapply(DF[,16:41], as.integer, na.rm=T)
#DF$the_good=sum(DF[13:8,])
