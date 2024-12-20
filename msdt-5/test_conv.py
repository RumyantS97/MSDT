import math

import pytest
from unittest.mock import patch, MagicMock

from main import (
    kilometers_to_miles,
    miles_to_kilometers,
    kilograms_to_pounds,
    pounds_to_kilograms,
    liters_to_gallons,
    gallons_to_liters,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    meters_to_feet,
    feet_to_meters,
    UnitConverter
)


@pytest.mark.parametrize("km, expected", [(1, 0.621371), (5, 3.106855), (10, 6.21371)])
def test_kilometers_to_miles(km, expected):
    assert math.isclose(kilometers_to_miles(km), expected, rel_tol=1e-5)


@pytest.mark.parametrize("miles, expected", [(1, 1.609344), (3, 4.828032), (5, 8.04672)])
def test_miles_to_kilometers(miles, expected):
    assert math.isclose(miles_to_kilometers(miles), expected, rel_tol=1e-5)


@pytest.mark.parametrize("celsius, expected", [(-40, -40), (0, 32), (100, 212)])
def test_celsius_to_fahrenheit(celsius, expected):
    assert math.isclose(celsius_to_fahrenheit(celsius), expected, rel_tol=1e-5)


@pytest.mark.parametrize("fahrenheit, expected", [(32, 0), (212, 100), (-40, -40)])
def test_fahrenheit_to_celsius(fahrenheit, expected):
    assert math.isclose(fahrenheit_to_celsius(fahrenheit), expected, rel_tol=1e-5)


def test_select_country():
    converter = UnitConverter()
    with patch("builtins.input", side_effect=["USA"]):
        country = converter.select_country()
    assert country == "USA"


def test_get_conversion_type():
    converter = UnitConverter()
    with patch("builtins.input", side_effect=["1"]):
        conversion_name, conversion_function = converter.get_conversion_type("metric")
    assert conversion_name == "Kilometers to Miles"
    assert conversion_function == kilometers_to_miles


def test_kilograms_to_pounds():
    assert math.isclose(kilograms_to_pounds(1), 2.20462, rel_tol=1e-5)
    assert math.isclose(kilograms_to_pounds(50), 110.231, rel_tol=1e-5)


def test_pounds_to_kilograms():
    assert math.isclose(pounds_to_kilograms(1), 0.453592, rel_tol=1e-5)
    assert math.isclose(pounds_to_kilograms(100), 45.3592, rel_tol=1e-5)


@pytest.mark.parametrize("country, system", [
    ("Russia", "metric"),
    ("USA", "imperial"),
    ("UK", "hybrid"),
])
def test_supported_countries(country, system):
    converter = UnitConverter()
    assert converter.supported_countries[country] == system
