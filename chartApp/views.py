# -*- coding: utf8 -*-

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, Http404
from .models import ParaMeasure, DataMeasure, StationUser
from .fusioncharts import FusionCharts
from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError
import os
import datetime



def home(request):
    paraMeasure = ParaMeasure.objects.all()

    return render(request, 'home.html', {'paraMeasures':paraMeasure})
def page(request, pk):

	try:
		#print (request.user)
		a = StationUser.objects.filter(user=request.user)
		

		link_folder = os.path.abspath("data")
		for filename in os.listdir(link_folder):
			temp = filename.split("_")
			#print (temp[-2])
			if (request.user.username == temp[0]):
				#print (temp[1])
				a = StationUser.objects.filter(user=request.user)
				if len(a) == 0:
					station = StationUser.objects.create(station_name=temp[-2], user=request.user)
					
				else:
				
					if all([sta.station_name != temp[-2] for sta in a]):
						try: 
							station = StationUser.objects.create(station_name=temp[-2], user=request.user)
							#print ("hehe")
						except IntegrityError:
							pass
					#print ("hello")
					station = StationUser.objects.get(station_name=temp[-2], user=request.user)
				
			

				f = open(os.path.join(link_folder,filename), 'r+')
					#dataString.append(f.readline().split("\t"))
				for line in f:			
					temp = line.split("\t")
					#print (temp[:4])
					if len(temp) >= 4:
						#print (temp)
						#print (station.station_name)
						name, va, dv, ti = temp[:4]

						try:
							tiS = "%s-%s-%s %s:%s:%s" %(ti[:4], ti[4:6], ti[6:8],ti[8:10], ti[10:12], ti[12:14])
							time = datetime.datetime.strptime(tiS,"%Y-%m-%d %H:%M:%S")
						except ValueError:
							error = 2
							return render(request, 'error_login.html', {'pk':pk, 'error':error})
						ptemp = ParaMeasure.objects.filter(nameStation=station)
						#print (ptemp)
						if (len(ptemp)):
						
							if all([name != iName.name for iName in ptemp]):
									try:
										sub = ParaMeasure.objects.create(name=name, unit=dv,nameStation=station)
										DataMeasure.objects.create(value=va, label=ti, paraStation=sub, last_updated=time)
										
										print ("test1", station.station_name)
									except IntegrityError:
										pass
							else:
								for iName in ptemp:
									if name == iName.name:
										DataMeasure.objects.create(value=va, label=ti, paraStation=iName, last_updated=time)
								
								#print ("test2", iName.nameStation.station_name)
						else:
							#for station in stationQuery:
							#print ((station))
							try:
								sub = ParaMeasure.objects.create(name=name, unit=dv, nameStation=station)
								DataMeasure.objects.create(value=va, label=ti, paraStation=sub, last_updated=time)
								
								#print ("test3", name)
							except IntegrityError:
								print ("error")
								pass
				#f.truncate(0)
				f.close()
				os.remove(os.path.join(link_folder,filename))
		column2D = []
			#print (column2D)
		#for us in User.objects.all():
		#print (type(request.user.username))
		#print ((request.user.username)=="trinh102")
		cment_1 = 1
		if int(pk)==1:
			dataSource = {}
			column2D = []
			xID = 100
			a = StationUser.objects.filter(user=request.user)
			for station in a:
				ptemp = ParaMeasure.objects.filter(nameStation=station)
				for j in ptemp:
					dataSource = {}
					dataSource['data'] = []
					dataSource['chart'] = { 
								        
								        "subCaption": "Measurement",
								        "xAxisName": "Time",
								        
								        "numberPrefix": "1",
								        "alternatehgridalpha": "5",
									    "anchorbgcolor": "BBDA00",
									    "anchorbordercolor": "FFFFFF",
									    "anchorborderthickness": "2",
									    "anchorradius": "4",
									    "basefontcolor": "FFFFFF",
									    "bgalpha": "100",
									    "bgcolor": "406181, 6DA5DB",
									    "canvasbgalpha": "0",
									    "canvasbordercolor": "FFFFFF",
									    "canvaspadding": "10",
									    
									    "divlinealpha": "100",
									    "divlinecolor": "FFFFFF",
									    "labeldisplay": "ROTATE",
									    "slantlabels": "1",
								        "anchorradius": "0",
								        "anchorgbalpha": "50",
									    "linecolor": "BBDA00",
									    "numbersuffix": "",
									    "numvdivlines": "10",
									    "showalternatevgridcolor": "1",
									    "showborder": "0",
									    "showvalues": "0",
									    "tooltipbgcolor": "406181",
									    "tooltipbordercolor": "406181",
									    "vdivlineisdashed": "1",
									    "vdivlinecolor": "#ffffff",
									    "vdivlinealpha": "100",
									    "yaxismaxvalue": "100",
									    "animation": "0",
								        }
					if j.nameStation.user == request.user:
						dtemp = DataMeasure.objects.filter(paraStation=j).order_by("-last_updated").reverse()
						for i in dtemp:
							if (i.paraStation.name) == j.name:
						
								#print (j.nameStation.user)
								
								dataSource['id'] = i.paraStation.name + '_' + j.nameStation.station_name
								dataSource['station'] = j.nameStation.station_name
								dataSource['name'] = i.paraStation.name + j.nameStation.station_name
								dataSource['chart'].update({ 
									"caption": i.paraStation.name,
									"yAxisName": "Value (%s)" %j.unit,
									})
								
								data = {}
								data['value'] = i.value
								data['label'] = (i.last_updated.strftime('%H:%M %d/%m'))#i.label[8:10]+':'+i.label[10:12]#+' '+i.label[6:8]+'-'+i.label[4:6]+'-'+i.label[:4]
								dataSource['data'].append(data)
								"""
								else:
									xID = xID + 1
									dataSource['id'] = xID
									dataSource['name'] = i.paraStation.name 
									dataSource['chart'].update({ 
							        "caption": i.paraStation.name,
							        })
									
									data = {}
									data['value'] = i.value
									data['label'] = (i.last_updated.strftime('%H:%m %d/%m'))#i.label[8:10]+':'+i.label[10:12]#+' '+i.label[6:8]+'-'+i.label[4:6]+'-'+i.label[:4]
									dataSource['data'].append(data)
									"""
				
						#print (len(dataSource['data']))
						#tao du lieu bieu do
						if len(dataSource['data']):
							#print (dataSource['id'],  dataSource['name'])
							column2D.append(FusionCharts("line", (dataSource['id']),dataSource['station'] , "1000", "250", dataSource['name'], "json", dataSource))
			return render(request, 'trang1.html', {'column2D' : column2D, 'station':a, 'pk': pk})

		elif int(pk)==2:
			"""print (len(a))
			for usertemp in a:
				print (usertemp.station_name)
			print (request.path)"""
			return  render(request, 'trang2.html', { 'pk':pk , 'station':a, 'cment_1':cment_1})
		elif int(pk)==3:
			dem = 0
			dem2 = 0
			dataTable = {}
			time = datetime.datetime.now()

			return render(request, 'trang3.html', {'dataTable':dataTable, 'pk':pk, 'station':a, 'cment_1':cment_1})
		elif int(pk)==4:
			return render(request, 'trang4.html', {'pk':pk})
		elif int(pk)==5:
			return render(request, 'trang5.html', {'pk':pk})
		elif int(pk)==6:
			return render(request, 'trang6.html', {'pk':pk})
	except TypeError:
		error = 1
		return render(request, 'error_login.html', {'pk':pk, 'error':error})
