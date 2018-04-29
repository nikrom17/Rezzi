# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    generate_pdf.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: enennige <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/04/28 12:47:28 by enennige          #+#    #+#              #
#    Updated: 2018/04/28 18:15:02 by enennige         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib import colors

#global vars
filename = "resume.pdf"
Story = []

doc = SimpleDocTemplate(filename,pagesize=letter,
                        rightMargin=30,leftMargin=30,
                        topMargin=30,bottomMargin=18)

#user input vars
full_name = "Adam Klein"
address_parts = ["510-396-3127", "adamk@gmail.com"]
job_skills = ["operating conveyor", "operating forklift", "pallet jack maneuvering", "site cleanup", "docking and unloading trucks"]
availability = "Weekdays after 9am"
languages = ["German", "English"]

class Job(object):
    def __init__(self, start_date, end_date, company_name, job_title, duties):
        self.start_date = start_date
        self.end_date = end_date
        self.company_name = company_name
        self.job_title = job_title
        self.duties = duties

jobs = [Job("Jan 2016", "March 2018", "Expresspoint Packaging", "Warehouse Associate",
            ["Put away all inbound products upon recieving them and transferred inventory between internal warehouse locations",
            "Loading and unloading trucks using forklift and pallet jacks",
            "Operating conveyors, carts and other equipment as well as general maintenance and cleanup of machinery"]),
        Job("Jan 2014", "Dec 2015", "LSG Shy Chefs", "Assembly Line Worker",
            ["Sort, wrap and pack airline goods as well as equipment into carts acoording to airline specifications",
            "Moniter overall quality of the product by performing periodic product inspections"]),
        Job("Jan 2010", "Dec 2013", "Manpower", "Manufacturing Assembler",
            ["Assembled various devices according to specifications including screwing, hammering, nailing and painting",
            "Provide safety training to other employees including machine and tool operation procedures"])]

class Education(object):
    def __init__(self, school_name, degree):
        self.school_name = school_name
        self.degree = degree

education = [Education("Fuhsd Fremont", "GED diploma"),
            Education("Red Cross Safety Training", "CPR and First Aid Certification")]

#styling
pdfmetrics.registerFont(TTFont('Nunito-Bold', 'resume_fonts/Nunito/Nunito-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Light', 'resume_fonts/Roboto/Roboto-Light.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Regular', 'resume_fonts/Roboto/Roboto-Regular.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=30))
title_size = 30
header_size = 18
subtext_size = 10
paragraph_size = 13
paragraph_color = '#4A4A4A'
subtext_color = '#9B9B9B'
name_color = "#3e7ce3"
paragraph_font = 'Roboto-Light'
subtitle_font = 'Roboto-Regular'
header_font = 'Nunito-Bold'
spacing_multiplier = 1.3

def put_content_line(content, size, font=paragraph_font, color=paragraph_color):
    ptext = '<font size=%d name="%s" color="%s">%s</font>' % (size, font, color, content)
    Story.append(Paragraph(ptext, styles["Normal"]))

#Resume Name
def put_name():
    put_content_line(full_name, title_size, header_font, name_color)
    Story.append(Spacer(1, title_size * spacing_multiplier))

# Write section header
def put_header(section_title):
    put_content_line(section_title, header_size, header_font)
    Story.append(Spacer(1, header_size))


# Write section paragraph
def put_paragraph(content):
    put_content_line(content, paragraph_size)
    Story.append(Spacer(1, paragraph_size * spacing_multiplier))

# Contact Information
def put_contact(address):
    for part in address:
        put_content_line(part.strip(), paragraph_size)
        Story.append(Spacer(1, paragraph_size / 3))
    Story.append(Spacer(1, paragraph_size * spacing_multiplier))

#Experience
def put_experience(jobs):
    put_header("Experience")
    for job in jobs:
        put_content_line(job.job_title + " at " + job.company_name,
        paragraph_size, font=subtitle_font)
        Story.append(Spacer(1, paragraph_size / 2))
        put_content_line(job.start_date + " - " + job.end_date,
        subtext_size, color=subtext_color)
        Story.append(Spacer(1, subtext_size / 2))
        for duty in job.duties:
            put_content_line("• " + duty, paragraph_size)
            Story.append(Spacer(1, paragraph_size / 2))
        Story.append(Spacer(1, paragraph_size * spacing_multiplier))

#Experience
def put_education(education):
    put_header("Education & Training")
    for course in education:
        put_content_line(course.degree,
        paragraph_size, font=subtitle_font)
        Story.append(Spacer(1, paragraph_size / 3))
        put_paragraph(course.school_name)
    Story.append(Spacer(1, paragraph_size * spacing_multiplier))

# Put a list
def put_list(title, job_skills):
    put_header(title)
    job_string = ', '.join(job_skills)
    put_paragraph(job_string)

# Put a list
def put_languages(languages):
    put_header("Languages")
    l_string = ', '.join(languages)
    put_content_line(l_string, paragraph_size)

# Availability
def put_availability(availability):
    put_header("Availability")
    put_paragraph(availability)


if __name__ == "__main__":
    put_name()
    put_contact(address_parts)
    put_list("Skills", job_skills)
    put_experience(jobs)
    put_education(education)
    put_languages(languages)
    #put_availability(availability)
    doc.build(Story)
