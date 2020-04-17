from slugify import slugify
from django.db import migrations


def populate_vehicles(apps, schema_editor):
    makers_raw = '''AC
AMC
Acura
Alfa Romeo
Alpina
Aston Martin
Audi
BMW
BYD
Bajaj
Bentley
Borgward
Brilliance
Buick
Cadillac
Changan
Chery
Chevrolet
Chrysler
Citroen
DKW
DS
DW Hower
Dacia
Daewoo
Daihatsu
Daimler
Dallara
Datsun
De Tomaso
Delage
Derways
Dodge
DongFeng
Doninvest
Eagle
Excalibur
FAW
Ferrari
Fiat
Ford
Foton
GAC
GMC
Geely
Genesis
Great Wall
Hafei
Haima
Haval
Hawtai
Heinkel
Honda
Hummer
Hyundai
Infiniti
Iran Khodro
Isuzu
JAC
JMC
Jaguar
Jeep
Kia
LADA (ВАЗ)
Lamborghini
Lancia
Land Rover
Lexus
Lifan
Lincoln
Luxgen
MG
MINI
Mahindra
Maserati
Maybach
Mazda
McLaren
Mercedes-Benz
Mercury
Metrocab
Mitsubishi
Mitsuoka
Nissan
Oldsmobile
Opel
PUCH
Packard
Peugeot
Plymouth
Pontiac
Porsche
Proton
Ravon
Renault
Rolls-Royce
Rover
SEAT
Saab
Saleen
Saturn
Scion
Shanghai Maple
Skoda
Smart
SsangYong
Steyr
Subaru
Suzuki
Tatra
Tesla
Tianye
Toyota
Triumph
Volkswagen
Volvo
Vortex
Willys
Xin Kai
ZX
Zotye
ГАЗ
ЗАЗ
ЗИЛ
ЗиС
ИЖ
Комбат
ЛуАЗ
Москвич
СМЗ
ТагАЗ
УАЗ'''

    Maker = apps.get_model('vehicles', 'Maker')

    makers = [
        Maker(title=title, slug=slugify(title))
        for title in makers_raw.split('\n')
    ]

    Maker.objects.bulk_create(makers)


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_vehicles),
    ]
