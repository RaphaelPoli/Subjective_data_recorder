#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#import sys
#text=""
#text = unicode(text, sys.getfilesystemencoding())
# add tireness when going to bed
# add satisfaction rate on diner
# charger les valeurs sous forme de notes qui ont été ajoutées.


#--------------------------------------dependencies-----------------------------------------------

# this is to get moon position
import swisseph as swe
import math
# this is interface library
import wx
#import wx.lib.scrolledpanel
#thi is used to search for files in directory
import os.path
#this is to update the xls
import pyexcel 
from pyexcel_ods import get_data
from pyexcel_ods import save_data
from collections import OrderedDict

# this is to get system date 
import datetime

# this is to create dream report in open document format
from odf.opendocument import OpenDocumentText #semble accepter les fichiers aux noms accentués
from odf.opendocument import load
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import H,P
from odf import  table, text
from odf.style import Style, TextProperties, ParagraphProperties
from odf.style import TableColumnProperties
from odf.table import Table, TableColumn, TableRow, TableCell

print wx.PlatformInfo

# to add a row: add the date and the place at the end of the row so that the row has all its cells.


#-----------------------------------------------------------------global variables
default_home_name="La cella"
output_file=u'lucid_dream_data_2018-2019_v2.xls'
french=True
english=False



number_of_rate_columns=5
number_of_improving_practices=5

Time_origin=4
Good_practice_origin=Time_origin+5
Bad_practice_origin=Good_practice_origin+2+number_of_improving_practices+2+2
Results_and_problems_origin=Bad_practice_origin+3+1

print Results_and_problems_origin


Skip_first_entry=False

date=datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")
sheet = get_data(output_file)["Sheet1"]
empty_row=[date,"NA","NA",

			"NA","NA","NA",
			"NA","NA","NA",
			"NA","NA","NA",
			
			"NA","NA","NA",
			"NA","NA","NA",
			"NA","NA","NA",
			
			"NA","NA","NA",
			"NA","NA","NA",
			"NA","NA","NA",
			
			"NA","NA","NA",
			"NA","NA","NA", 
			"NA","NA","NA",
			
			"NA","NA","NA",
			"NA","NA","NA",
			"NA","NA","NA",
			
			"NA","NA","NA","NA","NA",default_home_name,"NA"]
print "longueur du rang attendu",len(empty_row)
row_to_add=[]
i=-1
for value in empty_row:
	i+=1
	row_to_add.append(empty_row[i])


month_name_fr=["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Decembre"]


Dream_report=""
Day_recall=""
month_number=datetime.datetime.strftime(datetime.datetime.now(),"%m")
day_number=str(datetime.datetime.strftime(datetime.datetime.now(),"%d"))
year_number=datetime.datetime.strftime(datetime.datetime.now(),"%Y")
today_n_of_row=0
Today_Dream_filename=date=day_number.zfill(2)+"_"+month_name_fr[int(month_number)-1]+"_"+year_number+"_"+str(today_n_of_row).zfill(2)
Dream_report_tmp=u"dream_report_today"
Day_recall_tmp=u"day_recall_tmp"

print Today_Dream_filename

Software_Name="Dream Recorder"



#-----------------------------------------------------elemental procedures------------------------------------------


