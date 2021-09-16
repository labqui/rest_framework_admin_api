from enum import Enum


class DateTimeType(Enum):
    DATE_TIME = "date_time"
    DATE = "date"
    TIME = "time"


class TypeFieldReact(Enum):
    HIDDEN = "hidden"
    FOREIGN_KEY = "picker"
    MANY_TO_MANY = "picker"
    SELECT = "select"
    DATE_TIME = "date_time"
    TEXT_INPUT = "text_input"
    FILE = "file"
    SWITCH = "switch"
    IMAGE = "image_field"
    FILE_FIELD = "file"


class KeyboardType(Enum):
    DEFAULT = "default"
    NUMERIC = "numeric"
    EMAIL_ADDRESS = "email-address"
    ASCII_CAPABLE = "ascii-capable"
    NUMBERS_AND_PUNCTUATION = "numbers-and-punctuation"
    url = "url"
    NUMBER_PAD = "number-pad"
    PHONE_PAD = "phone-pad"
    NAME_PHONE_PAD = "name-phone-pad"
    DECIMAL_PAD = "decimal-pad"
    TWITTER = "twitter"
    WEB_SEARCH = "web-search"
    VISIBLE_PASSWORD = "visible-password"
