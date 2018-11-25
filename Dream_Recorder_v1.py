#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#import sys
#text=""
#text = unicode(text, sys.getfilesystemencoding())


#--------------------------------------dependencies-----------------------------------------------
import wx
#import wx.lib.scrolledpanel

import pyexcel 
from pyexcel_ods import get_data
from pyexcel_ods import save_data
from collections import OrderedDict
import datetime

from odf.opendocument import OpenDocumentText#semble accepter les fichiers aux noms accentués
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
output_file=u'lucid_dream_data_2018-2019.xls'

Time_origin=0
Good_practice_origin=5
Bad_practice_origin=Good_practice_origin+7
Results_and_problems_origin=Bad_practice_origin+3

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
			"NA","NA","NA","NA",default_home_name]

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
Today_Dream_filename=date=day_number.zfill(2)+"_"+month_name_fr[int(month_number)-1]+"_"+year_number
Dream_report_tmp="dream_report_today"
Day_recall_tmp="day_recall_tmp"

print Today_Dream_filename

Software_Name="Dream Recorder"



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
		for cell in row:
			i+=1
			occurences=get_string_coord(sheet, date)
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
	
	#print month_string
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

#-------------------------------------------------------------------interface start-------------------------------------------------

class Good_Practice(wx.Panel):
	def __init__(self, parent, title):
		#----------------------------------------------- container creation
		global Skip_first_entry
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
		fgs_more_practice=wx.FlexGridSizer(2, 2, 9, 50)
		
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

		diner_note=range(14)[1:14]#cette ligne génère douze integer de 1 à 13
		for n in range(13):
			if (n==0):
				self.rb2.append(wx.RadioButton(self, label=str(n+1),style=wx.RB_GROUP))
			else:
				self.rb2.append(wx.RadioButton(self, label=str(n+1)))
			self.rb2[n].Bind(wx.EVT_RADIOBUTTON, self.SetVal)
			self.rb2[n].SetValue(False)
		self.rb2.append(wx.RadioButton(self, label="NA"))
		self.rb2[13].SetValue(False)
		for i in range(12):
			if row_to_add[Good_practice_origin+6]==diner_note[i]:
				self.rb2[i].SetValue(True)
			if Skip_first_entry:
				self.rb2[13].SetValue(True)
		
		
		
		# bed time
		self.rb3.append(wx.RadioButton(self, label="22h00",style=wx.RB_GROUP))
		self.rb3.append(wx.RadioButton(self, label="22h30"))
		self.rb3.append(wx.RadioButton(self, label="23h00"))
		self.rb3.append(wx.RadioButton(self, label="23h30"))
		if row_to_add[Time_origin+1]==u"22h00":
			self.rb3[0].SetValue(True)
		if row_to_add[Time_origin+1]==u"22h30":
			self.rb3[1].SetValue(True)
		if row_to_add[Time_origin+1]==u"23h00":
			self.rb3[2].SetValue(True)
		if row_to_add[Time_origin+1]==u"23h30":
			self.rb3[3].SetValue(True)
			
		self.text_evening=wx.TextCtrl(self)
		
		
		# get up time
		self.rb4.append(wx.RadioButton(self, label="06h06",style=wx.RB_GROUP))
		self.rb4.append(wx.RadioButton(self, label="07h07"))
		self.rb4.append(wx.RadioButton(self, label="07h30"))
		self.rb4.append(wx.RadioButton(self, label="08h"))
		print "testing",row_to_add[Time_origin+2]
		if row_to_add[Time_origin+2]==u"08h":
			self.rb4[3].SetValue(True)
		if row_to_add[Time_origin+2]==u"07h07":
			self.rb4[1].SetValue(True)
		if row_to_add[Time_origin+2]==u"07h30":
			self.rb4[2].SetValue(True)
		if row_to_add[Time_origin+2]==u"06h06":
			self.rb4[0].SetValue(True)
	
		#meditation
		self.rb6.append(wx.RadioButton(self, label="0min",style=wx.RB_GROUP))
		self.rb6.append(wx.RadioButton(self, label="24min"))
		self.rb6.append(wx.RadioButton(self, label="30min"))
		self.rb6.append(wx.RadioButton(self, label="45min"))
		self.text_zazen=wx.TextCtrl(self)
		if row_to_add[Good_practice_origin+5]==0:
			self.rb4[0].SetValue(True)
		if row_to_add[Good_practice_origin+5]==24:
			self.rb4[1].SetValue(True)
		if row_to_add[Good_practice_origin+5]==30:
			self.rb4[2].SetValue(True)
		if row_to_add[Good_practice_origin+5]==45:
			self.rb4[3].SetValue(True)
		
		# improving practices
		self.chk.append(wx.CheckBox(self, -1, 'Spirit Offering'))
		self.chk.append(wx.CheckBox(self, -1, 'Practice acceptance dialog'))
		self.chk.append(wx.CheckBox(self, -1, 'Spoken prayers'))	
		
		for i in range(3):
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
			
		self.text_morning=wx.TextCtrl(self)
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
		bSizer.Add(fgs_container, wx.ALL)
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	def SetVal(self,event):# could be used to transfer standard values in text controls
		pass
		
		
	def add_new_row(self,event):# adds empty row
		global row_to_add
		global frame
		global empty_row
		date=datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")
		i=-1
		row_to_add=[]
		for value in empty_row:
			i+=1
			row_to_add.append(empty_row[i])

		print "empty row",empty_row
		blind_add_row(row_to_add)
		frame.Close()
		frame = Main_Form(None,Software_Name)
		app.SetTopWindow(frame)
		frame.Show()
		list_entry=get_string_coord(sheet, date)
		print "loading added row"
		# this should be a separate procedure
		i=-1
		for cell in range(len(row_to_add)):
			i+=1
			occurences=get_string_coord(sheet, date)
			#print occurences
			row_to_add[i]=Read_cell(occurences[0][0]+i,occurences[len(occurences)-1][1])#inserting at the last occurence of the date
		print row_to_add
		#print frame.text.GetValue()
	
		
		
	def Click(self,event):#records the data
		global app
		global row_to_add
		global Time_origin
		global Results_and_problems_origin
		hours_evening=["22h","22h30","23h","23h30"]
		hours_morning=["06h06","07h07","7h30","08h"]
		zazen_minutes=[0,24,30,45]
		#rest_note=map(str,range(13))[1:13]#cette ligne génère une chaine de douze chiffres de 1 à 12
		rest_note=range(14)[1:14]#cette ligne génère douze integer de 1 à 12
		reality_check=range(8)[0:8]
		diner_note=rest_note
		print reality_check
		
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
			row_to_add[Time_origin+1]=rb3_string
			
			
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
		if self.rb2[13].GetValue():#"If NA is checked don't look at the rate"
			print "NA checked"
			row_to_add[Good_practice_origin+6]="NA"
		else:
			for values in self.rb2:
				i+=1
				rb2_string="NA"
				if values.GetValue():
					rb2_string=diner_note[i]
					row_to_add[Good_practice_origin+6]=rb2_string
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
			if values.GetValue():
				#print "assinging"
				row_to_add[Good_practice_origin+2+i]=1
				one_checked=True
			else:
				row_to_add[Good_practice_origin+2+i]=0
				
		#zazen
		if self.text_zazen.GetValue()!="":
			row_to_add[Good_practice_origin+5]=int(self.text_zazen.GetValue())
		else:
			i=-1
			for values in self.rb6:
				i+=1
				rb6_string="NA"
				if values.GetValue():
					rb6_string=zazen_minutes[i]
					row_to_add[Good_practice_origin+5]=rb6_string
					break
		print row_to_add
		new_day_row(row_to_add)
		
			
		