def Today_moon_report(start_year,start_month,start_day):#this procedure needs swisseph (it is the only one
	start_hour=0
	total_aspects=0
	pro=True
	interp=False
	zodiac_sign=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricornus","Aquarius","Pisces"]
	planet_name=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto","k","",".","?","K"]

	
	if start_year>1582:
		gregflag=1
	else:
		gregflag=0
	
	def sign(lon):
		signnumber=int(math.floor(lon/30.0))
		return signnumber
	
	def next_sign(Julday,lon,gregflag):
		current_sign=sign(lon)
		moment=0
		result=[]
		while moment < range(30*24*20) and result==[]:
			moment+=1
			ret_gregflag_1 = swe.calc_ut(Julday+moment/480.0, 1, gregflag); 
			explorelon = ret_gregflag_1[0]
			if sign(explorelon)<> current_sign:
				#print "found new sign",
				result.append(sign(explorelon))
				result.append(Julday+moment/480.0)
		return result
	
	
	def any_next_aspect(Julday,lon,demanded_planet,aspect_string,howmany,reverse_direction,gregflag):#possibly "any" for aspect
		moment=0
		sensitivity=0.05
		result_as=[]
		result_pl=[]
		result_dt=[]
		gotit=False
		aspect_table = [["Conjunction",0],
		["Sextile",60],
		["Sextile",-60],
		["Square",90],
		["Square",-90],
		["Trine",120],
		["Trine",-120],
		["Opposition",180]]
		while math.fabs(moment) < range(30*24*20) and len(result_dt)<howmany:
			if reverse_direction:
				moment-=1
			else:
				moment+=1
			if demanded_planet==-1:
				for planet in range(10):
					if planet!=1:
						#extracting moon longitude
						ret_gregflag_1 = swe.calc_ut(Julday+(moment/480.0), 1, gregflag); 
						explorelon = ret_gregflag_1[0]
						#extracting other longitude (variable planet)
						ret_gregflag_other = swe.calc_ut(Julday+(moment/480.0), planet, gregflag); 
						explorelon_other = ret_gregflag_other[0]
						
						for i in range(len(aspect_table)):#parsing aspects to detect in developper defined list
							gotit=False
							dot=explorelon+aspect_table[i][1]
							#if aspect_table[i][1]==-120 and planet_name[planet]=="Pluto" and math.fabs(dot-explorelon_other)<sensitivity: print "trine to Pluto dot=",dot
							#if aspect_table[i][1]==120 and planet_name[planet]=="Pluto" and math.fabs(dot-explorelon_other)<sensitivity: print "trine to Pluto dot=",dot
							
							if dot>360 : dot = dot-360
							if dot<0 : dot = dot+360
							#if i==3 or i==4:
							#print "testing ",aspect_table[i][0]," to ",planet_name[planet], planet, math.fabs(dot-explorelon_other)
							#print math.fabs(dot-explorelon_other),math.fabs(explorelon_other-dot)
							if (math.fabs(dot-explorelon_other)<sensitivity) and (aspect_table[i][0]==aspect_string or aspect_string=="Any"):
								#print "detected aspect "+aspect_table[i][0]+" "+planet_name[planet]
								#if planet==0 and aspect_string=="Any" :print "found new aspect",aspect_table[i][0],planet_name[planet],Julday+moment/480.04
								#if planet==0 and aspect_string=="Any" :print "aft", dot
								already=0
								gotit=False
								if len(result_dt)>5:
									for j in range (5):
										already=(len(result_dt)-1)-j
										#print  "already",already	
										if result_pl[already] == planet and result_as[already]==aspect_table[i][0]:
											gotit=True
											#print "already got this aspect"
											#print "removed",planet_name[planet],aspect_table[i][0]
								else:
									for j in range (len(result_dt)):
										already=j
										if result_pl[already] == planet and result_as[already]==aspect_table[i][0]:
											gotit=True
											#print "already got this aspect"
											#print "removed",planet_name[planet],aspect_table[i][0]
								#print"len",len(result_dt)
								#print  "already",already	
								if not gotit:
									#print "adding aspect "+aspect_table[i][0]+" "+planet_name[planet]
									result_as.append(aspect_table[i][0])
									result_pl.append(planet)
									result_dt.append(Julday+moment/480.0)
								else:
									pass
									#print "gotit est true"
			else:
				#extracting moon longitude
				ret_gregflag_1 = swe.calc_ut(Julday+(moment/480.0), 1, gregflag); 
				explorelon = ret_gregflag_1[0]
				#extracting other longitude (variable planet)
				ret_gregflag_other = swe.calc_ut(Julday+(moment/480.0), demanded_planet, gregflag); 
				explorelon_other = ret_gregflag_other[0]
				
				for i in range(len(aspect_table)):
					gotit=False
					#print "testing ",aspect_table[i][0]," to ",planet_name[demanded_planet], demanded_planet,"lon",explorelon
					dot=explorelon+aspect_table[i][1]
					if dot>360 : dot = dot-360
					if dot<0 : dot = dot+360
					#print "dot ",aspect_table[i][1]," to ",planet_name[demanded_planet], dot
					#print "difference ",math.fabs(dot-explorelon_other)
					if math.fabs(dot-explorelon_other)<sensitivity and (aspect_table[i][0]==aspect_string or aspect_string=="Any"):
						#print "found new aspect",aspect_table[i][0],planet_name[demanded_planet],Julday+(moment/480.0)
						already=0
						gotit=False
						if len(result_dt)>5:
							for j in range (5):
								already=(len(result_dt)-1)-j
								#print  "already",already	
								if result_pl[already] == planet and result_as[already]==aspect_table[i][0]:
									gotit=True
									#print "already got this aspect"
									#print "removed",planet_name[planet],aspect_table[i][0]
							else:
								pass
						else:
							for j in range (len(result_dt)):
								already=j
								if result_pl[already] == planet and result_as[already]==aspect_table[i][0]:
									gotit=True
									#print "already got this aspect"
									#print "removed",planet_name[planet],aspect_table[i][0]
							else:
								pass
						if not gotit:
							#print "adding aspect "+aspect_table[i][0]+" "+planet_name[demanded_planet]
							result_as.append(aspect_table[i][0])
							result_pl.append(demanded_planet)
							result_dt.append(Julday+moment/480.0)
				
		return [result_as,result_pl,result_dt]# as : aspect, pl: planet, dt:time in julian date
		
	def date_hour_convert(date_list):#hours are Universal Time
		#print date_list[3]
		date_string=str(date_list[2])+"/"+str(date_list[1])+"/"+str(date_list[0])
		hourstring= str(datetime.timedelta(seconds = round(date_list[3],2)*3600))
		#print date_string+" "+hourstring+" UT"
		return date_string+" "+hourstring+" UT"
	def is_harmonious(string):
		if (string=="Trine" or string=="Sextile" or string=="Conjunction"):
			return True
		else:
			return False
	def Harmo_neutral_disharmo(string):
		if string=="Conjunction":
			return 2
		if (string=="Trine" or string=="Sextile" ):
			return 1
		else:
			return 3

	jul_day_UT = swe.julday(start_year, start_month, start_day, start_hour, gregflag);# Gr
	ret_gregflag_1 = swe.calc_ut(jul_day_UT, 1, gregflag); 
	moonlon = ret_gregflag_1[0]#longitude of moon
	
	#Checking the moon context

	#print "Current Moon longitude:",round(moonlon,2)
	#print "Current Moon sign:",zodiac_sign[sign(moonlon)]

	print ""
		
	# searching for next new moon
	
	
	#--------------------------------------------	
	#print"Computing today's moon"
	u=any_next_aspect(jul_day_UT,moonlon,-1,"Any",10,False,gregflag)
	#print u
	lastday=''
	day=''
	column=1
	count=0
	End=False
	#writing the moon cycle to the three documents----------------------------------------------------------------------------
	Harmonious_count=0
	Disharmonious_count=0
	Neutral_count=0
	Neutral_percent=0
	Harmonious_percent=0
	Disharmonious_percent=0
	num_jour=0
	new_moon=0
	full_moon=0
	for number in range(len(u[0])-1):
		if not End:
			date2=swe.revjul(u[2][number],gregflag)
			Julday_observed=u[2][number]
			lastday=day
			day=date_hour_convert(date2).split('/')[0]
			if day<>lastday:# when new day
				
				Harmonious_count=0
				Disharmonious_count=0
				Neutral_count=0
				#print int(Julday_observed),"compares",int(jul_day_UT)
				#print Julday_observed,"could compares",jul_day_UT
				
				
			if Harmo_neutral_disharmo(u[0][number])==1:
				Harmonious_count+=1
				total_aspects+=1
				#print "harmonious detected"
						
			if Harmo_neutral_disharmo(u[0][number])==3:
				Disharmonious_count+=1
				total_aspects+=1
				#print "disharmonious detected"
					
			if Harmo_neutral_disharmo(u[0][number])==2:
				Neutral_count+=1
				total_aspects+=1
				#print "neurel detected"
			#print u[0][number]
			#print u[1][number]
			if u[0][number]=="Conjunction" and u[1][number]==0:
				#print "new_moon"
				new_moon=1
			if u[0][number]=="Opposition" and u[1][number]==0:
				#print "full_moon"
				full_moon=1
	
			# testing if next aspect is tomorrow
			date3=swe.revjul(u[2][number+1],gregflag)
			Julday_next_aspect=u[2][number+1]
			next_aspect=date_hour_convert(date3).split('/')[0]
			#print "next aspect",next_aspect
			if next_aspect!=day:
				Number_of_aspect=Neutral_count+Harmonious_count+Disharmonious_count
				if Number_of_aspect>0:
					Neutral_percent=(Neutral_count/float(Number_of_aspect))*100
					Harmonious_percent=(Harmonious_count/float(Number_of_aspect))*100
					Disharmonious_percent=(Disharmonious_count/float(Number_of_aspect))*100
					break
				else:
					pass
				
				
					
	#print date_hour_convert(date2),u[0][number],"to",planet_name[u[1][number]]
	#adding table to document

	#print "Neutral",Neutral_percent
	#print "Harmonious",Harmonious_percent
	#print "Dysharmonious",Disharmonious_percent
	#print "total aspects",total_aspects
	return [Harmonious_percent,Neutral_percent,Disharmonious_percent,total_aspects,new_moon,full_moon]
	
	#------------------------------------------------------------------------------------------------------------------
	
	
def fill_all_moon(date_column=0, skip=4):
	global output_file
	
	sheet = get_data(output_file)#another way to load a sheet this time in an ordered dictionary
	print "longueur du tableau", len(sheet["Sheet1"])
	for date in range(len(sheet["Sheet1"])):
		if date>skip-1:
			
			date_str=sheet["Sheet1"][date][date_column]
			print date_str
			date_obj=datetime.datetime.strptime(date_str, '%d/%m/%Y')
			moon_report=Today_moon_report(date_obj.year,date_obj.month,date_obj.day)
			print ("Harmonious",moon_report[0])
			print ("Neutral",moon_report[1])
			print ("Dysharmonious",moon_report[2])
			print ""
			sheet["Sheet1"][date][date_column+1]=int(moon_report[0])
			sheet["Sheet1"][date][date_column+2]=int(moon_report[1])
			sheet["Sheet1"][date][date_column+3]=int(moon_report[2])
			sheet["Sheet1"][date][date_column+4]=int(moon_report[3])
	pyexcel.save_book_as(bookdict=sheet,dest_file_name=output_file)

#fill_all_moon()
#to work this procedure must load a xls file with 5 columns filled with NA the first column must be dates
def Create_time_delta(date_column=0, skip=1):
	file_name= "time_delta_2019.xls"
	
	sheet = get_data(file_name)#another way to load a sheet this time in an ordered dictionary
	print "longueur du tableau", len(sheet["Sheet1"])
	lun=0
	for date in range(len(sheet["Sheet1"])):
		if date>skip-1:
			
			date_str=str(sheet["Sheet1"][date][date_column])
			print date_str
			date_obj=datetime.datetime.strptime(date_str, '%Y-%m-%d')
			moon_report=Today_moon_report(date_obj.year,date_obj.month,date_obj.day)
			if int(moon_report[4])==1:
				lun+=1
			print "Harmonious",moon_report[0]
			print "Neutral",moon_report[1]
			print "Dysharmonious",moon_report[2]
			print "Lunaison",lun
			print ""
			print "Lunaison",lun
			sheet["Sheet1"][date][date_column+1]=int(moon_report[0])
			sheet["Sheet1"][date][date_column+2]=int(moon_report[1])
			sheet["Sheet1"][date][date_column+3]=int(moon_report[2])
			sheet["Sheet1"][date][date_column+4]=int(moon_report[3])
			sheet["Sheet1"][date][date_column+5]=int(moon_report[4])
			sheet["Sheet1"][date][date_column+6]=int(moon_report[5])
			sheet["Sheet1"][date][date_column+7]=lun
	pyexcel.save_book_as(bookdict=sheet,dest_file_name=file_name)

