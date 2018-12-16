#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#import sys
#text=""
#text = unicode(text, sys.getfilesystemencoding())


#--------------------------------------dependencies-----------------------------------------------
import wx
#import wx.lib.scrolledpanel

import os.path

import pyexcel 
from pyexcel_ods import get_data
from pyexcel_ods import save_data
from collections import OrderedDict
import datetime

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

# added vegetable to snack
# added belly to aches

# procedure to add a variable:
# add a column in the xls sheet
# add a "NA" to initialisation empty_row variable
# add a container in the tab
# add the button labels
# add the buttons (mostly copy paste)
# fill the containers
# ajust the offsets initial variables

#-----------------------------------------------------------------global variables

default_home_name="La cella"
output_file=u'food_observation.xls'
french=True
english=False




breakfast_offset=1
lunch_offset=15
diner_offset=31
snack_offset=47
beverage_offset=62
physical_activity_offset=72
body_state_offset=78
body_signs_offset=95
Skip_first_entry=False

date=datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")
sheet = get_data(output_file)["Sheet1"]

empty_row=["NA"]* 102
empty_row[0]=date

print empty_row
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

Software_Name="Food observator"



#-----------------------------------------------------elemental procedures------------------------------------------
def find_reality_check_consecutive():
	pass
	#find todays date
	#find last date where reality check were at 0
	#do a time object substraction (if possible)

def add_column(table):
	for column in table:
		column.append("")
	return table

def new_day_row(row):
	
	global output_file
	add=False
	
	#check if a row was added today and remove it if found
	date=datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")
	sheet = get_data(output_file)["Sheet1"]
	if get_string_coord(sheet, date)==[]:
		add=True
		print "adding row"
	else:
		print get_string_coord(sheet, date)
		print "inserting cells"
		print row
		i=-1
		occurences=get_string_coord(sheet, date)
		for cell in row:
			i+=1
			Insert_cell(occurences[0][0]+i,occurences[len(occurences)-1][1],cell)#inserting at the last occurence of the date
	if add:
	
		book = pyexcel.get_book(file_name=output_file)#loads a sheet in a sheet object that can be modified
		book.Sheet1.row+= row
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
		for i in range(12):
			if row_to_add[Results_and_problems_origin]==rest_note[i]:
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
		for i in range(14):
			if row_to_add[Good_practice_origin+number_of_improving_practices+3]==diner_note[i]:
				self.rb2[i].SetValue(True)
			if Skip_first_entry:#setting to NA if more than one row
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
		
		i=-1
		occurences=get_string_coord(sheet, date)
		print occurences
		for cell in range(len(row_to_add)):
			i+=1
			
			row_to_add[i]=Read_cell(occurences[0][0]+i,occurences[len(occurences)-1][1])#inserting at the last occurence of the date
		#print row_to_add
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
		new_day_row(row_to_add)
		
		
