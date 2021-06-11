from requests_html import HTML, HTMLSession
import os
from email.message import EmailMessage
from email.header import Header
import csv

import smtplib




url = "https://www.autotoja.lt/toyota/naudoti-automobiliai/"

# TODO make cvs save a new file each time for comparison
date = '_new'  # TODO make it dynamic
csvFileName = "web_scrape"+date

csv_file = open(csvFileName+'.csv', 'w', encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name', 'year', 'mileage', 'transmissin', 'fuel', 'link', 'warranty', 'price'])


session = HTMLSession()
r = session.get(url)

cars = r.html.find('.single-car-in')

# carText = r.html.find('.single-car-in ', first=True).text
for car in cars:

    carName = car.find('.car-name', first=True).text
    carYear = car.find('.car-info span:nth-child(2)', first=True).text
    carMileage = car.find(
        '.car-info-line:nth-child(2) span:nth-child(2)', first=True).text
    carTransm = car.find(
        '.car-info-line:nth-child(3) span:nth-child(2)', first=True).text
    carFuelType = car.find(
        '.car-info-line:nth-child(5) span:nth-child(2)', first=True).text
    carLink = car.find('.car-name a', first=True).attrs['href']
    try:
        carVarranty = car.find(
            '.car-info-line:nth-child(7) span:nth-child(2)', first=True).text
    except Exception as e:
        carVarranty = "NONE "

    carPrice = car.find('.car-price-in .value', first=True).text

    csv_writer.writerow([carName, carYear, carMileage, carTransm,
                        carFuelType, carLink, carVarranty, carPrice])

    # print('Pavadinimas: '+carName)
    # print('Metai: ' + carYear)
    # print('Rida: '+carMileage+'km')
    # print('Kuro tipas: '+carFuelType)
    # print('Pav. dež.: '+carTransm)
    # print('Garantijos tipas: '+carVarranty)
    # print('Kaina: '+carPrice)
    # print(carLink)


csv_file.close()

ingoneFuel = "Dyzelinas"
ignoreTransmission = "Mechaninė"

with open('web_scrape_old.csv', 'r', encoding="utf-8") as t1, open('web_scrape_new.csv', 'r', encoding="utf-8") as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()


with open('update.csv', 'w', encoding="utf-8") as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)

with open('update.csv', 'r', encoding="utf-8") as file:
    data = list(csv.reader(file))
    for index, line in enumerate(data):
        #    print(line)
        if ignoreTransmission in line:
            data.pop(index)
            # print(data)
    for index, line in enumerate(data):
        #    print(line)
        if ingoneFuel in line:
            data.pop(index)
            # print(data)
messageList=""
# print(data)
car = ''
for line in data:
    car +="\n\nAutomobilis:" +line[0]
    car +="\nRegistracijos metai:" +line[1]
    car +="\nRida:"+line[2]
    car +="\nPavarų dėžė:"+line[3]
    car +="\nDegalų tipas:"+line[4]
    car +="\nGarantija:"+line[5]
    car +="\nKaina:"+line[6]

# print(car)
# ---------------------------------------------------------------------------------------------------------


EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASS = os.environ.get('EMAIL_PASS')


msg = EmailMessage()
msg['Subject'] = "A new used car(s) have been posted in Autotoja.lt"
msg['From'] = str(Header('Cookie Monster Bot <'+EMAIL_ADDRESS+'>'))
msg['To'] = EMAIL_ADDRESS
msg.set_content("Hello!\n\n A new Car(s) have been posted on Autotoja.lt\n\n Please take a look at this:"+car + "\n\n With love,\n Cookie Monster Bot <3")

# if update is not empty send email!

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
    smtp.send_message( msg)
# # send email

os.remove('update.csv')
# remove _old
# rename _new to _old


print('Hello, beautifull')
# Phase 1: Scrape the website DONE

# Phase 2: Save to csv file (car name, reg. year, mileage, auto or mech, fuel type, link to the details, varranty, PRICE) DONE
# Phase 3: Compare the two last file between eachother DONE
# Phase 4: if difference found, send the difference to the communication medium. DONE
# Phase 4.1: Ignore if the difference includes Mechanine or DyzelinasDONE
# Phase 4.5: delete the old file and save the new one as _old for further comparison

# Phase 5: config the comms
#Make this run semi periodically
#set it up on raspberry