class Dream_report(wx.Panel):
	def __init__(self, parent, title):
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
		self.report=wx.TextCtrl(self,size=(480,350), style = wx.TE_MULTILINE, value=u"")
		self.button3 = wx.Button(self, label="Record Day Recall")
		self.Bind(wx.EVT_BUTTON, self.Click_day_recall, self.button3)
		self.button4 = wx.Button(self, label="Record Dream Report")
		self.Bind(wx.EVT_BUTTON, self.Click_dream_report, self.button4)
		
		self.report.SetFont(font)
		self.day_recall.SetFont(font)
		fgs_d_recall.AddMany([self.day_recall,self.button3])
		fgs_d_report.AddMany([self.report,self.button4])
		fgs_container.AddMany([fgs_d_report,fgs_d_recall])
		bSizer.Add(fgs_container, wx.ALL)
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	def SetVal(self,event):
		state1 = self.rb1.GetValue()
		state2 = self.rb2.GetValue()
		if state1:
			print "Melody"
		if state2: 
			print "Tone"
		
	def Click_dream_report(self,event):
		global Today_Dream_filename
		global Dream_report_tmp
		global Dream_report
		global Day_recall
		
		Dream_report=self.report.GetValue()
		
		print Dream_report
		
		
		textdoc = OpenDocumentText()
		tmpdoc= OpenDocumentText()
		
		s = textdoc.styles#here we define a style for Red font
		bluestyle = Style(name="blue", family="paragraph")
		bluestyle.addElement(TextProperties(attributes={'color':"#0000bf"}))
		s.addElement(bluestyle)
	
	
		#safeguard dream report
			
		p = P(text= Dream_report)
		tmpdoc.text.addElement(p)
	
		p = P(text= Dream_report)
		textdoc.text.addElement(p)
		
		print"Saving", "./"+Today_Dream_filename
		textdoc.save(u"./"+Today_Dream_filename, True)#unicode is important!!
		print"Saving", Dream_report_tmp
		tmpdoc.save(u"./"+Dream_report_tmp, True)
	
			
				
	def Click_day_recall(self,event):# recording in an open document the day recall text box
		global Today_Dream_filename
		global Dream_report_tmp
		global Dream_report
		global Day_recall
		global Good_practice_origin
		global Time_origin
		
		Day_recall=self.day_recall.GetValue()
		
		print Day_recall
		
		textdoc = OpenDocumentText()
		tmpdoc= OpenDocumentText()
		
		s = textdoc.styles#here we define a style for Red font
		bluestyle = Style(name="blue", family="paragraph")
		bluestyle.addElement(TextProperties(attributes={'color':"#0000bf"}))
		s.addElement(bluestyle)
		
		# saving day_recall input to a tmp file in case of crash and to reload it at next start up if in current day
		p = P(text= Day_recall)
		tmpdoc.text.addElement(p)
		
		# date inside document
		#here there might be an existing procedure, 
		#but probably not straightforward to get in french as my system language is english
		month_name_fr=["Janvier",u"Février","Mars","Avril","Mai","Juin","Juillet",u"Aoùt","Septembre","Octobre","Novembre",u"Décembre"]
		month_number=datetime.datetime.strftime(datetime.datetime.now(),"%m")
		day_number=str(datetime.datetime.strftime(datetime.datetime.now(),"%d"))
		year_number=datetime.datetime.strftime(datetime.datetime.now(),"%Y")
	
		date_string=day_number.zfill(2)+" "+month_name_fr[int(month_number)-1]+" "+year_number
		
		p = P(text=date_string)
		tmpdoc.text.addElement(p)
		
		h = H(text= date_string, stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		h = H(text= "", stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		
		# giving hour values in french in the document
		
		h = H(text=u"Je me couche à "+row_to_add[Time_origin+1]+u" et me lève à "+row_to_add[Time_origin+2]+".", stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		h = H(text=u"Je suis reposé à "+str(row_to_add[Results_and_problems_origin])+"/10", stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		if not row_to_add[Good_practice_origin+6] == u"NA":
			h = H(text=u"Le repas du soir était léger à "+str(row_to_add[Good_practice_origin+6])+u"/10 "+".", stylename=bluestyle, outlinelevel=1,)
			textdoc.text.addElement(h)
				
		h = H(text= "", stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		h = H(text= Day_recall, stylename=bluestyle, outlinelevel=1,)
		textdoc.text.addElement(h)
		
		p = P(text= "")
		textdoc.text.addElement(p)
		
		p = P(text= Dream_report)
		textdoc.text.addElement(p)
		
		p = P(text= Dream_report)
		tmpdoc.text.addElement(p)
		
		print"Saving", "./"+Today_Dream_filename
		textdoc.save(u"./"+Today_Dream_filename, True)#unicode is important!!
		print"Saving", Day_recall_tmp
		tmpdoc.save(u"./"+Day_recall_tmp, True)
	
		
		
class Dream_Quality(wx.Panel):# tab with Results and problems
	def __init__(self, parent, title):
		#----------------------------------------------- container creation

		fgs_container = wx.FlexGridSizer(2, 2, 9, 25)
		fgs_dream_quality = wx.FlexGridSizer(12, 1, 9, 25)
		fgs_problems=wx.FlexGridSizer(12, 1, 9, 25)
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
		
		self.chk.append(wx.CheckBox(self, -1, 'Bad remembering'))
		self.chk.append(wx.CheckBox(self, -1, 'Nightmare'))
		self.chk.append(wx.CheckBox(self, -1, 'Night Terror'))
		self.chk.append(wx.CheckBox(self, -1, 'Disturbance while reporting'))
		self.chk.append(wx.CheckBox(self, -1, 'Lack of sleep'))
		self.chk.append(wx.CheckBox(self, -1, 'Animal disturbance'))
		self.chk.append(wx.CheckBox(self, -1, 'Human disturbance'))
		self.chk.append(wx.CheckBox(self, -1, 'Spirit disturbance'))
		self.chk.append(wx.CheckBox(self, -1, 'Agitation'))
		self.chk.append(wx.CheckBox(self, -1, 'Total blackout'))
		self.chk.append(wx.CheckBox(self, -1, 'Night Worry'))
		
		for i in range(21):
			if row_to_add[Results_and_problems_origin+i+2]==1:
				self.chk[i].SetValue(True)

		
		
		
		self.button3 = wx.Button(self, label="Record Form")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		fgs_dream_quality.AddMany(self.chk[0:11])
		fgs_problems.AddMany(self.chk[11:22])
		fgs_container.AddMany([fgs_dream_quality,fgs_problems,self.button3])
		bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
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
			row_to_add[Results_and_problems_origin+2+i]=chk_string[i]
		print row_to_add
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
	
		for i in range(3):
			if row_to_add[Bad_practice_origin+i]==1:
				self.chk[i].SetValue(True)

		
		self.button3 = wx.Button(self, label="Record Entry")
		self.Bind(wx.EVT_BUTTON, self.Click, self.button3)
		
		fgs_dream_quality.AddMany(self.chk[0:8])
		fgs_problems.AddMany(self.chk[8:17])
		fgs_container.AddMany([fgs_dream_quality,fgs_problems,self.button3])
		bSizer.Add(fgs_container, wx.ALL)
		
		# ------------------------------------------------------- form foot
		
			
		bSizer2.Add(fgs_container, wx.ALL)
		self.SetSizer(bSizer2)
	
	
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
		print row_to_add
		new_day_row(row_to_add)
		
		
class Main_Form(wx.Frame):
	
	def __init__(self, parent, title, pos=(10,10)):
		#self.Move(wx.Point(100,100))
		global Skip_first_entry
		# -------------------------------main backend------------------------------------------------
		date=datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%Y")
		
		if get_string_coord(sheet, date)==[]:
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
				occurences=get_string_coord(sheet, date)
				#print occurences
				row_to_add[i]=Read_cell(occurences[0][0]+i,occurences[len(occurences)-1][1])#inserting at the last occurence of the date
			print row_to_add

		#---------------------------------------main frontend--------------------------------------------
		
		super(Main_Form, self).__init__(parent,title=title, size=(999, 444))
		
		
		panel = wx.Panel(self)
		nb = wx.Notebook(panel)

		# Create the tab windows
		tab1 = Good_Practice (nb, "Good Practice" )
		tab5 = Bad_Practice(nb,"Bad Practice")
		tab3 = Dream_report(nb,"Dream Report")
		tab2 = Dream_Quality(nb,"Dream Quality")
		#tab5 = Directories(nb,"Directories")
		# Add the windows to tabs and name them.
		nb.AddPage(tab1, "Good Practice")
		nb.AddPage(tab2, "Dream Quality")
		nb.AddPage(tab3, "Dream Report")
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
