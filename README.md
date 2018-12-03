# Subjective_data_recorder

## Overview
This is a data recorder coded for lucid dream practice. It can be adapted for any subjective frequent data input.
The principle is just a wx interface related to a xls file.
Procedures in there can be usefull for any data collection, subjective data but also measures with arduino.

## lucid dream practice
Lucid dream is a practice that allows one to live awake experiences in the dream world. It has been researched by Stephen Laberge in the 70s. It has been a buddhist practice for tens of centuries. 
I propose here to use data science to observe your practice of lucid dream. The observation already plays a good role in improving the quantity of result or the quality of sleep. A whole load of statistics are possible along the collected data that represents 36 variables in each row. Many rows a day is now possible, although certain values will not be relevant at each entry.

## installation

### install python 2.7 

### create a folder and put .py and .xls in it

### install dependencies (all modules after "import" keyword at the start of the .py code
(pyexcel, odf, wx)

With ubuntu:


#### pyexcel

sudo apt-get install python-pip

sudo pip install pyexcel

sudo pip install pyexcel-ods

sudo pip install pyexcel-xls

#### odf

sudo apt-get install python-odf python-odf-doc python-odf-tools

#### wx

sudo apt-get install python-wxgtk3.0



## type in a console from the created folder

>python Dream_Recorder_v1.py


the software should start and an interface should appear

## usage
each tab contains some data forms to fill. I usually start with "Dream Report"
I fill the dream report, record it (a tmp file is created and a partial ods file)
I fill the day recall and record it (the ods file is created with both texts)

if it is not a sleep time from evening to morning I add a new empty entry
I fill the Good practice tab and record it
I fill the Dream quality report which will be used to measure the practice results
I record this form
I finally fill the bad practice and record it even if nothing is ticked (else Not Available is inserted)

I then copy the xls and ods files that have been generated into an other folder because the ods is replaced during the whole day if I save a new dream report for another sleep session.

After one month we already have good overview of sleep improvements thru practice.

## known issues
see this section in github