def page2(request, pk, slug):
	path = (request.path).split("/")
	#print (len(request.GET))
	filt_var = False
	if len(request.GET):
		temp = (request.GET)
		if (temp['filter_from'] != '') and (temp['filter_to'] != ''):
			filt_var = True
			tiS = temp['filter_from'] + ' 00:00:00'
			tiE = temp['filter_to'] + ' 23:59:59'
			time_start = datetime.datetime.strptime(tiS,"%m/%d/%Y %H:%M:%S")
			time_end = datetime.datetime.strptime(tiE,"%m/%d/%Y %H:%M:%S")
		else:
			filt_var = False

	dataSource = {}
	column2D = []
	xID = 10
	a = StationUser.objects.filter(user=request.user, station_name=slug)
	#print (a[0].station_name)
	ptemp = ParaMeasure.objects.filter(nameStation=a[0])
	cment_1 = 2
	#dtemp = ParaMeasure.objects.filter(nameStation=station)
	#print (type(pk))
	if pk == "2":
		for j in ptemp:
			dataSource = {}
			dataSource['data'] = []
			dataSource['chart'] = { 
						        
						        "subCaption": "Measurement",
						        "xAxisName": "Time",
						        "yAxisName": "Value",
						        "numberPrefix": "1",
						        "alternatehgridalpha": "5",
							    "anchorbgcolor": "BBDA00",
							    "anchorbordercolor": "FFFFFF",
							    "anchorborderthickness": "2",
							    "anchorradius": "4",
							    "basefontcolor": "FFFFFF",
							    "bgalpha": "100",
							    "bgcolor": "406181, 6DA5DB",
							    "canvasbgalpha": "0",
							    "canvasbordercolor": "FFFFFF",
							    "canvaspadding": "10",
							    
							    "divlinealpha": "100",
							    "divlinecolor": "FFFFFF",
							    "labeldisplay": "ROTATE",
							    "slantlabels": "1",
						        "anchorradius": "0",
						        "anchorgbalpha": "10",
							    "linecolor": "BBDA00",
							    "numbersuffix": "",
							    "numvdivlines": "10",
							    "showalternatevgridcolor": "0",
							    "showborder": "0",
							    "showvalues": "0",
							    "tooltipbgcolor": "406181",
							    "tooltipbordercolor": "406181",
							    "vdivlineisdashed": "1",
							    "vdivlinecolor": "#ffffff",
							    "vdivlinealpha": "100",
							    "yaxismaxvalue": "100",
							    "animation": "0",
						        }
			if j.nameStation.user == request.user:
				dtemp = DataMeasure.objects.filter(paraStation=j).order_by("-last_updated").reverse()
				for i in dtemp:
					if (i.paraStation.name) == j.name:
						if filt_var:
							if time_start <= i.last_updated.replace(tzinfo=None) <= time_end:
								#print (j.nameStation.user)
								#xID = xID + 1
								dataSource['id'] = i.paraStation.name + '_' + j.nameStation.station_name
								dataSource['name'] = i.paraStation.name + j.nameStation.station_name
								dataSource['chart'].update({ 
						        "caption": i.paraStation.name,
						        "yAxisName": "Value (%s)" %j.unit,	
						        })
								
								data = {}
								data['value'] = i.value
								data['label'] = (i.last_updated.strftime('%H:%M %d/%m'))#i.label[8:10]+':'+i.label[10:12]#+' '+i.label[6:8]+'-'+i.label[4:6]+'-'+i.label[:4]
								dataSource['data'].append(data)
						else:
							xID = xID + 1
							dataSource['id'] = xID
							dataSource['id'] = i.paraStation.name + '_' + j.nameStation.station_name
							dataSource['name'] = i.paraStation.name + j.nameStation.station_name
							dataSource['chart'].update({ 
					        "caption": i.paraStation.name,
					        })
							
							data = {}
							data['value'] = i.value
							data['label'] = (i.last_updated.strftime('%H:%M %d/%m'))#i.label[8:10]+':'+i.label[10:12]#+' '+i.label[6:8]+'-'+i.label[4:6]+'-'+i.label[:4]
							dataSource['data'].append(data)
							
		
				#print (len(dataSource['data']))
				#tao du lieu bieu do
				if len(dataSource['data']):
					#print (dataSource['id'],  dataSource['name'])
					column2D.append(FusionCharts("line", str(dataSource['id']),j.nameStation.station_name , "1000", "250", dataSource['name'], "json", dataSource))
		return render(request, 'trang2.html', {'column2D' : column2D, 'slug':slug , 'station':a, 'cment_1':cment_1, 'pk': pk})
	elif pk == "3":
		dem = 0
		dem2 = 0
		dataTable = {}
		dataTable['data'] = []
		dataTable['sub'] = ptemp
		for j in ptemp:
			dtemp = DataMeasure.objects.filter(paraStation=j).order_by("-last_updated").reverse()
			for i in dtemp:
				if filt_var:
					if time_start <= i.last_updated.replace(tzinfo=None) <= time_end:
						dataTable['data'].append(i)
				else:
					dataTable['data'].append(i)
			#print (j.name)

		dataTable['numCol'] = dem
		#dataTable['is_Account'] = dem2
		#print (dem)
		#print (dataTable)
		return render(request, 'trang3.html', {'dataTable':dataTable, 'slug':slug, 'station':a, 'cment_1':cment_1, 'pk': pk})

def settingAcc(request):
	return render(request, 'setting.html')

