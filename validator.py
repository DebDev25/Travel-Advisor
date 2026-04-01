from ISO_Codes import country_to_iso
import re


def valid_country(country: str) -> str:
    country = country.strip().title()
    if not re.fullmatch(r"[A-Za-z\s\-]+", country):
        raise ValueError("Country name contains invalid characters")
    if country not in country_to_iso:
        raise ValueError("Country not supported")
    return country_to_iso[country]
