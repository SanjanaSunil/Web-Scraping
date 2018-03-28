from requests import get 
from bs4 import BeautifulSoup
import csv

names = []
urls = []
authors = []
price = []
ratingsno = []
avgratings = []

pages = [str(i) for i in range(1, 6)]

requests = 0

for page in pages:

    response = get('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_' + page + '?ie=UTF8&pg=' + page)

    requests += 1
    if requests > 5:
        break

    page_html = BeautifulSoup(response.text, 'html.parser')
    mv_containers = page_html.find_all('div', class_ = 'zg_itemImmersion')

    for container in mv_containers:

        if container.find('img'):
            name = container.find('img')['alt']
            names.append(name)
        elif container.find('div', class_ = 'p13n-sc-truncate p13n-sc-line-clamp-1'):
            name = container.find('div', class_ = 'p13n-sc-truncate p13n-sc-line-clamp-1').text.strip()
            names.append(name)
        else:
            names.append('Not avaliable')

        #-------------------------------------------------------------

        if container.find('div', class_ = 'a-row a-size-small'):
            author = container.find('div', class_ = 'a-row a-size-small').text.strip()
            authors.append(author)
        else:
            authors.append('Not available')

        #-------------------------------------------------------------

        
        if container.find('span', class_ = 'p13n-sc-price'):
            pricing = container.find('span', class_ = 'p13n-sc-price').text.strip()
            price.append('Rs. ' + pricing)
        else:
            price.append('Not available')

        #-------------------------------------------------------------

        if container.find('span', class_ = 'a-icon-alt'):
            stars = container.find('span', class_ = 'a-icon-alt').text
            if 'out of' in stars and 'stars' in stars:
                stars = container.find('span', class_ = 'a-icon-alt').text
            else:
                stars = 'Not available'
        avgratings.append(stars)

        #-------------------------------------------------------------

        if container.find('a', class_ = 'a-link-normal'):
            booklink = 'https://www.amazon.com' + container.find('a', class_ = 'a-link-normal')['href']
        else:
            booklink = 'Not available'
        urls.append(booklink)

        #-------------------------------------------------------------

        if container.find('a', class_ = 'a-size-small a-link-normal'):
            number = container.find('a', class_ = 'a-size-small a-link-normal').text
            ratingsno.append(number)
        else:
            ratingsno.append('Not available')

#-------------------------------------------------------------

with open('output/in_book.csv', 'w') as the_file:
    the_file.write('Name' + ';' + 'URL' + ';' + 'Author' + ';' + 'Price' + ';' + 'Number of ratings' + ';' + 'Average rating');
    the_file.write("\n")
    for i in range(0, 100):
        the_file.write(str(names[i]) + ';' + str(urls[i]) + ';' + str(authors[i]) + ';' + str(price[i]) + ';' + str(ratingsno[i]) + ';' + str(avgratings[i]))
        the_file.write("\n")

print("Successful completion of web scraping")
