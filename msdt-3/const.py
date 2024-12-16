VARIANT = 27
CSV_FILE = "msdt-3/27.csv"
RESULT = "msdt-3/result.json"
PATTERNS = {
    "email"      : "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$",
    "height"     : "^[0-2]\\.\\d{2}$",
    "snils"      : "^\\d{11}$",
    "passport"   : "^\\d{2}\\s\\d{2}\\s\\d{6}$",
    "occupation" : "[a-zA-Zа-яА-ЯёЁ -]+",
    "longitude"  : "^-?(180(\\.0+)?|1[0-7]\\d(\\.\\d+)?|[1-9]?\\d(\\.\\d+)?)$",
    "hex_color"  : "^#[A-Fa-f0-9]{6}$",
    "issn"       : "^\\d{4}\\-\\d{4}$",
    "locale_code": "^[a-zA-Z]+(-[a-zA-Z]+)*$",
    "time"       : "^([01]\\d|2[0-3]):([0-5]\\d):([0-5]\\d)\\.\\d{6}$"
}