#Create_time_delta()

def find_reality_check_consecutive():
	pass
	#find todays date
	#find last date where reality check were at 0
	#do a time object substraction (if possible)

def add_column(table):
	for column in table:
		column.append("")
	return table

# this is the procedure that takes too long
# it takes too long because it saves 54 times the whole xls
# insert_cell takes coordinates from 1 not from 0
def new_day_row(row):
	
	global output_file
	add=False
	
	#check if a row was added today and remove it if found
	date=datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")
	sheet = get_data(output_file)["Sheet1"]
	list_date=get_string_coord_column(sheet,0, date)
	print "offsets:",list_date
	if list_date==[]:
		add=True
		print "no today's date occurence found, adding row"
	else:
		print list_date
		print "inserting cells"
		print row
		i=0
		occurences=list_date
		for cell in row:
			i+=1
			#print "inserting at x",occurences[0][0]+i
			Insert_cell(occurences[0][0]+i,occurences[len(occurences)-1][1],str(cell))#inserting at the last occurence of the date
	if add:
	
		book = pyexcel.get_book(file_name=output_file)#loads a sheet in a sheet object that can be modified
		book.Sheet1.row+= row
		print "saving xls"
		book.save_as(output_file)
		
def blind_add_row(row):
	
	global output_file
	print "adding row"
	book = pyexcel.get_book(file_name=output_file)#loads a sheet in a sheet object that can be modified
	book.Sheet1.row+= row
	book.save_as(output_file)
	
#the next procedure writes into a cell but cannot access unexisting cells please add rows to do that
def Insert_cell(x=1,y=1,value="Writing here"):#this procedure uses an xls file and pyexcel the other should be harmonized
	
	global output_file
	
	sheet = get_data(output_file)#another way to load a sheet this time in an ordered dictionary
	sheet["Sheet1"][y-1][x-1]=value
	pyexcel.save_book_as(bookdict=sheet,dest_file_name=output_file)#saves a sheet
	return sheet

def Read_cell(x=1,y=1):#this procedure uses an xls file and pyexcel the other should be harmonized
	
	global output_file
	
	sheet = get_data(output_file)#another way to load a sheet this time in an ordered dictionary
	value=sheet["Sheet1"][y-1][x-1]
	return value

# the next procedure finds a string in the sheet
def get_string_coord(table, string):#if empty rows are repeated more than two times there are errors in row count probably due to ODSReader conditional count.
	
	#the search is now case sensitive
	
	#print "searching",string
	#print date_day
	i=0
	j=0
	memorize_coord=[]
	#print "number of rows",len(table)
	for row in range(len(table)):
		#print "row",row, table[row][0]
		i+=1
		j=0
		match=False
		cell__low=""
		for cell in table[row]:
			j+=1#column number
			#print "comparing",cell,string
			if type(cell)<>int:
				cell__low=str(cell)
				#print "-"+cell__low+"-"
				#print "converting to lowercase"
			else:
				if cell<>None:
					cell__low=str(cell)
					cell__low=cell__low.lower()
			#print "type",type(cell__low)
			#print cell__low.find(string)
			if string == cell__low:
				#print "found",cell__low
				memorize_coord.append([j,i])#column,row
				
	return memorize_coord

def get_string_coord_column(table,column, string):#if empty rows are repeated more than two times there are errors in row count probably due to ODSReader conditional count.
	
	#the search is now case sensitive
	
	#print "searching",string
	#print date_day
	i=0
	j=0
	memorize_coord=[]
	#print "number of rows",len(table)
	for row in range(len(table)):
		#print "row",row, table[row][0]
		i+=1
		j=0
		match=False
		cell__low=""
		j=column
		cell=table[row][column]
		if type(cell)<>int:
			cell__low=str(cell)
				#print "-"+cell__low+"-"
				#print "converting to lowercase"
		else:
			if cell<>None:
				cell__low=str(cell)
				cell__low=cell__low.lower()
			#print "type",type(cell__low)
			#print cell__low.find(string)
		if string == cell__low:
			#print "found",cell__low
			memorize_coord.append([j,i])#column,row
				
	return memorize_coord
	
def save_all(row,report,day_recall):
	
		new_day_row(row_to_add)
		

def define_type(bed_hour):#for now only works with "h" as a separator
	bed_h=int (bed_hour.split("h")[0])
	if bed_h>=10 and bed_h<19:
		typ="nap"
	if bed_h<=8 :
		typ="morning"
	if bed_h>=19:
		typ="evening"
	return typ
	
	
# imported classes

from string import Template

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)
    
#-------------------------------------------------------------------interface start-------------------------------------------------

