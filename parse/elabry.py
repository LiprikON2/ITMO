import requests# для парсинга 
import time # для слипа парсинга
import BD
import urllib.request
from urllib.request import urlretrieve# ДЛЯ СКАЧИВАНИЯ
import PyPDF2#ДЛЯ РАБОТЫ С ПДФ
import os # ПОТОМУ ЧТО НАДО
from win32com.shell import shell, shellcon # ДЛЯ ОЧИСТКИ ПДФ
#запись в файл
import win32com.client
import webbrowser # для скачивания 
import openpyxl
from config import direct
import random

global pages
pages=680# c какой строки начинать запись в Excel
# шаг для парсинга 
global step
step=300

global name
name='Gant'


def check_pdf(url:str,pages:int):
	print(url)
	#открываем файл в эксель 
	Excel = win32com.client.Dispatch("Excel.Application")
	wb = Excel.Workbooks.Open(u'{}\\{}\\{}\\{}\\{}\\BIGDAT1.xlsx'.format(direct[0],
																		direct[1],
																		direct[2],
																		direct[3],
                                                                        direct[4],
																		))
	print(wb)
	sheet = wb.ActiveSheet
	text=''
	balans=[0 for i in range(6)]
	destination = 'file1.pdf'
	try:
		urlretrieve(url, destination)
		# чтение файла
		pl = open('file1.pdf', 'rb')
		plread = PyPDF2.PdfFileReader(pl)
		for i in range(plread.numPages):
			getpage = plread.getPage(i)
			text += getpage.extractText().lower()
		#количество повторов 
		#закрываем pdf удаляем его с пк
		pl.close()
		path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'file1.pdf')
		os.remove(path)

		#добавляем в лист определенные параметры
		for word in BD.dev:
			balans[0]+=len(text.split(str(word)))
	
		for word in BD.need:
			balans[1]+=len(text.split(str(word)))
	
		for word in BD.suc:
			balans[2]+=len(text.split(str(word)))
	
		for word in BD.result:
			balans[3]+=len(text.split(str(word)))
	
		for word in BD.realiz:
			balans[4]+=len(text.split(str(word)))
		# загружаем в excel
		balans[5]=plread.numPages 
		for i in range(6):
			sheet.Cells(1+pages,i+2).value=balans[i]
		sheet.Cells(1+pages,1).value=url

		#закрываем лист

		wb.Save()
		wb.Close()
		#закрываем COM объект
		Excel.Quit()
	except urllib.error.HTTPError:
		print('Error pdf')
	except PyPDF2.utils.PdfReadError:
		print('Файл лежит на сайте ')
	except TimeoutError:
		print('Этот сайт возможно не дейст. ')
	except ConnectionResetError:
		print('Этот сайт возможно не дейст. ')
	#except urllib3.exceptions.ProtocolError:
		#print('Этот сайт возможно не дейст. ',url)
	except requests.exceptions.ConnectionError:
		print('Этот сайт возможно не дейст. ')
	except FileNotFoundError:
		print('Неккоренктный файл')
	except NameError:
		print('Этот сайт возможно не дейст. ')
	except urllib.error.URLError:
		print('Этот сайт возможно не дейст. ')

def check_dow(url:str,pages:int):
	# открываем excel
	Excel = win32com.client.Dispatch("Excel.Application")
	wb = Excel.Workbooks.Open(u'{}\\{}\\{}\\{}\\{}\\BIGDAT1.xlsx'.format(direct[0],
																	direct[1],
																	direct[2],
																	direct[3],
                                                                    direct[4],
																	))
	sheet = wb.ActiveSheet
	text=''
	balans=[0 for i in range(6)]
	#скачиваем
	webbrowser.open(url, new=0, autoraise=True)
	time.sleep(6)
	# имя скаченного файла
	directory='{}/{}/{}/{}/{}/IS'.format(direct[0],
										direct[1],
										direct[2],
										direct[3],
                                        direct[4],
										)
	files = os.listdir(directory)
	print(files)
	# смотрим название файла 
	destination = '{}/{}/{}/{}/{}/IS/'.format(direct[0],
											direct[1],
											direct[2],
											direct[3],
                                            direct[4],
											)+files[0]

	try:
		# чтение файла
		pl = open(destination, 'rb')
		plread = PyPDF2.PdfFileReader(pl)
		for i in range(plread.numPages):
			getpage = plread.getPage(i)
			text += getpage.extractText().lower()
		#количество повторов 
		#закрываем pdf удаляем его с пк
		pl.close()
		path = os.path.join(os.path.abspath(os.path.dirname(__file__))+"\\IS", files[0])
		os.remove(path)

		#добавляем в лист определенные параметры
		for word in BD.dev:
			balans[0]+=len(text.split(str(word)))
	
		for word in BD.need:
			balans[1]+=len(text.split(str(word)))
	
		for word in BD.suc:
			balans[2]+=len(text.split(str(word)))
	
		for word in BD.result:
			balans[3]+=len(text.split(str(word)))
	
		for word in BD.realiz:
			balans[4]+=len(text.split(str(word)))
		# загружаем в excel
		balans[5]=plread.numPages 
		for i in range(6):
			sheet.Cells(1+pages,i+2).value=balans[i]
		sheet.Cells(1+pages,1).value=url

		#закрываем лист
		wb.Save()
		# удаляем папку
		wb.Close()
		#закрываем COM объект
		Excel.Quit()
	except urllib.error.HTTPError:
		print('Error pdf')
	except PyPDF2.utils.PdfReadError:
		print('Файл лежит на сайте ')
	except TimeoutError:
		print('Этот сайт возможно не дейст. ',url)
	except urllib3.exceptions.ProtocolError:
		print('Этот сайт возможно не дейст. ',url)
	except requests.exceptions.ConnectionError:
		print('Этот сайт возможно не дейст. ',url)
	except NameError:
		print('Этот сайт возможно не дейст. ',url)

