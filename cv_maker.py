# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:44:01 2020

@author: rafae
"""

import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4
from reportlab.platypus  import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from datetime import date
PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

WIDTH, HEIGHT = A4
COLOR1 = (45/255, 89/255, 134/255) # Lead blue
COLOR2 = (22/255, 45/255, 65/255) 
WHITE = (1, 1, 1)
BLACK = (0, 0, 0)
FONT1 = ("Helvetica-Bold", 20)
FONT2 = ("Helvetica", 12)
FONT2i = ("Helvetica-Oblique", 12)
FONT3 = ("Helvetica", 8)
FONT3i = ("Helvetica-Oblique", 8)

LEFT_BAR = 5 * cm
TOP_MARGIN = 1 * cm
LEFT_BAR_MARGIN = 0.5 * cm
LANGUAGE = 'en'


with open('cv_'+LANGUAGE+'.json', 'r', encoding = 'utf-8') as file:
    cv_data = json.load(file)
	
ST_EN = {
		'Personal Info' : 'Personal Info',
		'Skills' : 'Skills',
		'PDF created using reportlab library': 'PDF created using reportlab library',
		'Script cv_maker.py availabe at:' : 'Script cv_maker.py available at:',
		'Education' : 'Education',
		'Work experience' : 'Work experience',
		'Research projects': 'Research projects',
		'Patents and publications' : 'Patents and publications',
		'Other achievements' : 'Other achievements',
		'Other' : 'Other'
		}

ST_PT = {
		'Personal Info' : 'Dados Pessoais',
		'Skills' : 'Conhecimentos',
		'PDF created using reportlab library': 'PDF criado com a biblioteca reportlab',
		'Script cv_maker.py availabe at:' : 'Script cv_maker.py disponível em:',
		'Education' : 'Educação',
		'Work experience' : 'Experiência profissional',
		'Research projects': 'Projetos de pesquisa',
		'Patents and publications' : 'Patentes and publicações',
		'Other achievements' : 'Outras atividades',
		'Other' : 'Outro'
		}

if LANGUAGE == 'en':
	ST = ST_EN
elif LANGUAGE == 'pt':
	ST = ST_PT

def firstPage(c, doc):
	c.saveState()
	c.setFillColorRGB(*COLOR2)
	c.setStrokeColorRGB(*COLOR2)
	c.rect(0, 0 ,LEFT_BAR, HEIGHT, stroke = 1, fill = 1)
	textobject = c.beginText()
	textobject.setTextOrigin(LEFT_BAR_MARGIN, HEIGHT - TOP_MARGIN)
	info = cv_data['personal info']
	textobject.setFont(*FONT1)
	textobject.setFillColorRGB(*WHITE)
	for n in info['name'].split(' '):
		textobject.textLine(n)
	textobject.moveCursor(-LEFT_BAR_MARGIN/2, 0)
	textobject.setFont(*FONT2)
	textobject.textLine(ST['Personal Info'])
	for n in ('phone', 'email', 'skype', 'linkedin', 'github'):
		textobject.moveCursor(0, 10)
		n_cap = n[0].upper() + n[1:]
		textobject.setFont(*FONT3i)
		textobject.textLine(n_cap)
		textobject.setFont(*FONT3)
		textobject.textLine(info[n])
	textobject.moveCursor(0, 20)
	textobject.setFont(*FONT2)
	textobject.textLine(ST['Skills'])
	textobject.setFont(*FONT3)
	textobject.moveCursor(0, -5)
	for n in cv_data['skills']:
		textobject.moveCursor(0, 5)
		textobject.textLine('- ' + n)
	c.drawText(textobject)
	
	textobject = c.beginText()
	textobject.setTextOrigin(LEFT_BAR_MARGIN/2, 50)
	textobject.setFont(*FONT3)
	textobject.setFillColorRGB(*WHITE)
	textobject.textLine(ST['PDF created using reportlab library'])
	textobject.textLine(ST['Script cv_maker.py availabe at:'])
	textobject.textLine('https://github.com/Arenhart/Other')
	now = date.today()
	now_str = now.strftime("%d / %m / %Y")
	textobject.textLine(now_str)
	c.drawText(textobject)
	
	c.restoreState()
		
def laterPages(c, doc):
	c.saveState()
	c.setFillColorRGB(*COLOR2)
	c.setStrokeColorRGB(*COLOR2)
	c.rect(0, 0 ,LEFT_BAR, HEIGHT, stroke = 1, fill = 1)
	c.restoreState()
	

parsedCV = []
entry = '<font size=18>' + cv_data['header']['title'] + '</font><br/>'
parsedCV.append(entry)
entry = '<font size=10>' + cv_data['header']['introduction'] + '</font><br/>'
parsedCV.append(entry)

parsedCV.append(f'<br/><br/><font size = 16>{ST["Education"]}</font><br/>' )
cv_data['education'].sort(key = lambda x : int(x['year start']), reverse = True)
for n in cv_data['education']:
	entry = n['year start'] + ' - ' + n['year end'] + ':   ' + n['degree'] + ', ' + n['institution'] + '<br/><font size = 8>' + n['conclusion work'] + '</font><br/>'
	parsedCV.append( entry )
	
parsedCV.append( f'<font size = 16>{ST["Work experience"]}</font><br/>' )
cv_data['work experience'].sort(key = lambda x : int(x['year start']), reverse = True)
for n in cv_data['work experience']:
	entry = n['year start'] + ' - ' + n['year end'] + '   ' + n['role'] + ',  ' + n['location'] + '<br/><font size = 7>' + n['description'] + '</font><br/>'
	parsedCV.append( entry )
	
parsedCV.append( f'<font size = 16>{ST["Research projects"]}</font><br/>' )
cv_data['research projects'].sort(key = lambda x : int(x['year']), reverse = True)
for n in cv_data['research projects']:
	entry = n['year'] + '   ' + n['title'] + '<br/><font size = 7>' + n['description'] + '</font><br/>'
	parsedCV.append( entry )
	
parsedCV.append(f'<font size = 16>{ST["Patents and publications"]}</font><br/>' )
cv_data['publications'].sort(key = lambda x : int(x['year']), reverse = True)
for n in cv_data['publications']:
	entry = n['year'] + '   ' + n['title'] + '<br/>'
	parsedCV.append( entry )
	
parsedCV.append( f'<font size = 16>{ST["Other achievements"]}</font><br/>' )
categories = list(set(i['category'] for i in cv_data['other achievements']))
for cat in categories:
	subset = [i for i in cv_data['other achievements'] if i['category'] == cat]
	subset.sort(key = lambda x : int(x['year']), reverse = True)
	if cat != ST['Other']:
		parsedCV.append(f'<u>{cat}</u><br/>' )
	for n in subset:
		entry = '<font size = 10>' + n['year'] + '   ' + n['title'] + '</font><br/>'
		parsedCV.append( entry )

def go():
	doc = SimpleDocTemplate(f'cv_{LANGUAGE}.pdf')
	doc.leftMargin = LEFT_BAR + LEFT_BAR_MARGIN
	doc.rightMargin = 20
	doc.topMargin = 0.5 * cm
	Story = []
	style = styles['Normal']
	style.__dict__['justifyBreaks'] = 0
	style.__dict__['autoLeading'] = 'max'
	style.__dict__['alignment'] = 4
	style.__dict__['spaceAfter'] = 6
	style.refresh()
	for entry in parsedCV:
		p = Paragraph(entry, style)
		Story.append(p)
		#Story.append(Spacer(1,2*cm))
	doc.build(Story, onFirstPage=firstPage, onLaterPages=laterPages)
	
go()


'''
c.showPage()
c.save()
'''