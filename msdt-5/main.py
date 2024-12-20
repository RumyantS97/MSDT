import math


def kilometers_to_miles(km):
    return km * 0.621371


def miles_to_kilometers(miles):
    return miles / 0.621371


def kilograms_to_pounds(kg):
    return kg * 2.20462


def pounds_to_kilograms(pounds):
    return pounds / 2.20462


def liters_to_gallons(liters):
    return liters * 0.264172


def gallons_to_liters(gallons):
    return gallons / 0.264172


def celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9


def meters_to_feet(meters):
    return meters * 3.28084


def feet_to_meters(feet):
    return feet / 3.28084


class UnitConverter:
    def __init__(self):
        self.supported_countries = {
            "Russia": "metric",
            "USA": "imperial",
            "UK": "hybrid",
        }
        self.conversion_methods = {
            "metric": {
                "Kilometers to Miles": kilometers_to_miles,
                "Kilograms to Pounds": kilograms_to_pounds,
                "Liters to Gallons": liters_to_gallons,
                "Celsius to Fahrenheit": celsius_to_fahrenheit,
                "Meters to Feet": meters_to_feet,
            },
            "imperial": {
                "Miles to Kilometers": miles_to_kilometers,
                "Pounds to Kilograms": pounds_to_kilograms,
                "Gallons to Liters": gallons_to_liters,
                "Fahrenheit to Celsius": fahrenheit_to_celsius,
                "Feet to Meters": feet_to_meters,
            },
            "hybrid": {
                "Kilometers to Miles": kilometers_to_miles,
                "Miles to Kilometers": miles_to_kilometers,
                "Kilograms to Pounds": kilograms_to_pounds,
                "Pounds to Kilograms": pounds_to_kilograms,
            },
        }

    def select_country(self):
        print("Available countries: ", ", ".join(
            self.supported_countries.keys()))
        while True:
            country = input("Select a country: ").strip()
            if country in self.supported_countries:
                return country
            print("Unsupported country. Please try again.")

    def get_conversion_type(self, system):
        methods = self.conversion_methods[system]
        print("Available conversions:")
        for idx, conversion in enumerate(methods.keys(), start=1):
            print(f"{idx}. {conversion}")

        while True:
            try:
                choice = int(input("Select a conversion type by number: "))
                if 1 <= choice <= len(methods):
                    conversion_name = list(methods.keys())[choice - 1]
                    return conversion_name, methods[conversion_name]
            except ValueError:
                print("Invalid input. Please enter a number.")

    def convert(self):
        print("Welcome to the Unit Converter!")
        country = self.select_country()
        system = self.supported_countries[country]
        print(f"Selected country: {country} ({system} system)")

        conversion_name, conversion_function = self.get_conversion_type(system)
        while True:
            try:
                value = float(
                    input(f"Enter the value to convert ({conversion_name}): "))
                result = conversion_function(value)
                print(f"Result: {result}")
                break
            except ValueError:
                print("Invalid value. Please enter a numeric value.")


if __name__ == "__main__":
    converter = UnitConverter()
    converter.convert()
