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

with open('cv.json', 'r') as file:
    cv_data = json.load(file)
	
#c = canvas.Canvas("cv.pdf", pagesize = A4)

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
	textobject.textLine('Personal Info')
	for n in ('phone', 'email', 'skype', 'linkedin', 'github'):
		textobject.moveCursor(0, 10)
		n_cap = n[0].upper() + n[1:]
		textobject.setFont(*FONT3i)
		textobject.textLine(n_cap)
		textobject.setFont(*FONT3)
		textobject.textLine(info[n])
	textobject.moveCursor(0, 20)
	textobject.setFont(*FONT2)
	textobject.textLine('Skills')
	textobject.setFont(*FONT3)
	textobject.moveCursor(0, -5)
	for n in cv_data['skills']:
		textobject.moveCursor(0, 5)
		textobject.textLine('- ' + n)
	c.drawText(textobject)
	
	textobject = c.beginText()
	textobject.setTextOrigin(LEFT_BAR_MARGIN, 50)
	textobject.setFont(*FONT3)
	textobject.setFillColorRGB(*WHITE)
	textobject.textLine('PDF created using reportlab library')
	textobject.textLine('Script cv_maker.py availabe at:')
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
entry = '<br/><br/><font size=18>' + cv_data['header']['title'] + '</font><br/>'
parsedCV.append(entry)
entry = '<font size=10>' + cv_data['header']['introduction'] + '</font><br/>'
parsedCV.append(entry)

parsedCV.append( '<br/><br/><font size = 16>Education</font><br/>' )
cv_data['education'].sort(key = lambda x : int(x['year start']), reverse = True)
for n in cv_data['education']:
	entry = n['year start'] + ' - ' + n['year end'] + ':   ' + n['degree'] + ' ' + n['institution'] + '<br/><font size = 8>' + n['conclusion work'] + '</font><br/>'
	parsedCV.append( entry )
	
parsedCV.append( '<font size = 16>Work experience</font><br/>' )
cv_data['work experience'].sort(key = lambda x : int(x['year start']), reverse = True)
for n in cv_data['work experience']:
	entry = n['year start'] + ' - ' + n['year end'] + '   ' + n['role'] + ' at  ' + n['location'] + '<br/><font size = 8>' + n['role'] + '</font><br/>'
	parsedCV.append( entry )
	
parsedCV.append( '<font size = 16>Research projects</font><br/>' )
cv_data['research projects'].sort(key = lambda x : int(x['year']), reverse = True)
for n in cv_data['research projects']:
	entry = n['year'] + '   ' + n['title'] + '<br/><font size = 8>' + n['description'] + '</font><br/>'
	parsedCV.append( entry )
	
parsedCV.append( '<font size = 16>Patents and publications</font><br/>' )
cv_data['publications'].sort(key = lambda x : int(x['year']), reverse = True)
for n in cv_data['publications']:
	entry = n['year'] + '   ' + n['title'] + '<br/>'
	parsedCV.append( entry )
	
parsedCV.append( '<font size = 16>Other achievements</font><br/>' )
categories = list(set(i['category'] for i in cv_data['other achievements']))
for cat in categories:
	subset = [i for i in cv_data['other achievements'] if i['category'] == cat]
	subset.sort(key = lambda x : int(x['year']), reverse = True)
	parsedCV.append(cat + '<br/>' )
	for n in subset:
		entry = n['year'] + '   ' + n['title'] + '<br/>'
		parsedCV.append( entry )

def go():
	doc = SimpleDocTemplate('cv.pdf')
	doc.leftMargin = LEFT_BAR + LEFT_BAR_MARGIN
	doc.rightMargin = 20
	doc.topMargin = 0
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