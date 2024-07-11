from django.db import models

class ShotTypeChoices(models.TextChoices):
        SCREENSHOT = "s" , "Screenshot"
        WEB_CAM = "w" , "Web Cam"

class CurrencyChoices(models.TextChoices):
        USD = "US", "USD"
        PKR = "PK", "PKR"
        EUR = "EU", "EUR"
        GBP = "GB", "GBP"
        JPY = "JP", "JPY"
        CAD = "CA", "CAD"
        AUD = "AU", "AUD"
        INR = "IN", "INR"
        CNY = "CN", "CNY"
        SGD = "SG", "SGD"
        CHF = "CH", "CHF"
        NZD = "NZ", "NZD"
        RUB = "RU", "RUB"
        BRL = "BR", "BRL"
        ZAR = "ZA", "ZAR"


class ScreenshotInterval(models.TextChoices):
        FIVE_MINUTES = "F" , "Five Minutes"
        TEN_MINUTES = "T" , "Ten Minutes"
        THIRTY_MINUTES = "TH", "Thirty Minutes"
        SIXTY_MINUTES = "S" , "Sixty Minutes"

class RoleChoices(models.TextChoices):
       ADMIN =  "A", "Admin"
       SUPERVISOR = "S", "Supervisor"
       WORKER = "W", "Worker"

class ActivityType(models.TextChoices):
        DESKTOP = "D" , "Desktop"
        MANUAL = "M" , "Manual"
        WEB = "W" , "Web"
        Mobile = "B" , "Mobile"

class TimeZoneChoices(models.TextChoices):
    UTC_MINUS_12 = "UTC-12", "(-12:00) Etc/GMT-12"
    UTC_MINUS_11 = "UTC-11", "(-11:00) Pacific/Midway"
    UTC_MINUS_10 = "UTC-10", "(-10:00) Pacific/Honolulu"
    UTC_MINUS_9 = "UTC-9", "(-09:00) America/Anchorage"
    UTC_MINUS_8 = "UTC-8", "(-08:00) America/Los_Angeles"
    UTC_MINUS_7 = "UTC-7", "(-07:00) America/Denver"
    UTC_MINUS_6 = "UTC-6", "(-06:00) America/Chicago"
    UTC_MINUS_5 = "UTC-5", "(-05:00) America/New_York"
    UTC_MINUS_4 = "UTC-4", "(-04:00) America/Santiago"
    UTC_MINUS_3 = "UTC-3", "(-03:00) America/Sao_Paulo"
    UTC_MINUS_2 = "UTC-2", "(-02:00) Etc/GMT-2"
    UTC_MINUS_1 = "UTC-1", "(-01:00) Atlantic/Azores"
    UTC_PLUS_0 = "UTC+0", "(+00:00) Europe/London"
    UTC_PLUS_1 = "UTC+1", "(+01:00) Europe/Paris"
    UTC_PLUS_2 = "UTC+2", "(+02:00) Europe/Athens"
    UTC_PLUS_3 = "UTC+3", "(+03:00) Europe/Moscow"
    UTC_PLUS_4 = "UTC+4", "(+04:00) Asia/Dubai"
    UTC_PLUS_5 = "UTC+5", "(+05:00) Asia/Karachi"
    UTC_PLUS_6 = "UTC+6", "(+06:00) Asia/Dhaka"
    UTC_PLUS_7 = "UTC+7", "(+07:00) Asia/Bangkok"
    UTC_PLUS_8 = "UTC+8", "(+08:00) Asia/Singapore"
    UTC_PLUS_9 = "UTC+9", "(+09:00) Asia/Tokyo"
    UTC_PLUS_10 = "UTC+10", "(+10:00) Australia/Sydney"
    UTC_PLUS_11 = "UTC+11", "(+11:00) Pacific/Noumea"
    UTC_PLUS_12 = "UTC+12", "(+12:00) Pacific/Auckland"
    UTC_PLUS_13 = "UTC+13", "(+13:00) Pacific/Fakaofo"
#     UTC_PLUS_13_1 = "UTC+13:1", "(+13:00) Pacific/Apia"
    UTC_PLUS_14 = "UTC+14", "(+14:00) Pacific/Kiritimati"

