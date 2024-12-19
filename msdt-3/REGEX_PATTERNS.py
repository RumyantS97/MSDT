REGEX_PATTERNS = {
    "telephone"           : r"^\+7-\(\d{3}\)-\d{3}(-\d{2}){2}$",
    "http_status_message" : r"^\d{3}\s.+",
    "snils"               : r"^\d{11}$",
    "identifier"          : r"^\d{2}-\d{2}/\d{2}$",
    "ip_v4"               : r"^\d{1,3}(\.\d{1,3}){3}$",
    "longitude"           : r"^-?(180|(\d{1,2}|1[0-7]\d)(\.\d{1,})?)$",
    "blood_type"          : r"^([ABO]|AB)[\−\+]$",
    "isbn"                : r"(^\d{3}-)?\d-\d{5}-\d{3}-\d$",
    "locale_code"         : r"^[A-Za-z]+(\-[A-Za-z]+)*$",
    "date"                : r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"
}