class Good_Practice(wx.Panel):
	def __init__(self, parent, title):
		#----------------------------------------------- container creation
		global Skip_first_entry
		global number_of_improving_practices
		
		fgs_container = wx.FlexGridSizer(4, 2, 9, 25)
		fgs_buttons = wx.FlexGridSizer(1, 2, 9, 25)
		fgs_reality_check=wx.FlexGridSizer(1, 8, 9, 12)
		fgs_reality_check_and_title=wx.FlexGridSizer(2, 1, 9, 12)
		fgs_zazen1=wx.FlexGridSizer(1, 5, 9, 12)
		fgs_zazen2=wx.FlexGridSizer(1, 2, 9, 12)
		fgs_zazen_and_title=wx.FlexGridSizer(2, 1, 9, 12)
		fgs_note1=wx.FlexGridSizer(5, 5, 9, 12)
		fgs_note2=wx.FlexGridSizer(5, 5, 9, 12)
		fgs_notes=wx.FlexGridSizer(2, 2, 9, 50)
		fgs_time=wx.FlexGridSizer(2, 2, 9, 50)
		fgs_hours=wx.FlexGridSizer(1, 2, 9, 50)
		fgs_more_practice=wx.FlexGridSizer(3, 2, 9, 50)
		
		fgs_morning_choice=wx.FlexGridSizer(2,2,9,12)
		fgs_evening_choice=wx.FlexGridSizer(2,2,9,12)
		fgs_morning=wx.FlexGridSizer(2, 1, 9, 50)
		fgs_evening=wx.FlexGridSizer(2, 1, 9, 50)
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		self.title_diner=wx.StaticText(self, label="I had a light diner (on 10)")
		self.title_rest=wx.StaticText(self, label="I am well rested (on 10)")
		self.title_evening=wx.StaticText(self, label="I went to bed at")
		self.title_morning=wx.StaticText(self, label="I finally got up at")
		self.reality_check_t=wx.StaticText(self, label="Reality checks yesterday")
		self.zazen_t=wx.StaticText(self, label="Zazen yesterday")
		
		self.rb1=[]
		self.rb2=[]
		self.rb3=[]
		self.rb4=[]
		self.rb5=[]
		self.rb6=[]
		self.chk=[]
		
		
		
		
		
		#rest rate
		rest_note=range(14)[1:14]#cette ligne génère douze integer de 1 à 13
		for n in range(13):
			if (n==0):
				self.rb1.append(wx.RadioButton(self, label=str(n+1),style=wx.RB_GROUP))
			else:
				self.rb1.append(wx.RadioButton(self, label=str(n+1)))
			self.rb1[n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb1[n].SetValue(False)
		# loading rest rate
		print "rest rate",row_to_add[Results_and_problems_origin]
		if row_to_add[Results_and_problems_origin]==u"NA":
			
			self.rb1[len(self.rb1)-1].SetValue(True)
		else:
			for i in range(13):
				if int(row_to_add[Results_and_problems_origin])==rest_note[i]:
					self.rb1[i].SetValue(True)
					
					
				
				
				
		#diner rate

		diner_note=range(14)[0:14]#cette ligne génère douze integer de 1 à 13
		for n in range(14):
			if (n==0):
				self.rb2.append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.rb2.append(wx.RadioButton(self, label=str(n)))
			self.rb2[n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb2[n].SetValue(False)
		self.rb2.append(wx.RadioButton(self, label="NA"))
		self.rb2[14].SetValue(False)
		
		# loading diner rate
		rate=row_to_add[Good_practice_origin+number_of_improving_practices+3]
		print "diner",rate
		if rate==u"NA":
			self.rb2[14].SetValue(True)
		else:
			for i in range(13):
				if int(row_to_add[Good_practice_origin+number_of_improving_practices+3])==diner_note[i]:
					self.rb2[i].SetValue(True)
				if Skip_first_entry:#setting to NA if more than one row has been recorded this day
					self.rb2[14].SetValue(True)
			
		
		
		# bed time
		bedtime_index=1
		self.rb3.append(wx.RadioButton(self, label="22h00",style=wx.RB_GROUP))
		self.rb3.append(wx.RadioButton(self, label="22h30"))
		self.rb3.append(wx.RadioButton(self, label="23h00"))
		self.rb3.append(wx.RadioButton(self, label="23h30"))
		standard_hour=False
		if row_to_add[Time_origin+bedtime_index]==u"22h00":
			self.rb3[0].SetValue(True)
			standard_hour=True
		if row_to_add[Time_origin+bedtime_index]==u"22h30":
			self.rb3[1].SetValue(True)
			standard_hour=True
		if row_to_add[Time_origin+bedtime_index]==u"23h00":
			self.rb3[2].SetValue(True)
			standard_hour=True
		if row_to_add[Time_origin+bedtime_index]==u"23h30":
			self.rb3[3].SetValue(True)
			standard_hour=True
			
		self.text_evening=wx.TextCtrl(self)
		if not standard_hour and row_to_add[Time_origin+bedtime_index]!="NA" :
			self.text_evening.SetValue(row_to_add[Time_origin+bedtime_index])
		
		
		# get up time
		getuptime_index=2
		
		# interface elements
		self.rb4.append(wx.RadioButton(self, label="06h06",style=wx.RB_GROUP))
		self.rb4.append(wx.RadioButton(self, label="07h07"))
		self.rb4.append(wx.RadioButton(self, label="07h30"))
		self.rb4.append(wx.RadioButton(self, label="08h00"))
		
		
		#loading data for get up time
		#print "testing",row_to_add[Time_origin+getuptime_index]
		
		standard_hour=False
		if row_to_add[Time_origin+getuptime_index]==u"08h00":
			self.rb4[3].SetValue(True)
			standard_hour=True
		if row_to_add[Time_origin+getuptime_index]==u"07h07":
			self.rb4[1].SetValue(True)
			standard_hour=True
		if row_to_add[Time_origin+getuptime_index]==u"07h30":
			self.rb4[2].SetValue(True)
			standard_hour=True
		if row_to_add[Time_origin+getuptime_index]==u"06h06":
			self.rb4[0].SetValue(True)
			standard_hour=True
		
		#if time is not standard load it, if it is not availanle load current time
		self.text_morning=wx.TextCtrl(self)
		if (not standard_hour) :
			if row_to_add[Time_origin+getuptime_index]=="NA":
				current_hour=datetime.datetime.strftime(datetime.datetime.now(),"%Hh%M")
				self.text_morning.SetValue(current_hour)
			else:
				self.text_morning.SetValue(row_to_add[Time_origin+getuptime_index])
				
			
		#meditation
	
		self.rb6.append(wx.RadioButton(self, label="0min",style=wx.RB_GROUP))
		self.rb6.append(wx.RadioButton(self, label="24min"))
		self.rb6.append(wx.RadioButton(self, label="30min"))
		self.rb6.append(wx.RadioButton(self, label="45min"))
	
		standard_time=False
		#print "zazen loaded", row_to_add[Good_practice_origin+number_of_improving_practices+2]#+2 for reality check and consecutive days
		#print type(row_to_add[Good_practice_origin+number_of_improving_practices+2])
		if row_to_add[Good_practice_origin+number_of_improving_practices+2]==0:
			self.rb6[0].SetValue(True)
			standard_time=True
		if row_to_add[Good_practice_origin+number_of_improving_practices+2]==24:
			self.rb6[1].SetValue(True)
			standard_time=True
		if row_to_add[Good_practice_origin+number_of_improving_practices+2]==30:
			self.rb6[2].SetValue(True)
			standard_time=True
		if row_to_add[Good_practice_origin+number_of_improving_practices+2]==45:
			self.rb6[3].SetValue(True)
			standard_time=True
		
		self.text_zazen=wx.TextCtrl(self)
		if not standard_time :
			self.text_zazen.SetValue(str(row_to_add[Good_practice_origin+number_of_improving_practices+2]))
			#print "zazen",row_to_add[Good_practice_origin+number_of_improving_practices+2]
			if row_to_add[Good_practice_origin+number_of_improving_practices+2]!=u"NA":
				#print "zazen not NA"
				self.text_zazen.SetValue(str(row_to_add[Good_practice_origin+number_of_improving_practices+2]))
		
		# improving practices
		self.chk.append(wx.CheckBox(self, -1, 'Spirit Offering'))
		self.chk.append(wx.CheckBox(self, -1, 'Practice acceptance dialog'))
		self.chk.append(wx.CheckBox(self, -1, 'Spoken prayers'))	
		self.chk.append(wx.CheckBox(self, -1, 'Ginkgo intake'))	
		self.chk.append(wx.CheckBox(self, -1, 'Sincerity and no gain spirit in practice'))	
		
		for i in range(len(self.chk)):
			if row_to_add[Good_practice_origin+i+2]==1:
				self.chk[i].SetValue(True)

		#reality checks
		reality_check=range(8)[0:8]
		for n in range(8):
			if (n==0):
				self.rb5.append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.rb5.append(wx.RadioButton(self, label=str(n)))
			self.rb5[n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb5[n].SetValue(False)
		for i in range(8):
			if row_to_add[Good_practice_origin]==reality_check[i]:
				self.rb5[i].SetValue(True)
			
	
		#print (len(self.rb3))
		#self.rb1[9].SetValue(True)
		self.button3 = wx.Button(self, label="Record on last Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		self.button4 = wx.Button(self, label="Add new empty entry")
		self.Bind(wx.EVT_BUTTON, self.add_new_row, self.button4)
		
		
		
		#now filling containers
		
		fgs_note1.AddMany(self.rb1)#contient les douze radio buttons de la première note
		fgs_note2.AddMany(self.rb2)
		
		fgs_morning_choice.AddMany(self.rb3)#5 elements en colonne
		fgs_morning.AddMany([fgs_morning_choice,self.text_evening])#2elements en colonne
		
		fgs_evening_choice.AddMany(self.rb4)
		fgs_evening.AddMany([fgs_evening_choice,self.text_morning])#morning and evening seem inverted but they are not (?)
		
		fgs_reality_check.AddMany(self.rb5)
		fgs_reality_check_and_title.AddMany([self.reality_check_t,fgs_reality_check])
		fgs_zazen1.AddMany(self.rb6)
		fgs_zazen2.AddMany([fgs_zazen1,self.text_zazen])
		fgs_zazen_and_title.AddMany([self.zazen_t,fgs_zazen2])
		#fgs_hours.AddMany([fgs_evening,fgs_morning])
		
		fgs_more_practice.AddMany(self.chk)
		
		fgs_notes.AddMany([self.title_rest,self.title_diner,fgs_note1,fgs_note2])#contains two main rates
		fgs_time.AddMany([self.title_evening,self.title_morning,fgs_morning,fgs_evening])#contains time questions
		fgs_buttons.AddMany([self.button3,self.button4])
		fgs_container.AddMany([fgs_notes,fgs_time,fgs_reality_check_and_title,fgs_zazen_and_title,fgs_more_practice,fgs_buttons])
		#bSizer.Add(fgs_container, wx.ALL)
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	def SetVal(self,event):# could be used to transfer standard values in text controls
		pass
		
		
	def add_new_row(self,event):# adds empty row
		global row_to_add
		global frame
		global empty_row
		global output_file
		global today_n_of_row
		global Today_Dream_filename
		date=datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")
		i=-1
		row_to_add=[]
		for value in empty_row:
			i+=1
			row_to_add.append(empty_row[i])
		
		print "empty row",empty_row
		blind_add_row(row_to_add)
		today_n_of_row=today_n_of_row+1
		Today_Dream_filename=day_number.zfill(2)+"_"+month_name_fr[int(month_number)-1]+"_"+year_number+"_"+str(today_n_of_row).zfill(2)

		frame.Close()
		frame = Main_Form(None,Software_Name)
		app.SetTopWindow(frame)
		frame.Show()
		# this should be a separate procedure
		print "loading added row"
		print "date",date
		sheet = get_data(output_file)["Sheet1"]
		occurences=get_string_coord_column(sheet,0, date)
		
		print occurences
		
		i=0
		for cell in range(len(row_to_add)):
			#print cell
			i+=1
			#print occurences
			#print "occ",occurences[0][0]
			print "i",i
			
			cell_content=Read_cell(occurences[len(occurences)-1][0]+i,occurences[len(occurences)-1][1])
			row_to_add[i-1]=u""+str(cell_content)#inserting at the last occurence of the date
			print cell_content
		print "after add row in good practice row", row_to_add
		i=-1
		#print frame.text.GetValue()
	
		
		
	def Click(self,event):#records the data for good practices
		global app
		global row_to_add
		global Time_origin
		global Results_and_problems_origin
		global Good_practice_origin
		
		hours_evening=["22h00","22h30","23h00","23h30"]
		hours_morning=["06h06","07h07","7h30","08h00"]
		zazen_minutes=[0,24,30,45]
		#rest_note=map(str,range(13))[1:13]#cette ligne génère une chaine de douze chiffres de 1 à 12
		rest_note=range(14)[1:14]#cette ligne génère quatorze integers de 0 à 13
		reality_check=range(8)[0:8]
		diner_rate=range(14)
		print reality_check
		
			
		#Calculating sleep duration
		def time_difference(string_start,string_end):# this time difference is made for yesterday to today (should be split into two procedures)
			#add here or in the core of the click procedure something to complete string if minutes lack for example
			typ=define_type(string_start)
			yesterday_date=datetime.date.today()-datetime.timedelta(1)
			#print "yesterday",yesterday_date
			yesterday_string=yesterday_date.strftime("%d%m%Y")
			today_string=datetime.date.today().strftime("%d%m%Y")
			if typ=="evening":
				start=datetime.datetime.strptime(yesterday_string+string_start, '%d%m%Y%Hh%M')
			else:
				start=datetime.datetime.strptime(today_string+string_start, '%d%m%Y%Hh%M')
			end=datetime.datetime.strptime(today_string+string_end, '%d%m%Y%Hh%M')
			#print start, end
			time_object=end-start
			result=strfdelta(time_object, "%H h %M")#only workd with spaces (this is a flaw of the imported procedure)
			result=result.replace(" ", "")
			#print "replaced result",result
			return result
		
		#Transfering interface values into the global list of variable that represents current row (row_to_add)
		
		#moon analysis
		moon_analysis=Today_moon_report(int(year_number),int(month_number),int(day_number))
		i=-1
		for value in moon_analysis:
			i+=1
			row_to_add[i+1]=int(value)
		
		#wake up time
		if self.text_morning.GetValue()!="":
			print "wake up time not blank inserting typed text"
			row_to_add[Time_origin+2]=self.text_morning.GetValue()# be careful this line assigns a unicode
		else:
			i=-1
			for values in self.rb4:
				i+=1
				if values.GetValue():
					rb4_string=hours_morning[i]
			row_to_add[Time_origin+2]=rb4_string
			
			
		#bed time
		if self.text_evening.GetValue()!="":
			print "bed time not blank inserting typed text"
			row_to_add[Time_origin+1]=self.text_evening.GetValue()# be careful this line assigns a unicode
		else:
			i=-1
			for values in self.rb3:
				i+=1
				if values.GetValue():
					rb3_string=hours_evening[i]
			row_to_add[Time_origin+1]=row_to_add[Time_origin+1]=rb3_string
			
		#sleep length
		row_to_add[Time_origin+3]=time_difference(row_to_add[Time_origin+1],row_to_add[Time_origin+2])
		#row type
		row_to_add[Time_origin+4]=define_type(row_to_add[Time_origin+1])
		
		i=-1# rest rate
		for values in self.rb1:
			i+=1
			rb1_string="NA"
			#print i,values.GetValue()
			if values.GetValue():
				#print "assinging"
				rb1_string=rest_note[i]
				row_to_add[Results_and_problems_origin]=rb1_string
				break
				
				
		i=-1#diner rate
		if self.rb2[14].GetValue():#"If NA is checked don't look at the rate"
			print "NA checked"
			row_to_add[Good_practice_origin+number_of_improving_practices+3]="NA"
		else:
			for values in self.rb2:
				i+=1
				rb2_string="NA"
				if values.GetValue():
					rb2_string=diner_rate[i]
					print "recording diner",rb2_string,"at position",Good_practice_origin+number_of_improving_practices+3
					row_to_add[Good_practice_origin+number_of_improving_practices+3]=rb2_string
					break
					
		i=-1#reality check
		for values in self.rb5:
			i+=1
			rb5_string="NA"
			if values.GetValue():
				rb5_string=reality_check[i]
				row_to_add[Good_practice_origin]=rb5_string
				break
				
		#improving practice
		i=-1
		for values in self.chk:
			i+=1
			#print 5+i,values.GetValue()
			if values.GetValue():#if checkbox is true
				#print "assinging"
				row_to_add[Good_practice_origin+2+i]=1# 2 is there because there are rest rate and consecutive days of good rest
				one_checked=True
			else:
				row_to_add[Good_practice_origin+2+i]=0
				
		#zazen
		if self.text_zazen.GetValue()!="":
			if self.text_zazen.GetValue()=="NA":
				row_to_add[Good_practice_origin+number_of_improving_practices+2]="NA"
			else:
				row_to_add[Good_practice_origin+number_of_improving_practices+2]=int(self.text_zazen.GetValue())
		else:
			i=-1
			for values in self.rb6:
				i+=1
				rb6_string="NA"
				if values.GetValue():
					rb6_string=zazen_minutes[i]
					print "recording zazen",rb6_string,"at position",Good_practice_origin+number_of_improving_practices+2
					row_to_add[Good_practice_origin+number_of_improving_practices+2]=rb6_string
					break
		print "after good practice recording",row_to_add
		new_day_row(row_to_add)
		
			
		
class Dream_Report(wx.Panel):
	def __init__(self, parent, title):
		global Dream_report_tmp
		global Day_recall_tmp
		global Results_and_problems_origin
		global row_to_add
		global number_of_rate_columns


		# entry is defined new if none of the dream characteristics have been s
	    # because usually it is easier to set them after the dream report is written
		def entry_is_new():
			result=True
			for i in range(23):
				value=row_to_add[Results_and_problems_origin+i+number_of_rate_columns]
				if value!=u"NA":
					result=False
			return result

			
		if not entry_is_new():
			if os.path.isfile(Dream_report_tmp+".odt"):
				report= load(Dream_report_tmp+".odt")
				last_dream_report=report.text
				last_recall= load(Day_recall_tmp+".odt")
				last_day_recall=last_recall.text
	
		#----------------------------------------------- container creation

		
		fgs_container = wx.FlexGridSizer(1, 2, 9, 25)
		fgs_d_report = wx.FlexGridSizer(2, 1, 9, 25)
		fgs_d_recall = wx.FlexGridSizer(2, 1, 9, 25)
		
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		font=wx.Font(17,wx.FONTFAMILY_DEFAULT,wx.NORMAL,wx.FONTWEIGHT_NORMAL,False, encoding=wx.FONTENCODING_UTF8)
	
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		self.rb1=[]
		self.rb2=[]
		
		#self.rb1[9].SetValue(True)
		self.day_recall=wx.TextCtrl(self,size=(480,350), style = wx.TE_MULTILINE)
		if not entry_is_new():
			self.day_recall.SetValue(str(last_day_recall))
		self.report=wx.TextCtrl(self,size=(480,350), style = wx.TE_MULTILINE, value=u"")
		if not entry_is_new():
			self.report.SetValue(str(last_dream_report))
		self.button3 = wx.Button(self, label="Record both")
		self.Bind(wx.EVT_BUTTON, self.Click_day_recall, self.button3)#should rename this procedure

		self.report.SetFont(font)
		self.day_recall.SetFont(font)
		fgs_d_recall.AddMany([self.day_recall,self.button3])
		fgs_d_report.AddMany([self.report])
		fgs_container.AddMany([fgs_d_report,fgs_d_recall])
		#bSizer.Add(fgs_container, wx.ALL)
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	# ------------------------------------------------- panel methods ---------------------------------------------------
	
	def SetVal(self,event):
		pass
		
	def Click_day_recall(self,event):# recording in an open document the day recall text box
		global Today_Dream_filename
		global Dream_report_tmp
		global Dream_report
		global Day_recall
		global Good_practice_origin
		global Time_origin
		global number_of_improving_practices
		global french
		global english
		
		Day_recall=self.day_recall.GetValue()
		Dream_report=self.report.GetValue()
			
		textdoc = OpenDocumentText()
		tmpdoc_recall= OpenDocumentText()
		tmpdoc_dream= OpenDocumentText()
		
		s = textdoc.styles#here we define a style for Red font
		bluestyle = Style(name="blue", family="paragraph")
		bluestyle.addElement(TextProperties(attributes={'color':"#0000bf"}))
		s.addElement(bluestyle)
		
		# saving day_recall input to a tmp file in case of crash and to reload it at next start up if in current day
		p = P(text= Day_recall)
		tmpdoc_recall.text.addElement(p)
	
		p = P(text= Dream_report)
		tmpdoc_dream.text.addElement(p)
	
		
		# date inside document
		#here there might be an existing procedure, 
		#but probably not straightforward to get in french as my system language is english
		month_name_fr=["Janvier",u"Février","Mars","Avril","Mai","Juin","Juillet",u"Aoùt","Septembre","Octobre","Novembre",u"Décembre"]
		month_number=datetime.datetime.strftime(datetime.datetime.now(),"%m")
		day_number=str(datetime.datetime.strftime(datetime.datetime.now(),"%d"))
		year_number=datetime.datetime.strftime(datetime.datetime.now(),"%Y")
	
		date_string=day_number.zfill(2)+" "+month_name_fr[int(month_number)-1]+" "+year_number
			
		h = H(text= date_string, stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		h = H(text= "", stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		
		# giving hour values in french in the document
		
		
		if french :
			h = H(text=u"Je me suis couché à "+row_to_add[Time_origin+1]+u" et je me suis levé à "+row_to_add[Time_origin+2]+".", stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
			
			
			h = H(text=u"J'ai dormi "+row_to_add[Time_origin+3]+".", stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
			
			h = H(text=u"Je suis reposé à "+str(row_to_add[Results_and_problems_origin])+"/10", stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
			
			if not row_to_add[Good_practice_origin+number_of_improving_practices+3] == u"NA":
				h = H(text=u"Le repas du soir était léger à "+str(row_to_add[Good_practice_origin+number_of_improving_practices+3])+u"/10 "+".", stylename=bluestyle, outlinelevel=1,)
				textdoc.text.addElement(h)
	
			h = H(text=u"La Lune était intense à "+str(row_to_add[4]), stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
		
		if english:
			h = H(text=u"I went to bed at "+row_to_add[Time_origin+1]+u" and got up at "+row_to_add[Time_origin+2]+".", stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
			
			
			h = H(text=u"I slept for "+row_to_add[Time_origin+3], stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
			
			h = H(text=u"I am well rested at"+str(row_to_add[Results_and_problems_origin])+"/10", stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
			
			if not row_to_add[Good_practice_origin+6] == u"NA":
				h = H(text=u"My evening meal was light at "+str(row_to_add[Good_practice_origin+number_of_improving_practices+3])+u"/10 "+".", stylename=bluestyle, outlinelevel=1,)
				textdoc.text.addElement(h)
			
			h = H(text=u"The Moon was intense at "+str(row_to_add[4]), stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
				
		h = H(text= "", stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		h = H(text= Day_recall, stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		p = P(text= "")
		textdoc.text.addElement(p)
		
		p = P(text= Dream_report)
		textdoc.text.addElement(p)
		
		print"Saving", "./"+Today_Dream_filename
		textdoc.save(u"./"+Today_Dream_filename, True)#unicode is important!!
		print"Saving", Day_recall_tmp
		tmpdoc_recall.save(u"./"+Day_recall_tmp, True)
		print"Saving", Dream_report_tmp
		tmpdoc_dream.save(u"./"+Dream_report_tmp, True)
	
	
	
class Good_Practice2(wx.Panel):# tab with Results and problems
	def __init__(self, parent, title):
		#----------------------------------------------- container creation

		fgs_container = wx.FlexGridSizer(4, 2, 9, 25)
		fgs_rates_1 = wx.FlexGridSizer(3, 5,  9, 25)
		fgs_rates_2 = wx.FlexGridSizer(3, 5,  9, 25)
		fgs_problems=wx.FlexGridSizer(7, 2, 9, 25)
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		
		#those copy paste could be a iterative loop
		
		self.rb=[]
				
		#Satisfaction rate
		self.title_1=wx.StaticText(self, label="Satisfaction found in yesterday's diner(rate on 10)")
		self.rb.append([])
		rate_list=range(14)[0:14]#cette ligne génère douze integer de 1 à 13
		for n in range(14):
			if (n==0):
				self.rb[0].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.rb[0].append(wx.RadioButton(self, label=str(n)))
			self.rb[0][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb[0][n].SetValue(False)
		self.rb[0].append(wx.RadioButton(self, label="NA"))
		self.rb[0][14].SetValue(False)
		
		# setting initial state to the rate
		
		for i in range(14):
			if row_to_add[Good_practice_origin+10]==rate_list[i]:
				self.rb[0][i].SetValue(True)
			if Skip_first_entry:#setting to NA if more than one row
				self.rb[0][14].SetValue(True)
		
		
		#Tireness rate
		self.rb.append([])
		
		self.title_2=wx.StaticText(self, label="Tireness When going to bed (rate on 10)")
		rate_list=range(14)[0:14]#cette ligne génère douze integer de 1 à 13
		for n in range(14):
			if (n==0):
				self.rb[1].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.rb[1].append(wx.RadioButton(self, label=str(n)))
			self.rb[1][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb[1][n].SetValue(False)
		self.rb[1].append(wx.RadioButton(self, label="NA"))
		self.rb[1][14].SetValue(False)
		
		# setting initial state to the rate
		for i in range(14):
			if row_to_add[Good_practice_origin+9]==rate_list[i]:
				self.rb[1][i].SetValue(True)
			if Skip_first_entry:#setting to NA if more than one row
				self.rb[1][14].SetValue(True)
		
		
		
		
		self.chk=[]
		#self.rb1[9].SetValue(True)
		#self.report=wx.TextCtrl(self,size=(500,200), style = wx.TE_MULTILINE)
		
		
		
		self.button3 = wx.Button(self, label="Record Form")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		fgs_rates_1.AddMany(self.rb[0])
		fgs_rates_2.AddMany(self.rb[1])
		#the fgs container is filled line by line from left to right
		fgs_container.AddMany([self.title_1,self.title_2,fgs_rates_1,fgs_rates_2,self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
	
		# ------------------------------------------------- Dream quality rates panel methods ---------------------------------------------------

	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Good_practice_origin
		global number_of_improving_practices
		
		rate_list=range(14)[0:14]
			
		i=-1
		if self.rb[0][14].GetValue():#"If NA is checked don't look at the rate"
			print "NA checked"
			row_to_add[Good_practice_origin+10]="NA"
		else:
			for values in self.rb[0]:
				i+=1
				if values.GetValue():
					row_to_add[Good_practice_origin+10]=rate_list[i]
					break
		
		i=-1
		if self.rb[1][14].GetValue():#"If NA is checked don't look at the rate"
			print "NA checked"
			row_to_add[Good_practice_origin+9]="NA"
		else:
			for values in self.rb[1]:
				i+=1
				if values.GetValue():
					row_to_add[Good_practice_origin+9]=rate_list[i]
					break
					
		#print row_to_add
		new_day_row(row_to_add)
		
		
	
class Dream_Quality_rates(wx.Panel):# tab with Results and problems
	def __init__(self, parent, title):
		#----------------------------------------------- container creation

		fgs_container = wx.FlexGridSizer(4, 2, 9, 25)
		fgs_rates_1 = wx.FlexGridSizer(3, 5,  9, 25)
		fgs_rates_2 = wx.FlexGridSizer(3, 5,  9, 25)
		fgs_rates_3 = wx.FlexGridSizer(3, 5,  9, 25)
		fgs_problems=wx.FlexGridSizer(7, 2, 9, 25)
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		
		#those copy paste could be a iterative loop
				
		#Vividness rate
		self.title_1=wx.StaticText(self, label="The dream was vivid (rate on 10)")
		self.rb_vivid=[]
		vividness_rate=range(14)[0:14]#cette ligne génère douze integer de 1 à 13
		for n in range(14):
			if (n==0):
				self.rb_vivid.append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.rb_vivid.append(wx.RadioButton(self, label=str(n)))
			self.rb_vivid[n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb_vivid[n].SetValue(False)
		self.rb_vivid.append(wx.RadioButton(self, label="NA"))
		self.rb_vivid[14].SetValue(False)
		
		# setting initial state to the rate
		for i in range(14):
			if row_to_add[Results_and_problems_origin+2]==vividness_rate[i]:
				self.rb_vivid[i].SetValue(True)
			if Skip_first_entry:#setting to NA if more than one row
				self.rb_vivid[14].SetValue(True)
		
		
		#blissfulness rate
		self.title_2=wx.StaticText(self, label="The dream was blissfull (rate on 10)")
		self.rb_blissfull=[]
		blissfulness_rate=range(14)[0:14]#cette ligne génère douze integer de 1 à 13
		for n in range(14):
			if (n==0):
				self.rb_blissfull.append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.rb_blissfull.append(wx.RadioButton(self, label=str(n)))
			self.rb_blissfull[n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb_blissfull[n].SetValue(False)
		self.rb_blissfull.append(wx.RadioButton(self, label="NA"))
		self.rb_blissfull[14].SetValue(False)
		
		# setting initial state to the rate
		for i in range(14):
			if row_to_add[Results_and_problems_origin+3]==blissfulness_rate[i]:
				self.rb_blissfull[i].SetValue(True)
			if Skip_first_entry:#setting to NA if more than one row
				self.rb_blissfull[14].SetValue(True)
		
		
		#Rememberance rate
		self.title_3=wx.StaticText(self, label="I remember well (rate on 10)")
		self.rb_rememberance=[]
		rememberance_rate=range(14)[0:14]#cette ligne génère douze integer de 1 à 13
		for n in range(14):
			if (n==0):
				self.rb_rememberance.append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.rb_rememberance.append(wx.RadioButton(self, label=str(n)))
			self.rb_rememberance[n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb_rememberance[n].SetValue(False)
		self.rb_rememberance.append(wx.RadioButton(self, label="NA"))
		self.rb_rememberance[14].SetValue(False)
		
		# setting initial state to the rate
		for i in range(14):
			if row_to_add[Results_and_problems_origin+4]==rememberance_rate[i]:
				self.rb_rememberance[i].SetValue(True)
			if Skip_first_entry:#setting to NA if more than one row
				self.rb_rememberance[14].SetValue(True)
		
		
		
		
		self.chk=[]
		#self.rb1[9].SetValue(True)
		#self.report=wx.TextCtrl(self,size=(500,200), style = wx.TE_MULTILINE)
		
		
		
		self.button3 = wx.Button(self, label="Record Form")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		fgs_rates_1.AddMany(self.rb_vivid)
		fgs_rates_2.AddMany(self.rb_blissfull)
		fgs_rates_3.AddMany(self.rb_rememberance)
		#the fgs container is filled line by line from left to right
		fgs_container.AddMany([self.title_1,self.title_3,fgs_rates_1,fgs_rates_3,self.title_2,self.button3,fgs_rates_2])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
	
		# ------------------------------------------------- Dream quality rates panel methods ---------------------------------------------------

	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Good_practice_origin
		global number_of_improving_practices
		
		vividness_rate=range(14)[0:14]
		rememberance_rate=range(14)[0:14]		
		blissfullness_rate=range(14)[0:14]
			
		i=-1
		if self.rb_vivid[14].GetValue():#"If NA is checked don't look at the rate"
			print "NA checked"
			row_to_add[Results_and_problems_origin+2]="NA"
		else:
			for values in self.rb_vivid:
				i+=1
				if values.GetValue():
					row_to_add[Results_and_problems_origin+2]=vividness_rate[i]
					break
		
		i=-1
		if self.rb_blissfull[14].GetValue():#"If NA is checked don't look at the rate"
			print "NA checked"
			row_to_add[Results_and_problems_origin+3]="NA"
		else:
			for values in self.rb_blissfull:
				i+=1
				if values.GetValue():
					row_to_add[Results_and_problems_origin+3]=blissfullness_rate[i]
					break
					
		
		i=-1
		if self.rb_rememberance[14].GetValue():#"If NA is checked don't look at the rate"
			print "NA checked"
			row_to_add[Results_and_problems_origin+4]="NA"
		else:
			for values in self.rb_rememberance:
				i+=1
				if values.GetValue():
					row_to_add[Results_and_problems_origin+4]=rememberance_rate[i]
					break
		#print row_to_add
		new_day_row(row_to_add)
		
		
		
class Dream_Quality(wx.Panel):# tab with Results and problems
	def __init__(self, parent, title):
		global number_of_rate_columns
		#----------------------------------------------- container creation

		fgs_container = wx.FlexGridSizer(2, 2, 9, 25)
		fgs_dream_quality = wx.FlexGridSizer(7, 2, 9, 25)
		fgs_problems=wx.FlexGridSizer(7, 2, 9, 25)
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		self.chk=[]
		#self.rb1[9].SetValue(True)
		#self.report=wx.TextCtrl(self,size=(500,200), style = wx.TE_MULTILINE)
		self.chk.append(wx.CheckBox(self, -1, 'Lots of dream signs'))
		self.chk.append(wx.CheckBox(self, -1, 'Full Lucidity report'))
		self.chk.append(wx.CheckBox(self, -1, 'Partial Lucidity report'))
		self.chk.append(wx.CheckBox(self, -1, 'Vivid Dream'))
		self.chk.append(wx.CheckBox(self, -1, 'Blissfull Dream'))
		self.chk.append(wx.CheckBox(self, -1, 'Mystic Dream'))
		self.chk.append(wx.CheckBox(self, -1, 'Learning Dream'))
		self.chk.append(wx.CheckBox(self, -1, 'Teaching Dream'))
		self.chk.append(wx.CheckBox(self, -1, 'Advice Dream'))
		self.chk.append(wx.CheckBox(self, -1, 'Warn Dream'))
		self.chk.append(wx.CheckBox(self, -1, 'Outlet Dream'))
		self.chk.append(wx.CheckBox(self, -1, 'Repairing Dream'))
		
		self.chk.append(wx.CheckBox(self, -1, 'Bad remembering'))
		self.chk.append(wx.CheckBox(self, -1, 'Nightmare'))
		self.chk.append(wx.CheckBox(self, -1, 'Night Terror'))
		self.chk.append(wx.CheckBox(self, -1, 'Disturbance while reporting'))
		self.chk.append(wx.CheckBox(self, -1, 'Lack of sleep'))
		self.chk.append(wx.CheckBox(self, -1, 'Animal disturbance'))
		self.chk.append(wx.CheckBox(self, -1, 'Human disturbance'))
		self.chk.append(wx.CheckBox(self, -1, 'Spirit disturbance'))
		self.chk.append(wx.CheckBox(self, -1, 'Agitation'))
		self.chk.append(wx.CheckBox(self, -1, 'Breathing difficulty'))
		self.chk.append(wx.CheckBox(self, -1, 'Total blackout'))
		self.chk.append(wx.CheckBox(self, -1, 'Night Worry'))
		
		for i in range(23):
			if row_to_add[Results_and_problems_origin+i+number_of_rate_columns]==1:#if you change this offset also change line 604 (dream report loading) and data recording in this tab's methods
				self.chk[i].SetValue(True)

		
		
		
		self.button3 = wx.Button(self, label="Record Form")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		fgs_dream_quality.AddMany(self.chk[0:12])
		fgs_problems.AddMany(self.chk[12:24])
		fgs_container.AddMany([fgs_dream_quality,fgs_problems,self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	def SetVal(self,event):
		state1 = self.rb1.GetValue()
		state2 = self.rb2.GetValue()
		if state1:
			print "Melody"
		if state2: 
			print "Tone"
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Results_and_problems_origin
		global number_of_rate_columns
		i=-1
		chk_string=[]
		for values in self.chk:
			i+=1
			#print i,values.GetValue()
			if values.GetValue():
				#print "assinging"
				chk_string.append(1)
				one_checked=True
			else:
				chk_string.append(0)	
		print len(self.chk)
		print "length of dream quality file", len(row_to_add)
		print "length of dream quality string",len(chk_string)
		for i in range(len(self.chk)):
			print i
			row_to_add[Results_and_problems_origin+number_of_rate_columns+i]=chk_string[i]
		#print row_to_add
		new_day_row(row_to_add)
		
		
		
		
class Bad_Practice(wx.Panel):
	def __init__(self, parent, title):
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(2, 2, 9, 25)
		fgs_dream_quality = wx.FlexGridSizer(9, 1, 9, 25)
		fgs_problems=wx.FlexGridSizer(9, 1, 9, 25)
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		self.chk=[]
		#self.rb1[9].SetValue(True)
		#self.report=wx.TextCtrl(self,size=(500,200), style = wx.TE_MULTILINE)
		self.chk.append(wx.CheckBox(self, -1, 'Alcohol/Smoke/Drugs taken'))
		self.chk.append(wx.CheckBox(self, -1, 'More than 2 coffees yesterday'))
		self.chk.append(wx.CheckBox(self, -1, 'Screen used during last hour before sleep'))
		self.chk.append(wx.CheckBox(self, -1, 'Emphasis in offering'))
	
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[Bad_practice_origin+i]==1:
				self.chk[i].SetValue(True)

		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		fgs_dream_quality.AddMany(self.chk[0:8])
		fgs_problems.AddMany(self.chk[8:17])
		fgs_container.AddMany([fgs_dream_quality,fgs_problems,self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		state1 = self.rb1.GetValue()
		state2 = self.rb2.GetValue()
		if state1:
			print "Melody"
		if state2: 
			print "Tone"
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Results_and_problems_origin
		i=-1
		chk_string=[]
		for values in self.chk:
			i+=1
			#print i,values.GetValue()
			if values.GetValue():
				#print "assinging"
				chk_string.append(1)
				one_checked=True
			else:
				chk_string.append(0)	
		print len(self.chk)
		print len(row_to_add)
		print len(chk_string)
		for i in range(len(self.chk)):
			print i
			row_to_add[Bad_practice_origin+i]=chk_string[i]
		#print row_to_add
		new_day_row(row_to_add)
		
		
class Main_Form(wx.Frame):
	
	def __init__(self, parent, title, pos=(10,10)):
		#self.Move(wx.Point(100,100))
		global Skip_first_entry
		global today_n_of_row
		global Today_Dream_filename
		# -------------------------------main backend------------------------------------------------
		date=datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")
		sheet = get_data(output_file)["Sheet1"]
		occurences=get_string_coord_column(sheet,0, date)
		print occurences
		today_n_of_row=len(occurences)
		Today_Dream_filename=day_number.zfill(2)+"_"+month_name_fr[int(month_number)-1]+"_"+year_number+"_"+str(today_n_of_row).zfill(2)

		if occurences==[]:
			
			row_to_add[0]=date
			new_day_row(row_to_add)
			"You did not run the program today creating new row"
		else:
			list_entry=get_string_coord_column(sheet,0, date)
			if len(list_entry)>1:
				print "Found more than one entry for today, skipping first day entry values"
				Skip_first_entry=True
			print "reading today last entry" #in case todays date exists in the sheet
										#the number of variable must match between the init list and the loaded sheet
			print "number of variables:",len(row_to_add)
			i=0
			for cell in range(len(row_to_add)):
				#print cell
				i+=1
				#print occurences
				#print "occ",occurences[0][0]
				print "i",i
				
				cell_content=Read_cell(occurences[len(occurences)-1][0]+i,occurences[len(occurences)-1][1])
				row_to_add[i-1]=u""+str(cell_content)#inserting at the last occurence of the date
				print cell_content
			print "after reading row", row_to_add

		#---------------------------------------main frontend--------------------------------------------
		
		super(Main_Form, self).__init__(parent,title=title, size=(999, 444))
		
		
		panel = wx.Panel(self)
		nb = wx.Notebook(panel)

		# Create the tab windows
		tab1 = Good_Practice (nb, "Good Practice" )
		tab4 = Good_Practice2(nb, "Good Practice 2" )
		tab5 = Bad_Practice(nb,"Bad Practice")
		tab3 = Dream_Report(nb,"Dream Report")
		tab2 = Dream_Quality(nb,"Dream Quality 1")
		tab6 = Dream_Quality_rates(nb,"Dream Quality 2")
		#tab5 = Directories(nb,"Directories")
		# Add the windows to tabs and name them.
		nb.AddPage(tab3, "Dream Report")
		nb.AddPage(tab1, "Good Practice 1")
		nb.AddPage(tab4, "Good Practice 2")
		nb.AddPage(tab2, "Dream Quality 1")
		nb.AddPage(tab6, "Dream Quality 2")
		nb.AddPage(tab5, "Bad Practice")
		#nb.AddPage(tab5, "Directories")
			
		#final wrapping
		sizer = wx.BoxSizer()
		sizer.Add(nb, 1, wx.EXPAND)
		panel.SetSizer(sizer)


if __name__ == "__main__":
	app = wx.App()
	app.font=wx.Font(24,wx.FONTFAMILY_DEFAULT,wx.NORMAL,wx.FONTWEIGHT_NORMAL,False, encoding=wx.FONTENCODING_UTF8)
	

	frame = Main_Form(None,Software_Name)
	app.SetTopWindow(frame)
	frame.Show()
	#print frame.text.GetValue()
	app.MainLoop()
