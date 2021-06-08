import csv

from requests_html import HTML, HTMLSession
url = "https://www.autotoja.lt/toyota/naudoti-automobiliai/"

# TODO make cvs save a new file each time for comparison
date= '3' # TODO make it dynamic
csvFileName = "web_scrape"+date

csv_file = open(csvFileName+'.csv', 'w', encoding="utf-8")
csv_writer= csv.writer(csv_file)
csv_writer.writerow(['name', 'year', 'mileage', 'transmissin', 'fuel', 'link', 'warranty', 'price'])


session = HTMLSession()
r = session.get(url)

cars = r.html.find('.single-car-in')

# carText = r.html.find('.single-car-in ', first=True).text
for car in cars:

    carName = car.find('.car-name', first=True).text
    carYear = car.find('.car-info span:nth-child(2)', first=True).text
    carMileage = car.find('.car-info-line:nth-child(2) span:nth-child(2)', first=True).text
    carTransm = car.find('.car-info-line:nth-child(3) span:nth-child(2)', first=True).text
    carFuelType = car.find('.car-info-line:nth-child(5) span:nth-child(2)', first=True).text
    carLink = car.find('.car-name a', first=True).attrs['href']
    try:
        carVarranty = car.find('.car-info-line:nth-child(7) span:nth-child(2)', first=True).text
    except Exception as e:
        carVarranty = "NONE "
    
    carPrice = car.find('.car-price-in .value', first=True).text
    
    csv_writer.writerow([carName, carYear, carMileage, carTransm, carFuelType, carLink, carVarranty, carPrice])


    print('Pavadinimas: '+carName)
    print('Metai: ' + carYear)
    print('Rida: '+carMileage+'km')
    print('Kuro tipas: '+carFuelType)
    print('Pav. dež.: '+carTransm)
    print('Garantijos tipas: '+carVarranty)
    print('Kaina: '+carPrice)
    print(carLink)

csv_file.close()

print('Hello, beautifull')
# Phase 1: Scrape the website

# Phase 2: Save to csv file (car name, reg. year, mileage, auto or mech, fuel type, link to the details, varranty, PRICE)
# Phase 3: Compare the two last file between eachother
# Phase 4: if difference found, send the difference to the communication medium.
# Phase 5: config the comms