def check_brow(url:str,pages:int):
	Excel = win32com.client.Dispatch("Excel.Application")
	wb = Excel.Workbooks.Open(u'{}\\{}\\{}\\{}\\{}\\BIGDAT1.xlsx'.format(direct[0],
																		direct[1],
																		direct[2],
																		direct[3],
                                                                        direct[4],
																		))
	sheet = wb.ActiveSheet
	text=''
	balans=[0 for i in range(6)]
	try:
		req=requests.get(url)
		text=req.text
		for word in BD.dev:
			balans[0]+=len(text.split(str(word)))
	
		for word in BD.need:
			balans[1]+=len(text.split(str(word)))
	
		for word in BD.suc:
			balans[2]+=len(text.split(str(word)))
	
		for word in BD.result:
			balans[3]+=len(text.split(str(word)))
	
		for word in BD.realiz:
			balans[4]+=len(text.split(str(word)))
		# загружаем в excel
		balans[5]='сайт' 
		for i in range(6):
			sheet.Cells(1+pages,i+2).value=balans[i]
		sheet.Cells(1+pages,1).value=url

		#закрываем лист
		wb.Save()
		# удаляем папку
		wb.Close()
		#закрываем COM объект
		Excel.Quit()

	except ConnectionError:
		print('Ошибка подключения ')
		time.sleep(1)
	except urllib.error.HTTPError:
		print('Error pdf')
	except PyPDF2.utils.PdfReadError:
		print('Файл лежит на сайте ')
	except TimeoutError:
		print('Этот сайт возможно не дейст. ',url)
	except ConnectionResetError:
		print('Этот сайт возможно не дейст. ',url)
	except requests.exceptions.ConnectionError:
		print('Этот сайт возможно не дейст. ',url)
	except NameError:
		print('Этот сайт возможно не дейст. ',url)

def parsing_website(method:str,pages):
	count=(pages-pages%10)# счетчик для parsing фмиксированного числа ссылок 
	#количество запросов 
	req2=requests.get('https://scholar.google.ru/scholar?start=0&q={}&hl=ru&as_sdt=0,5&as_ylo=2018&as_vis=1'.format(method))
	countpage=req2.text.split('Результатов: примерно ')
	countpage=countpage[1].split(' (')
	countpage=countpage[0].split(',')
	countpage=countpage[0].split()
	countpage=countpage[0]+countpage[1]
	arrayurl=list()
	print(countpage)
	# сам парсинг разделов
	start=(pages-pages%10)
	end=start+step
	for i in range(start,end,10):
		req1=requests.get('https://scholar.google.ru/scholar?start={}&q={}&hl=ru&as_sdt=0,5&as_ylo=2018&as_vis=1'.format(i,method))
		x=req1.text.split('href="h')
		m=x[0]
		websites=req1.text.split('href="h')
		for j in range(3,len(websites)):
			count+=1
			url=websites[j]
			url=url.split('"')
			url="h"+url[0]
			#рассматриваем сайт на годность))
			arrayurl.append(url)
			if count==end-1:# фиксация массива ссылко 
				return arrayurl
			print(len(arrayurl),' ',url)
		if i%100==0:
			print('Я сплю')
			time.sleep(random.randint(10,20))
			print(i)

def worked(page,pages):
	for url in page:
		if url[-3:len(url)]=='pdf':
			pages+=1
			check_pdf(url,pages)
		elif len(url.split('download'))>=2:
			pages+=1
			check_dow(url,pages)
		elif url!=None:
			pages+=1
			check_brow(url,pages)
		else:
			continue

if __name__=="__main__":

	for i in range(14):
		page=list()
		page=parsing_website(name,pages)
		print(page)
		page=page
		print('keke')
		worked(page,pages)
		print(pages)
		pages+=step
