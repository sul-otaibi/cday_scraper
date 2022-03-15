import requests
from bs4 import BeautifulSoup, NavigableString

s = requests.Session()
s.get(r'https://cday.kfupm.edu.sa/Home/English')
r = s.get(r'https://cday.kfupm.edu.sa/Home/Opportunities')
s.close()

# Parse the HTML of the page.
soup = BeautifulSoup(r.text, 'html.parser').body

# Get the names of the majors.
majors = soup.find('select', class_='required').find_all('optgroup', label='Associate Degree') 
majors += soup.find('select', class_='required').find_all('optgroup', label='BSc') 
majors += soup.find('select', class_='required').find_all('optgroup', label='MS') 
majors += soup.find('select', class_='required').find_all('optgroup', label='PhD')

# Split them into list.
# The first and last elements are empty, thus discarded.
majors_names = [f'{x.strip()}' for x in majors[0].text.split('\n')[1:-1]]
majors_names.extend([f'{x.strip()}' for x in majors[1].text.split('\n')[1:-1]])
majors_names.extend([f'MS {x.strip()}' for x in majors[2].text.split('\n')[1:-1]])
majors_names.extend([f'PhD {x.strip()}' for x in majors[3].text.split('\n')[1:-1]])

# Convert to dictionary: {Major: count}.
major_count = {}
for name in majors_names:
    major_count.update({name : 0})

# Get names of companies and location and majors wanted by that company.
comp_majors = {}
for i in soup.find('table').children:
    if type(i) is not NavigableString:
        l = i.text.replace('\t','').replace('\r','').replace('Apply','').replace('\n\n','')
        l = l.replace('[Show/Hide]','').replace('  ','').replace('\xa0','').strip().split('\n')
        comp_majors.update({l[0]:{'loc': l[1], 'majors': set(l[3:])}})
comp_majors.pop('Company')

# Count majors.
for element in comp_majors.items():
    for i in element[1]['majors']:
        major_count[i.strip()] = major_count[i.strip()] + 1
