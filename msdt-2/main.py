import os
import vobject
from datetime import date
from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()
v_card = os.getenv('VCF')

vcf_table = PrettyTable()
vcf_table.field_names = [
    'full_name',
    'birthday_and_years',
    'address',
    'number'
]

vcf_table.align = 'l'
vcf_table.sortby = 'full_name'
vcf_table.hrules = True

with open(v_card, encoding='utf-8') as phone_book:
    # allowQP to process quoted-printable data
    contacts = vobject.readComponents(phone_book, allowQP=True)
    for contact in contacts:
        # Name, patronymic and surname
        full_name = contact.fn.value

        # If a contact has a birthday, we display it in Russian format
        # Using the difference between the current date and the day of birth, we determine the age
        # For fun, we determine the zodiac sign
        # We handle the exception if this field does not exist
        try:
            birthday = date.fromisoformat(contact.bday.value)
            today = date.today()
            years = (today - birthday).days // 365

            zodiac_signs = {
                'Capricorn': (date(birthday.year, month=12, day=22), date(birthday.year, month=1, day=19)),
                'Aquarius': (date(birthday.year, month=1, day=20), date(birthday.year, month=2, day=18)),
                'Pisces': (date(birthday.year, month=2, day=19), date(birthday.year, month=3, day=20)),
                'Aries': (date(birthday.year, month=3, day=21), date(birthday.year, month=4, day=19)),
                'Taurus': (date(birthday.year, month=4, day=20), date(birthday.year, month=5, day=20)),
                'Gemini': (date(birthday.year, month=5, day=21), date(birthday.year, month=6, day=20)),
                'Cancer': (date(birthday.year, month=6, day=21), date(birthday.year, month=7, day=22)),
                'Leo': (date(birthday.year, month=7, day=23), date(birthday.year, month=8, day=22)),
                'Virgo': (date(birthday.year, month=8, day=23), date(birthday.year, month=9, day=22)),
                'Libra': (date(birthday.year, month=9, day=23), date(birthday.year, month=10, day=22)),
                'Scorpio': (date(birthday.year, month=10, day=23), date(birthday.year, month=11, day=21)),
                'Sagittarius': (date(birthday.year, month=11, day=22), date(birthday.year, month=12, day=21))
            }

            for sign, (start_date, end_date) in zodiac_signs.items():
                if start_date <= birthday <= end_date:
                    birthday_and_years = f'Birthday: {birthday.strftime("%d.%m.%Y")}\nZodiac signs: {sign}\nAge: {years}'

        except AttributeError:
            birthday_and_years = ''

        # There may be several phone numbers, we display them all
        number = []
        for phone_number in contact.tel_list:
            number.append(phone_number.value)
        number = '\n'.join(number)

        # If there is a comma in the address (for example: Lenin 1, apt. 2) - it is considered a list
        # If there are no commas - a line
        # We handle the exception if the field does not exist
        address = []
        try:
            for adds in contact.adr_list:
                street = adds.value.street
                if isinstance(street, str):
                    address.append(street)
                else:
                    address.append(''.join(street))
            address = '\n'.join(address)
        except AttributeError:
            address = ''

        # Filling in the table
        vcf_table.add_row(
            [
                full_name,
                birthday_and_years,
                address,
                number,
            ]
        )

# Table header indicating the number of records
vcf_table.title = f'rowcount: {vcf_table.__getattr__("rowcount")}'

# Write to file with current date
with open(f'{v_card}_{today}.txt', 'w') as report:
    report.write(vcf_table.get_string())