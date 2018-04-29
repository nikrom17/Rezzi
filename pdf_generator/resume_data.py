import re
import datetime

def extract_string(field):
    return re.findall('"([^"]*)"', data[field])

def convert_date(test_date):
    months = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    year, month, day = test_date.split('-')
    ret = str(months[int(month)]) + " " + str(year)
    return (ret)

def data_to_resume():
    full_name = data['given-name'] + " " + data['last-name']
    languages = extract_string('language')
    date = extract_string('date-period')
    endDate = convert_date(date[1][:10])
    startDate = convert_date(date[3][:10])
    job_title = extract_string('jobs')
    duties = data['any']
    print (startDate, endDate, job_title[0], duties, full_name, languages)

data = {'given-name': 'Jacob',
        'last-name': 'Fuller',
        'language': 'values { string_value: "English"} values {string_value: "Spanish"}',
        'jobs': 'values { string_value: "cook"}',
        'any': 'made a lot of food',
        'date-period':
        'fields { key: "endDate" \
        value {string_value: "2016-02-29T12:00:00-08:00"}} \
        fields {key: "startDate" \
        value {string_value: "2014-01-01T12:00:00-08:00"}}'
        }

data_to_resume()