class Diner(wx.Panel):
	def __init__(self, parent, title):
		global breakfast_offset
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(10, 2, 9, 25)
		fgs_dietary_supplement = wx.FlexGridSizer(9, 1, 9, 25)
		fgs_other_component=wx.FlexGridSizer(4, 2, 9, 25)
		fgs_n_of_=[]#list of number of containers
		for g in range(5):
			fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		i=-1
		self.title=[]
		#Number of Vegetable
		i+=1#0
		self.title.append(wx.StaticText(self, label="Number of Vegetable:"))
		self.breakfast=[]
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Number of meat
		i+=1#1
		self.title.append(wx.StaticText(self, label="Number of meat share (100g a share):"))
		self.breakfast.append([])
		for n in range(3):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][3].SetValue(False)
		
		#Number of share of fish
		i+=1#2
		self.title.append(wx.StaticText(self, label="Number of shares of fish (100g a share):"))
		self.breakfast.append([])
		for n in range(3):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][3].SetValue(False)
		
		#Number of share of cheese
		i+=1#3
		self.title.append(wx.StaticText(self, label="Number of shares of dairy:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Number of eggs
		i+=1#4
		self.title.append(wx.StaticText(self, label="Number of eggs:"))
		self.breakfast.append([])
		for n in range(3):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][3].SetValue(False)
		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		self.chk=[]
		self.chk.append([])
		self.chk[0].append(wx.CheckBox(self, -1, 'Meal substitute taken'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Iron and magnesium taken'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Vitamins taken'))
		
		
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[breakfast_offset+i]==1:
				self.chk[i].SetValue(True)

		
		self.chk.append([])
		self.chk[1].append(wx.CheckBox(self, -1, 'Bread taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Butter taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Fat chocolate taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Nibbling before diner'))
		
		self.chk[1].append(wx.CheckBox(self, -1, 'Cake taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Jam taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Black chocolate taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'yogurt taken'))
		
	
		# ------------------------------ filling containers for lunch
		
		for j in range(5):
			fgs_n_of_[j].AddMany(self.breakfast[j])
		
		fgs_dietary_supplement.AddMany(self.chk[0][0:8])
		fgs_other_component.AddMany(self.chk[1][0:8])
		fgs_container.AddMany([	self.title[0],fgs_n_of_[0],
								self.title[1],fgs_n_of_[1],
								self.title[2],fgs_n_of_[2],
								self.title[3],fgs_n_of_[3],
								self.title[4],fgs_n_of_[4],
								fgs_dietary_supplement, fgs_other_component,
								self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Results_and_problems_origin
		global diner_offset
		
		n_of_num=len(self.breakfast)
		print "n_of_num",n_of_num
		saved_factor=[]
		saved_factor.append(["0","1","2","3","NA"])#vegetable
		saved_factor.append(["0","1","2","NA"])#meat
		saved_factor.append(["0","1","2","NA"])#fish
		saved_factor.append(["0","1","2","3","NA"])#cheese	
		saved_factor.append(["0","1","2","NA"])#eggs	
		
		
		#saving all radio buttons
		for i in range (len(self.breakfast)):#iterating thru radio groups
			j=-1
			for values in self.breakfast[i]:#iterating thru radio buttons
				j+=1
				if values.GetValue():
					rb_string=saved_factor[i][j]
			row_to_add[diner_offset+i]=rb_string
		num_of_n=len(saved_factor)
		
		# saving all checkbox groups
		chk_string=[]
		for i in range(len(self.chk)):#iterating thru checkbox groups
			j=-1
			for values in self.chk[i]:#iterating thru checkboxes
				j+=1
				#print i,values.GetValue()
				if values.GetValue():
					#print "assinging"
					chk_string.append(1)
					one_checked=True
				else:
					chk_string.append(0)	
			print "n of chk",len(self.chk[i])
			print "n of chk string",len(chk_string)
		for k in range(len(chk_string)):
			print k
			row_to_add[diner_offset+num_of_n+k]=chk_string[k]
				
		#print row_to_add
		new_day_row(row_to_add)
			
		
class Lunch(wx.Panel):
	def __init__(self, parent, title):
		global breakfast_offset
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(10, 2, 9, 25)
		fgs_dietary_supplement = wx.FlexGridSizer(9, 1, 9, 25)
		fgs_other_component=wx.FlexGridSizer(4, 2, 9, 25)
		fgs_n_of_=[]#list of number of containers
		for g in range(5):
			fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		i=-1
		self.title=[]
		#Number of Vegetable
		i+=1#0
		self.title.append(wx.StaticText(self, label="Number of Vegetable:"))
		self.breakfast=[]
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Number of meat
		i+=1#1
		self.title.append(wx.StaticText(self, label="Number of meat share (100g a share):"))
		self.breakfast.append([])
		for n in range(3):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][3].SetValue(False)
		
		#Number of share of fish
		i+=1#2
		self.title.append(wx.StaticText(self, label="Number of shares of fish (100g a share):"))
		self.breakfast.append([])
		for n in range(3):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][3].SetValue(False)
		
		#Number of share of cheese
		i+=1#3
		self.title.append(wx.StaticText(self, label="Number of shares of dairy:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Number of eggs
		i+=1#4
		self.title.append(wx.StaticText(self, label="Number of eggs:"))
		self.breakfast.append([])
		for n in range(3):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][3].SetValue(False)
		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		self.chk=[]
		self.chk.append([])
		self.chk[0].append(wx.CheckBox(self, -1, 'Meal substitute taken'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Iron and magnesium taken'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Vitamins taken'))
		
		
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[breakfast_offset+i]==1:
				self.chk[i].SetValue(True)

		
		self.chk.append([])
		self.chk[1].append(wx.CheckBox(self, -1, 'Bread taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Butter taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Fat chocolate taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Nibbling before lunch'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Cake taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Jam taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Black chocolate taken'))
	
		
	
		# ------------------------------ filling containers for lunch
		
		for j in range(5):
			fgs_n_of_[j].AddMany(self.breakfast[j])
		
		fgs_dietary_supplement.AddMany(self.chk[0][0:8])
		fgs_other_component.AddMany(self.chk[1][0:8])
		fgs_container.AddMany([	self.title[0],fgs_n_of_[0],
								self.title[1],fgs_n_of_[1],
								self.title[2],fgs_n_of_[2],
								self.title[3],fgs_n_of_[3],
								self.title[4],fgs_n_of_[4],
								fgs_dietary_supplement, fgs_other_component,
								self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Results_and_problems_origin
		
		n_of_num=len(self.breakfast)
		print "n_of_num",n_of_num
		saved_factor=[]
		saved_factor.append(["0","1","2","3","NA"])#vegetable
		saved_factor.append(["0","1","2","NA"])#meat
		saved_factor.append(["0","1","2","NA"])#fish
		saved_factor.append(["0","1","2","3","NA"])#cheese	
		saved_factor.append(["0","1","2","NA"])#eggs	
		
		
		#saving all radio buttons
		for i in range (len(self.breakfast)):#iterating thru radio groups
			j=-1
			for values in self.breakfast[i]:#iterating thru radio buttons
				j+=1
				if values.GetValue():
					rb_string=saved_factor[i][j]
			row_to_add[lunch_offset+i]=rb_string
		num_of_n=len(saved_factor)
		
		# saving all checkbox groups
		chk_string=[]
		for i in range(len(self.chk)):#iterating thru checkbox groups
			j=-1
			for values in self.chk[i]:#iterating thru checkboxes
				j+=1
				#print i,values.GetValue()
				if values.GetValue():
					#print "assinging"
					chk_string.append(1)
					one_checked=True
				else:
					chk_string.append(0)	
			print "n of chk",len(self.chk[i])
			print "n of chk string",len(chk_string)
		for k in range(len(chk_string)):
			print k
			row_to_add[lunch_offset+num_of_n+k]=chk_string[k]
														
		#print row_to_add
		new_day_row(row_to_add)
		

class Snack(wx.Panel):
	def __init__(self, parent, title):
		global breakfast_offset
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(9, 2, 9, 25)
		fgs_dietary_supplement = wx.FlexGridSizer(9, 1, 9, 25)
		fgs_other_component=wx.FlexGridSizer(5, 2, 9, 25)
		fgs_n_of_=[]
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		i=-1
		self.title=[]
		self.breakfast=[]
		
		
		#Number of vegetable
		i+=1#0
		self.title.append(wx.StaticText(self, label="Number of vegetable:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		#Number of fruit
		i+=1#1
		self.title.append(wx.StaticText(self, label="Number of fruits:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Number of share of cheese
		i+=1#2
		self.title.append(wx.StaticText(self, label="Number of shares of cheese (10g a share):"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		self.chk=[]
		self.chk.append([])
		self.chk[0].append(wx.CheckBox(self, -1, 'Meal substitute taken'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Iron and magnesium taken'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Vitamins taken'))
		
		
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[breakfast_offset+i]==1:
				self.chk[i].SetValue(True)

		
		self.chk.append([])
		self.chk[1].append(wx.CheckBox(self, -1, 'Bread taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Butter taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Fat chocolate taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Cake taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'FruitSauce taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Nibbling during afternoon'))
		
		self.chk[1].append(wx.CheckBox(self, -1, 'Jam taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Black chocolate taken'))
		self.chk[1].append(wx.CheckBox(self, -1, 'yogurt taken'))
		
	
		# ------------------------------ filling containers
		
		fgs_n_of_[0].AddMany(self.breakfast[0])
		fgs_n_of_[1].AddMany(self.breakfast[1])
		fgs_n_of_[2].AddMany(self.breakfast[2])
		
		fgs_dietary_supplement.AddMany(self.chk[0][0:8])
		fgs_other_component.AddMany(self.chk[1])
		fgs_container.AddMany([	self.title[0],fgs_n_of_[0],
								self.title[1],fgs_n_of_[1],
								self.title[2],fgs_n_of_[2],
								
								fgs_dietary_supplement, fgs_other_component,
								self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Results_and_problems_origin
		global snack_offset
		saved_factor=[]
		saved_factor.append(["0","1","2","3","NA"])#vegetable
		saved_factor.append(["0","1","2","3","NA"])#fruits
		saved_factor.append(["0","1","2","3","NA"])#cheese
		
		
		#saving all radio buttons
		for i in range (len(self.breakfast)):#iterating thru radio groups
			j=-1
			for values in self.breakfast[i]:#iterating thru radio buttons
				j+=1
				if values.GetValue():
					rb_string=saved_factor[i][j]
			row_to_add[snack_offset+i]=rb_string
		
		num_of_n=len(saved_factor)
		# saving all checkbox groups
		chk_string=[]
		for i in range(len(self.chk)):#iterating thru checkbox groups
			j=-1
			for values in self.chk[i]:#iterating thru checkboxes
				j+=1
				#print i,values.GetValue()
				if values.GetValue():
					#print "assinging"
					chk_string.append(1)
					one_checked=True
				else:
					chk_string.append(0)	
			print "n of chk",len(self.chk[i])
			print "n of chk string",len(chk_string)
		for k in range(len(chk_string)):
			print k
			row_to_add[snack_offset+num_of_n+k]=chk_string[k]
									
		
		#print row_to_add
		new_day_row(row_to_add)
		
			
class Breakfast(wx.Panel):
	def __init__(self, parent, title):
		global breakfast_offset
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(6, 2, 9, 25)
		fgs_dietary_supplement = wx.FlexGridSizer(9, 1, 9, 25)
		fgs_other_component=wx.FlexGridSizer(4, 2, 9, 25)
		fgs_n_of_=[]
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		i=-1
		self.title=[]
		#Number of fruit
		i+=1#0
		self.title.append(wx.StaticText(self, label="Number of fruits:"))
		self.breakfast=[]
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Number of eggs
		i+=1#1
		self.title.append(wx.StaticText(self, label="Number of eggs:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		#Number of share of meat
		i+=1#2
		self.title.append(wx.StaticText(self, label="Number of shares of meat (100g a share):"))
		self.breakfast.append([])
		for n in range(3):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][3].SetValue(False)
		
		#Number of share of cheese
		i+=1#3
		self.title.append(wx.StaticText(self, label="Number of shares of cheese (10g a share):"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=str(n),style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=str(n)))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		self.chk=[]
		self.chk.append(wx.CheckBox(self, -1, 'Meal substitute taken'))
		self.chk.append(wx.CheckBox(self, -1, 'Iron and magnesium taken'))
		self.chk.append(wx.CheckBox(self, -1, 'Vitamins taken'))
		
		
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[breakfast_offset+i]==1:
				self.chk[i].SetValue(True)

		
		self.chk2=[]
		self.chk2.append(wx.CheckBox(self, -1, 'Bread taken'))
		self.chk2.append(wx.CheckBox(self, -1, 'Butter taken'))
		self.chk2.append(wx.CheckBox(self, -1, 'Fat chocolate taken'))
		self.chk2.append(wx.CheckBox(self, -1, 'Cake taken'))
		
		self.chk2.append(wx.CheckBox(self, -1, 'Jam taken'))
		self.chk2.append(wx.CheckBox(self, -1, 'Black chocolate taken'))
		self.chk2.append(wx.CheckBox(self, -1, 'yogurt taken'))
		
	
		# ------------------------------ filling containers
		
		fgs_n_of_[0].AddMany(self.breakfast[0])
		fgs_n_of_[1].AddMany(self.breakfast[1])
		fgs_n_of_[2].AddMany(self.breakfast[2])
		fgs_n_of_[3].AddMany(self.breakfast[3])
		fgs_dietary_supplement.AddMany(self.chk[0:8])
		fgs_other_component.AddMany(self.chk2[0:8])
		fgs_container.AddMany([	self.title[0],fgs_n_of_[0],
								self.title[1],fgs_n_of_[1],
								self.title[2],fgs_n_of_[2],
								self.title[3],fgs_n_of_[3],
								fgs_dietary_supplement, fgs_other_component,
								self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		bSizer2.Fit(self)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Results_and_problems_origin
		global breakfast_offset
		
		n_of_num=len(self.breakfast)
		print "n_of_num",n_of_num
		saved_factor=[]
		saved_factor.append(["0","1","2","3","NA"])#fruits
		saved_factor.append(["0","1","2","3","NA"])#eggs
		saved_factor.append(["0","1","2","NA"])#meat
		saved_factor.append(["0","1","2","3","NA"])#cheese	
		
		
		#saving all radio buttons
		for i in range (len(self.breakfast)):
			j=-1
			for values in self.breakfast[i]:
				j+=1
				if values.GetValue():
					rb_string=saved_factor[i][j]
			row_to_add[breakfast_offset+i]=rb_string

		
		# saving individual checkbox groups
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
		print "n of chk",len(self.chk)
		print "n of chk string",len(chk_string)
		for i in range(len(self.chk)):
			print i
			row_to_add[breakfast_offset+n_of_num+i]=chk_string[i]
		
		
		chk_string=[]
		for values in self.chk2:
			i+=1
			#print i,values.GetValue()
			if values.GetValue():
				#print "assinging"
				chk_string.append(1)
				one_checked=True
			else:
				chk_string.append(0)	
		print "n of chk",len(self.chk2)
		print "n of chk string",len(chk_string)
		for i in range(len(self.chk2)):
			print i
			row_to_add[breakfast_offset+n_of_num+3+i]=chk_string[i]
		print row_to_add
		new_day_row(row_to_add)
		
		
class Beverage(wx.Panel):
	def __init__(self, parent, title):
		global breakfast_offset
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(14, 2, 9, 25)
		fgs_dietary_supplement = wx.FlexGridSizer(9, 1, 9, 25)
		fgs_other_component=wx.FlexGridSizer(4, 2, 9, 25)
		fgs_n_of_=[]
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 5,  9, 25))
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		i=-1
		self.title=[]
		self.breakfast=[]
		self.labs=[	["None","1/2l","1l","1,5l"], #water 
				["None","1/2l","1l","1,5l"], #sparkling water
				["None","1 glass","more than one glass"], #alcohol
				["None","25cl","50cl","1l or more"],#fruit juice
				["None","25cl","50cl","1l or more"],#fresh juice
				["None","25cl","50cl","1l or more"],#sodas
				["None","1","2","3 or more"], #coffee
				["None","1","2","3 or more"],#tea
				["None","1","2","3 or more"],#milk beverageg
				["None","1","2","3 or more"],#infusion
				]
		self.dict_translate={
		"None":0,
		"1/2l":0.5,
		"1l":1,
		"1,5l":1.5,
		"1 glass":0.1,
		"more than one glass":"many",
		"25cl":0.25,
		"50cl":0.5,
		"1l or more":"much",
			"1":1,
			"2":2,
			"3 or more":"much"
			}
		
		#Water
		i+=1#0
		labels=self.labs[i]

		self.title.append(wx.StaticText(self, label="Water:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		#Sparkling Water
		labels=["None","1/2l","1l","1,5l"]
		i+=1#1
		self.title.append(wx.StaticText(self, label="Sparkling Water:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Alcohol
		i+=1#2
		self.title.append(wx.StaticText(self, label="Alcohol:"))
		labels=self.labs[i]
		self.breakfast.append([])
		for n in range(3):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][3].SetValue(False)
		
		#Fruit juice
		i+=1#3
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Fruit Juice:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Frensh fruit or vegetable juice
		i+=1#4
		
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Fresh fruit or vegetable juice :"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Sodas
		i+=1#5
		
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Sodas:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Coffee
		i+=1#6
		
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Coffee:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Tea
		i+=1#7
		
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Tea:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		#Milk beverage
		i+=1#7
		
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Milk Beverage:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		#Infusion
		i+=1#7
		
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Infusion:"))
		self.breakfast.append([])
		for n in range(4):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][4].SetValue(False)
		
		
		
		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		self.chk=[]
		#self.chk.append(wx.CheckBox(self, -1, 'Meal substitute taken'))
		
		
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[breakfast_offset+i]==1:
				self.chk[i].SetValue(True)

		
		self.chk2=[]
		#self.chk2.append(wx.CheckBox(self, -1, 'Bread taken'))
		
		# ------------------------------ filling containers
		
		fgs_n_of_[0].AddMany(self.breakfast[0])
		fgs_n_of_[1].AddMany(self.breakfast[1])
		fgs_n_of_[2].AddMany(self.breakfast[2])
		fgs_n_of_[3].AddMany(self.breakfast[3])
		fgs_n_of_[4].AddMany(self.breakfast[4])
		fgs_n_of_[5].AddMany(self.breakfast[5])
		fgs_n_of_[6].AddMany(self.breakfast[6])
		fgs_n_of_[7].AddMany(self.breakfast[7])
		fgs_n_of_[8].AddMany(self.breakfast[8])
		fgs_n_of_[9].AddMany(self.breakfast[9])
		fgs_dietary_supplement.AddMany(self.chk[0:8])
		fgs_other_component.AddMany(self.chk2[0:8])
		fgs_container.AddMany([	self.title[0],fgs_n_of_[0],
								self.title[1],fgs_n_of_[1],
								self.title[2],fgs_n_of_[2],
								self.title[3],fgs_n_of_[3],
								self.title[4],fgs_n_of_[4],
								self.title[5],fgs_n_of_[5],
								self.title[6],fgs_n_of_[6],
								self.title[7],fgs_n_of_[7],
								self.title[8],fgs_n_of_[8],
								self.title[9],fgs_n_of_[9],
								fgs_dietary_supplement, fgs_other_component,
								self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Results_and_problems_origin
		saved_factor=[]
		j=-1
		#retreivng labels
		
		for i in range (len(self.breakfast)):
			saved_factor.append([])
			for j in range(len(self.labs[i])):
				saved_factor[i].append("NA")
				string=self.labs[i][j]
				saved_factor[i][j]=self.dict_translate[self.labs[i][j]]
		print saved_factor
		
		
		#saving all radio buttons
		for i in range (len(self.breakfast)):#iterating thru radio groups
			j=-1
			for values in self.breakfast[i]:#iterating thru radio buttons
				j+=1
				if values.GetValue():
					rb_string=saved_factor[i][j]
			row_to_add[beverage_offset+i]=rb_string
		
		num_of_n=len(saved_factor)
		#print row_to_add
		new_day_row(row_to_add)
		
		
		
class Body_state(wx.Panel):
	def __init__(self, parent, title):
		global breakfast_offset
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(9, 4, 9, 25)
		fgs_aches = wx.FlexGridSizer(9, 1, 9, 25)
		fgs_other_component=wx.FlexGridSizer(4, 2, 9, 25)
		fgs_n_of_=[]
		fgs_n_of_.append(wx.FlexGridSizer(9, 1,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(9, 1,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(9, 1,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(9, 1,  9, 25))
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		i=-1
		self.title=[]
		self.breakfast=[]
	
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		self.chk=[]
		self.chk.append([])
		self.title.append(wx.StaticText(self, label="Aches:"))#0
		self.chk[0].append(wx.CheckBox(self, -1, 'Breasts'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Back'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Legs'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Gluteal'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Feet'))
		self.chk[0].append(wx.CheckBox(self, -1, 'Perineum'))
		self.chk[0].append(wx.CheckBox(self, -1, 'belly'))
		
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[breakfast_offset+i]==1:
				self.chk[i].SetValue(True)

		
		self.chk.append([])
		self.title.append(wx.StaticText(self, label="Other problems:"))#1
		self.chk[1].append(wx.CheckBox(self, -1, 'cramps'))
		self.chk[1].append(wx.CheckBox(self, -1, 'Nausea'))
		
		
		self.chk.append([])
		self.title.append(wx.StaticText(self, label="lack sensation:"))#2
		self.chk[2].append(wx.CheckBox(self, -1, 'morning'))
		self.chk[2].append(wx.CheckBox(self, -1, 'early afternoon'))
		self.chk[2].append(wx.CheckBox(self, -1, 'late afternoon'))
		self.chk[2].append(wx.CheckBox(self, -1, 'evening'))
		
		
		self.chk.append([])
		self.title.append(wx.StaticText(self, label="gastroesophageal reflux:"))#3
		self.chk[3].append(wx.CheckBox(self, -1, 'morning'))
		self.chk[3].append(wx.CheckBox(self, -1, 'early afternoon'))
		self.chk[3].append(wx.CheckBox(self, -1, 'late afternoon'))
		self.chk[3].append(wx.CheckBox(self, -1, 'evening'))
		
		# ------------------------------ filling containers
		
		fgs_n_of_[0].AddMany(self.chk[0])
		fgs_n_of_[1].AddMany(self.chk[1])
		fgs_n_of_[2].AddMany(self.chk[2])
		fgs_n_of_[3].AddMany(self.chk[3])
		fgs_container.AddMany([	self.title[0],self.title[1],self.title[2],self.title[3],
								fgs_n_of_[0],fgs_n_of_[1],fgs_n_of_[2],fgs_n_of_[3],
								
								
								self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global Results_and_problems_origin
		global body_tate_offset
		
		# saving all checkbox groups
		
		chk_string=[]
		for i in range(len(self.chk)):#iterating thru checkbox groups
			j=-1
			for values in self.chk[i]:#iterating thru checkboxes
				j+=1
				#print i,values.GetValue()
				if values.GetValue():
					#print "assinging"
					chk_string.append(1)
					one_checked=True
				else:
					chk_string.append(0)	
			print "n of chk",len(self.chk[i])
			print "n of chk string",len(chk_string)
		for k in range(len(chk_string)):
			print k
			row_to_add[body_state_offset+k]=chk_string[k]
																	
		print row_to_add
		new_day_row(row_to_add)
		
		
		
class Body_signs(wx.Panel):
	def __init__(self, parent, title):
		global breakfast_offset
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(12, 2, 9, 25)
		fgs_dietary_supplement = wx.FlexGridSizer(3, 2, 9, 25)
		fgs_other_component=wx.FlexGridSizer(4, 2, 9, 25)
		fgs_n_of_=[]
		fgs_n_of_.append(wx.FlexGridSizer(1, 11,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 11,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 11,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 11,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 11,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 11,  9, 25))
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		self.empty2=wx.StaticText(self, label="")
		
		
		self.title=[]
		self.breakfast=[]
		
		self.labs=[
					["1","2","3","4","5","6","7","8","9","10","NA"],#vitality
					["1","2","3","4","5","6","7","8","9","10","NA"],#tireness
					["None","A little","A lot","NA"],#dark circle strength
					["Brown","Black","Green","White","NA"],#dark circles color
					["Diarhea","Soft stool","Almost good consistency","Good consistency","Constipation","NA"],#stools
					["Brown","Deep yellow","Clear yellow", "NA"]]#urine color
		
		self.dict_translate={
		"NA":"NA",
		"1":1,
		"2":2,
		"3":3,
		"4":4,
		"5":5,
		"6":6,
		"7":7,
		"8":8,
		"9":9,
		"10":10,
		"None":"None",
		"A little":"a_little",
		"A lot":"a_lot",
		"Brown":"brown",
		"Black":"black",
		"Green":"green",
		"White":"white",
		"Diarhea":"diarhea",
		"Soft stool":"soft_stool",
		"Almost good consistency":"almost_good",
		"Good consistency":"good",
		"Constipation":"constipation",
		"Deep yellow":"deep_yellow",
		"Clear yellow":"clear_yellow"}
		
		
		#brown terre 
		#black eau 
		#Gren bois 
		#white metal
		
		i=-1
		#Vitality
		
		i+=1#0
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Vitality:"))
		self.breakfast.append([])
		
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		
		
		#Tireness
		
		i+=1#1
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Tireness:"))
		self.breakfast.append([])
		
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
				
		#dark circles strength
	
		i+=1#2
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Dark circles:"))
		self.breakfast.append([])
		
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		
		
		
		#Dark circles color
		
		#brown terre 
		#black eau 
		#Gren bois 
		#white metal
		i+=1#3
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Dark circle color:"))
		self.breakfast.append([])
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
	
	
	
		#Stools
		i+=1#4
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Stools:"))
		self.breakfast.append([])
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
				
				
				
		#Urine color
		i+=1#5
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Urine:"))
		self.breakfast.append([])
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
				
				
		self.chk=[]
		self.chk.append([])
		self.title.append(wx.StaticText(self, label="other problems:"))#6
		self.chk[0].append(wx.CheckBox(self, -1, 'Cellulite'))
		
		
		
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[breakfast_offset+i]==1:
				self.chk[i].SetValue(True)
				
				

		# ------------------------------ filling containers
		
		fgs_n_of_[0].AddMany(self.breakfast[0])
		fgs_n_of_[1].AddMany(self.breakfast[1])
		fgs_n_of_[2].AddMany(self.breakfast[2])
		fgs_n_of_[3].AddMany(self.breakfast[3])
		fgs_n_of_[4].AddMany(self.breakfast[4])
		fgs_n_of_[5].AddMany(self.breakfast[5])
		
		fgs_dietary_supplement.AddMany(self.chk[0])
		fgs_container.AddMany([	self.title[0],fgs_n_of_[0],
								self.title[1],fgs_n_of_[1],
								self.title[2],fgs_n_of_[2],
								self.title[3],fgs_n_of_[3],
								self.title[4],fgs_n_of_[4],
								self.title[5],fgs_n_of_[5],
								self.empty,	self.title[6],
								self.empty2,fgs_dietary_supplement,self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		pass
			
				
	def Click(self,event):#problems and results
		global row_to_add
		global body_signs_offset
		
		#retreivng labels
		saved_factor=[]
		print "n of num", len(self.breakfast)
		for i in range (len(self.breakfast)):
			print "i",i
			saved_factor.append([])
			for j in range(len(self.labs[i])):
				print  "j",j
				saved_factor[i].append("NA")
				string=self.labs[i][j]
				saved_factor[i][j]=self.dict_translate[self.labs[i][j]]
		print saved_factor
		
		
		#saving all radio buttons
		for i in range (len(self.breakfast)):#iterating thru radio groups
			j=-1
			for values in self.breakfast[i]:#iterating thru radio buttons
				j+=1
				if values.GetValue():
					rb_string=saved_factor[i][j]
			row_to_add[body_signs_offset+i]=rb_string
		
		num_of_n=len(saved_factor)
		
		# saving all checkbox groups
		chk_string=[]
		for i in range(len(self.chk)):#iterating thru checkbox groups
			j=-1
			for values in self.chk[i]:#iterating thru checkboxes
				j+=1
				#print i,values.GetValue()
				if values.GetValue():
					#print "assinging"
					chk_string.append(1)
					one_checked=True
				else:
					chk_string.append(0)	
			print "n of chk",len(self.chk[i])
			print "n of chk string",len(chk_string)
		for k in range(len(chk_string)):
			print k
			row_to_add[body_signs_offset+num_of_n+k]=chk_string[k]
				
		#print row_to_add
		new_day_row(row_to_add)
		
		
		
class Physical_activity(wx.Panel):
	def __init__(self, parent, title):
		global breakfast_offset
		#----------------------------------------------- container creation
		fgs_container = wx.FlexGridSizer(9, 2, 9, 25)
		fgs_dietary_supplement = wx.FlexGridSizer(9, 1, 9, 25)
		fgs_other_component=wx.FlexGridSizer(4, 2, 9, 25)
		fgs_n_of_=[]
		fgs_n_of_.append(wx.FlexGridSizer(1, 8,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 8,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 8,  9, 25))
		fgs_n_of_.append(wx.FlexGridSizer(1, 8,  9, 25))
		
		#--------------------------------------------------- panel start
		wx.Panel.__init__(self, parent)
		bSizer  = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		self.empty=wx.StaticText(self, label="")
		
		i=-1
		self.title=[]
		self.breakfast=[]
		self.labs=[
					["None","10min","10-30min","30-1h","1h et +"],#walking
					["None","5","10","15","20"],#push ups
					["None","100m","200m","300m","400m","500m","more"],#swimming
					["None","0min","24min","45min","more"]#meditation
					]
		self.dict_translate={
		"None":0,
		"10min":"10",
		"10-30min":"10-30",
		"30-1h":"30-60",
		"1h et +":"much",
		"5":5,
		"10":10,
		"15":15,
		"20":20,
		"100m":100,
		"200m":200,
		"300m":300,
		"400m":400,
		"500m":500,
		"more":"much",
		"0min":0,
		"24min":24,
		"45min":45,
		"more":"much"
			}
		
		#Walking
		
		i+=1#0
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Walking:"))
		self.breakfast.append([])
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][len(labels)].SetValue(False)
		
		#Push ups
		
		i+=1#1
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Push ups:"))
		self.breakfast.append([])
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][len(labels)].SetValue(False)
		
		#Swimming
		
		i+=1#2
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Swimming:"))
		self.breakfast.append([])
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][len(labels)].SetValue(False)
		
		#Meditation
		
		i+=1#3
		labels=self.labs[i]
		self.title.append(wx.StaticText(self, label="Meditation:"))
		self.breakfast.append([])
		for n in range(len(labels)):
			if (n==0):
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n],style=wx.RB_GROUP))
			else:
				self.breakfast[i].append(wx.RadioButton(self, label=labels[n]))
			self.breakfast[i][n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.breakfast[i][n].SetValue(False)
		self.breakfast[i].append(wx.RadioButton(self, label="NA"))
		self.breakfast[i][len(labels)].SetValue(False)
		
		
		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		
		self.chk=[]
		self.chk.append([])
		self.chk[0].append(wx.CheckBox(self, -1, 'regenerating motion'))
		self.chk[0].append(wx.CheckBox(self, -1, 'surya namaskar'))
		
		for i in range(len(self.chk)):#loading current row values into form
			if row_to_add[breakfast_offset+i]==1:
				self.chk[i].SetValue(True)

		
		self.chk.append([])
		#self.chk2.append(wx.CheckBox(self, -1, 'Bread taken'))
		
		# ------------------------------ filling containers
		
		fgs_n_of_[0].AddMany(self.breakfast[0])
		fgs_n_of_[1].AddMany(self.breakfast[1])
		fgs_n_of_[2].AddMany(self.breakfast[2])
		fgs_n_of_[3].AddMany(self.breakfast[3])
		
		fgs_dietary_supplement.AddMany(self.chk[0][0:8])
		fgs_other_component.AddMany(self.chk[1][0:8])
		fgs_container.AddMany([	self.title[0],fgs_n_of_[0],
								self.title[1],fgs_n_of_[1],
								self.title[2],fgs_n_of_[2],
								self.title[3],fgs_n_of_[3],
								
								fgs_dietary_supplement, fgs_other_component,
								self.button3])
		#bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
		# ------------------------------------------------- panel methods ---------------------------------------------------

	
	def SetVal(self,event):
		pass
			
			
	def Click(self,event):#Saving physical activity
		global row_to_add
		global Results_and_problems_origin
		global physical_activity_offset
		
		#retreivng labels
		saved_factor=[]
		print "n of num", len(self.breakfast)
		for i in range (len(self.breakfast)):
			saved_factor.append([])
			for j in range(len(self.labs[i])):
				saved_factor[i].append("NA")
				string=self.labs[i][j]
				saved_factor[i][j]=self.dict_translate[self.labs[i][j]]
		print saved_factor
		
		
		#saving all radio buttons
		for i in range (len(self.breakfast)):#iterating thru radio groups
			j=-1
			for values in self.breakfast[i]:#iterating thru radio buttons
				j+=1
				if values.GetValue():
					rb_string=saved_factor[i][j]
			row_to_add[physical_activity_offset+i]=rb_string
		
		num_of_n=len(saved_factor)
		
		# saving all checkbox groups
		chk_string=[]
		for i in range(len(self.chk)):#iterating thru checkbox groups
			j=-1
			for values in self.chk[i]:#iterating thru checkboxes
				j+=1
				#print i,values.GetValue()
				if values.GetValue():
					#print "assinging"
					chk_string.append(1)
					one_checked=True
				else:
					chk_string.append(0)	
			print "n of chk",len(self.chk[i])
			print "n of chk string",len(chk_string)
		for k in range(len(chk_string)):
			print k
			row_to_add[physical_activity_offset+num_of_n+k]=chk_string[k]
				
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
		occurences=get_string_coord(sheet, date)
		today_n_of_row=len(occurences)
		Today_Dream_filename=day_number.zfill(2)+"_"+month_name_fr[int(month_number)-1]+"_"+year_number+"_"+str(today_n_of_row).zfill(2)

		if occurences==[]:
			
			row_to_add[0]=date
			new_day_row(row_to_add)
			"You did not run the program today creating new row"
		else:
			list_entry=get_string_coord(sheet, date)
			if len(list_entry)>1:
				print "Found more than one entry for today, skipping first day entry values"
				Skip_first_entry=True
			print "reading today last entry" #in case todays date exists in the sheet
										#the number of variable must match between the init list and the loaded sheet
			print "number of variables:",len(row_to_add)
			i=-1
			for cell in range(len(row_to_add)):
				i+=1
				#print occurences
				row_to_add[i]=Read_cell(occurences[0][0]+i,occurences[len(occurences)-1][1])#inserting at the last occurence of the date
			print row_to_add
			
		#---------------------------------------main frontend--------------------------------------------
		
		super(Main_Form, self).__init__(parent,title=title, size=(999, 444))
		
		
		panel = wx.Panel(self)
		nb = wx.Notebook(panel)

		# Create the tab windows
		tab1 = Breakfast (nb, "Breakfast" )
		tab2 = Lunch(nb,"Lunch")
		tab3 = Diner(nb,"Diner")
		tab4 = Snack(nb,"Snack")
		tab5 = Beverage(nb,"Beverage")
		tab7= Physical_activity(nb,"Physical activity")
		tab8 = Body_state(nb,"Body state")
		tab9 = Body_signs(nb,"Body signs")
		# Add the windows to tabs and name them.
		nb.AddPage(tab1, "Breakfast")
		nb.AddPage(tab2, "Lunch")
		nb.AddPage(tab3, "Diner")
		nb.AddPage(tab4, "Snack")
		nb.AddPage(tab5, "Beverage")
		nb.AddPage(tab7, "Physical activity")
		nb.AddPage(tab8, "Body State")
		nb.AddPage(tab9, "Body signs")

			
		#final wrapping
		sizer = wx.BoxSizer()
		sizer.Add(nb, 1, wx.EXPAND)
		panel.SetSizer(sizer)


if __name__ == "__main__":
	app = wx.App()
	#app.font=wx.Font(24,wx.FONTFAMILY_DEFAULT,wx.NORMAL,wx.FONTWEIGHT_NORMAL,False, encoding=wx.FONTENCODING_UTF8)
	

	frame = Main_Form(None,Software_Name)
	app.SetTopWindow(frame)
	frame.Show()
	#print frame.text.GetValue()
	app.MainLoop()
bo
