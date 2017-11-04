'''
Astronomical algorithms
from the book "Astronomical Algorithms" by Jean Meeus, 1998
'''

import math
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ",
       "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tí", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ",
       "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CHI_MONTH = ["", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi",
             "Thân", "Dậu", "Tuất", "Hợi", "Tí", "Sửu"]


def julian_day_from_date(dd, mm, yy):
    '''
    ' Compute the (integral) Julian day number of day dd/mm/yyyy,
    ' i.e., the number
    ' of days between 1/1/4713 BC (Julian calendar) and dd/mm/yyyy.
    ' Formula from http://www.tondering.dk/claus/calendar.html
    params: dd - day
            mm - month
            yy - year
    rtype: int
    '''
    temp_a = int((14 - mm) / 12.)
    temp_year = yy + 4800 - temp_a
    temp_month = mm + 12 * temp_a - 3
    julian_day = (dd + int((153*temp_month + 2) / 5.) +
                  365 * temp_year + int(temp_year / 4.) -
                  int(temp_year/100.) + int(temp_year/400)
                  - 32045)
    if julian_day < 2299161:
        julian_day = dd + int((153*temp_month + 2)/5.) \
            + 365*temp_year + int(temp_year/4.) - 32083
    return julian_day


def julian_day_to_date(julian_day):
    '''
    Convert a Julian day number to day/month/year. Parameter jd is an integer
    '''
    if julian_day > 2299160:
        # After 5/10/1582, Gregorian calendar
        temp_a = julian_day + 32044
        temp_b = int((4 * temp_a + 3) / 146097.)
        temp_c = temp_a - int((temp_b * 146097) / 4.)
    else:
        temp_b = 0
        temp_c = julian_day + 32082
    temp_d = int((4 * temp_c + 3) / 1461.)
    temp_e = temp_c - int((1461 * temp_d) / 4.)
    temp_m = int((5 * temp_e + 2) / 153.)
    _day = temp_e - int((153 * temp_m + 2) / 5.) + 1
    _month = temp_m + 3 - 12 * int(temp_m / 10.)
    _year = temp_b * 100 + temp_d - 4800 + int(temp_m / 10.)
    return [_day, _month, _year]


def new_moon(k_th):
    '''
    ' Compute the time of the k-th new moon after the new moon
    ' of 1/1/1900 13:52 UCT
    ' (measured as the number of days since 1/1/4713 BC noon UCT,
    ' e.g., 2451545.125 is 1/1/2000 15:00 UTC).
    ' Returns a floating number, e.g.,
    ' 2415079.9758617813 for k_th=2 or 2414961.935157746 for k_th=-2
    '''
    # Time in Julian centuries from 1900 January 0.5
    time_julian = k_th / 1236.85
    time_julian_2 = time_julian * time_julian
    time_julian_3 = time_julian_2 * time_julian
    degree_to_radian = math.pi / 180
    julian_day_1 = (2415020.75933 + 29.53058868 * k_th +
                    0.0001178 * time_julian_2 -
                    0.000000155 * time_julian_3)
    julian_day_1 = (julian_day_1 +
                    0.00033*math.sin((166.56 + 132.87*time_julian -
                                      0.009173 * time_julian_2) *
                                     degree_to_radian))
    # Mean new moon
    mean_new_moon = (359.2242 + 29.10535608*k_th -
                     0.0000333*time_julian_2 - 0.00000347*time_julian_3)
    # Sun's mean anomaly
    sun_mean_anomaly = (306.0253 + 385.81691806*k_th +
                        0.0107306*time_julian_2 + 0.00001236*time_julian_3)
    # Moon's mean anomaly
    moon_mean_anomaly = (21.2964 + 390.67050646*k_th -
                         0.0016528*time_julian_2 - 0.00000239*time_julian_3)
    # Moon's argument of latitude
    moon_arg_lat = ((0.1734 - 0.000393*time_julian) *
                    math.sin(mean_new_moon*degree_to_radian) +
                    0.0021*math.sin(2*degree_to_radian*mean_new_moon))
    moon_arg_lat = (moon_arg_lat -
                    0.4068*math.sin(sun_mean_anomaly*degree_to_radian)
                    + 0.0161*math.sin(degree_to_radian*2*sun_mean_anomaly))
    moon_arg_lat = (moon_arg_lat -
                    0.0004*math.sin(degree_to_radian*3*sun_mean_anomaly))
    moon_arg_lat = (moon_arg_lat +
                    0.0104*math.sin(degree_to_radian*2*moon_mean_anomaly)
                    - 0.0051 * math.sin(degree_to_radian *
                                        (mean_new_moon + sun_mean_anomaly)))
    moon_arg_lat = (moon_arg_lat -
                    0.0074*math.sin(degree_to_radian *
                                    (mean_new_moon - sun_mean_anomaly))
                    + 0.0004*math.sin(degree_to_radian *
                                      (2*moon_mean_anomaly + mean_new_moon)))
    moon_arg_lat = (moon_arg_lat - 0.0004*math.sin(degree_to_radian *
                                                   (2*moon_mean_anomaly -
                                                    mean_new_moon))
                    - 0.0006 * math.sin(degree_to_radian *
                                        (2*moon_mean_anomaly
                                         + sun_mean_anomaly)))
    moon_arg_lat = (moon_arg_lat + 0.0010*math.sin(degree_to_radian *
                                                   (2*moon_mean_anomaly -
                                                    sun_mean_anomaly))
                    + 0.0005*math.sin(degree_to_radian *
                                      (2*sun_mean_anomaly + mean_new_moon))
                    )
    if time_julian < -11:
        deltat = (0.001 + 0.000839*time_julian + 0.0002261*time_julian_2
                  - 0.00000845*time_julian_3 -
                  0.000000081*time_julian*time_julian_3)
    else:
        deltat = -0.000278 + 0.000265*time_julian + 0.000262*time_julian_2
    new_julian_day = julian_day_1 + moon_arg_lat - deltat
    return new_julian_day


def sun_longitude(jdn):
    '''
    ' Compute the longitude of the sun at any time.
    ' Parameter: floating number jdn, the number of days since 1/1/4713 BC noon
    '''
    time_in_julian = (jdn - 2451545.0) / 36525.
    # Time in Julian centuries
    # from 2000-01-01 12:00:00 GMT
    time_in_julian_2 = time_in_julian * time_in_julian
    degree_to_radian = math.pi / 180.  # degree to radian
    mean_time = (357.52910 + 35999.05030*time_in_julian
                 - 0.0001559*time_in_julian_2 -
                 0.00000048 * time_in_julian*time_in_julian_2)
    # mean anomaly, degree
    mean_degree = (280.46645 + 36000.76983*time_in_julian +
                   0.0003032*time_in_julian_2)
    # mean longitude, degree
    mean_long_degree = ((1.914600 - 0.004817*time_in_julian -
                         0.000014*time_in_julian_2)
                        * math.sin(degree_to_radian*mean_time))
    mean_long_degree += ((0.019993 - 0.000101*time_in_julian) *
                         math.sin(degree_to_radian*2*mean_time) +
                         0.000290*math.sin(degree_to_radian*3*mean_time))
    long_degree = mean_degree + mean_long_degree  # true longitude, degree
    long_degree = long_degree * degree_to_radian
    long_degree = long_degree - math.pi*2*(int(long_degree / (math.pi*2)))
    # Normalize to (0, 2*math.pi)
    return long_degree


def get_sun_longitude(dayNumber, timeZone):
    '''
    ' Compute sun position at midnight of the day with the
    ' given Julian day number.
    ' The time zone if the time difference between local time
    ' and UTC: 7.0 for UTC+7:00.
    ' The function returns a number between 0 and 11.
    ' From the day after March equinox and the 1st major term
    ' after March equinox,
    ' 0 is returned. After that, return 1, 2, 3 ...
    '''
    return int(sun_longitude(dayNumber - 0.5 - timeZone / 24)
               / math.pi*6)


def get_new_moon_day(k, timeZone):
    '''
    ' Compute the day of the k-th new moon in the given time zone.
    ' The time zone if the time difference between
    ' local time and UTC: 7.0 for UTC+7:00
    '''
    return int(new_moon(k) + 0.5 + timeZone / 24.)


def get_lunar_month_11(yy, timeZone):
    '''
    ' Find the day that starts the luner month 11 of the given year
    ' for the given time zone
    '''
    off = julian_day_from_date(31, 12, yy) - 2415021.
    k = int(off / 29.530588853)
    lunar_month = get_new_moon_day(k, timeZone)
    sun_long = get_sun_longitude(lunar_month, timeZone)
    # sun longitude at local midnight
    if sun_long >= 9:
        lunar_month = get_new_moon_day(k - 1, timeZone)
    return lunar_month


def get_leap_month_offset(a11, timeZone):
    '''
    ' Find the index of the leap month after the month starting on the day a11.
    '''
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1  # start with month following lunar month 11
    arc = get_sun_longitude(get_new_moon_day(k + i, timeZone),
                            timeZone)
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(get_new_moon_day(k + i, timeZone),
                                timeZone)
        if not (arc != last and i < 14):
            break
    return i - 1


def solar_to_lunar(solar_dd, solar_mm, solar_yy, time_zone=7):
    '''
    ' Convert solar date dd/mm/yyyy to the corresponding lunar date
    ' params: day, month, year in solar calendar ;
             time_zone with default = 7 (Ha Noi time zone)
    ' rtype: list with 4 elements
            0: dd : In lunar calendar
            1: mm : In lunar calendar
            2: yy : In lunar calendar
            3: Is leap month: 1 --> leap month
    '''
    time_zone = 7
    day_number = julian_day_from_date(solar_dd, solar_mm, solar_yy)
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k + 1, time_zone)
    if month_start > day_number:
        month_start = get_new_moon_day(k, time_zone)
    # alert(dayNumber + " -> " + monthStart)
    a11 = get_lunar_month_11(solar_yy, time_zone)
    b11 = a11
    if a11 >= month_start:
        lunar_year = solar_yy
        a11 = get_lunar_month_11(solar_yy - 1, time_zone)
    else:
        lunar_year = solar_yy + 1
        b11 = get_lunar_month_11(solar_yy + 1, time_zone)
    lunar_day = day_number - month_start + 1
    diff = int((month_start - a11) / 29.)
    lunar_leap = 0
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_month_diff = \
            get_leap_month_offset(a11, time_zone)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
        if diff == leap_month_diff:
            lunar_leap = 1
    if lunar_month > 12:
        lunar_month = lunar_month - 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return [lunar_day, lunar_month, lunar_year, lunar_leap]


def lunar_to_solar(lunar_day, lunar_month, lunar_year,
                   lunar_leap_month, time_zone=7):
    '''Convert a lunar date to the corresponding solar date.
    ' params: dd, mm, yy in lunar calendar
            : leap_month: 1 if leap month; 0 if not leap month
            : time_zone: default = 7 - Hanoi timezone
     rtype  : list with 3 elements
            0: dd : In solar calendar
            1: mm : In solar calendar
            2: yy : In solar calendar
    '''
    if lunar_month < 11:
        a11 = get_lunar_month_11(lunar_year - 1, time_zone)
        b11 = get_lunar_month_11(lunar_year, time_zone)
    else:
        a11 = get_lunar_month_11(lunar_year, time_zone)
        b11 = get_lunar_month_11(lunar_year + 1, time_zone)
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunar_month - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        leap_off = get_leap_month_offset(a11, time_zone)
        leap_month = leap_off - 2
        if leap_month < 0:
            leap_month += 12
        if lunar_leap_month != 0 and lunar_month != leap_month:
            return [0, 0, 0]
        elif lunar_leap_month != 0 or off >= leap_off:
            off += 1
    month_start = get_new_moon_day(k + off, time_zone)
    return julian_day_to_date(month_start + lunar_day - 1)


def day_in_week(solar_dd, solar_mm, solar_yy, viet_language=1):
    '''Get day in week by algrorithm: get julian day, get mod of julian day and 7
    'Params: 3 elements and 1 default element
            0: dd : In solar calendar
            1: mm : In solar calendar
            2: yy : In solar calendar
            3: viet_language: default = 1 return Vietnamese language
                            : other value return English language
    '''
    julian_day = julian_day_from_date(solar_dd, solar_mm, solar_yy)
    date_index = julian_day % 7
    if viet_language:
        _day_in_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5",
                        "Thứ 6", "Thứ 7", "Chủ nhật"]
    else:
        _day_in_week = ["Mon", "Tue", "Wed", "Thu",
                        "Fri", "Sat", "Sun"]
    return _day_in_week[date_index]


def zodiac_year(year):
    '''Find year in CAN-CHI (zodiac) name'''
    can_index = (year + 6) % 10
    chi_index = (year + 8) % 12
    return "{} {}".format(CAN[can_index], CHI[chi_index])


def zodiac_day(solar_dd, solar_mm, solar_yy):
    '''Find day in CAN-CHI  (zodiac) name
    '  Params: day
    '        : month
    '        : year
    '  rtype: str
    '''
    julian_day = julian_day_from_date(solar_dd, solar_mm, solar_yy)
    can_index = (julian_day + 9) % 10
    chi_index = (julian_day + 1) % 12
    return "{} {}".format(CAN[can_index], CHI[chi_index])


def lunar_leap(yy):
    '''find leap year
    params: yy - year
    rtype: 1 - leap year
           0 - not leap year
    '''
    if yy % 19 in [0, 3, 6, 9, 11, 14, 17]:
        return 1
    else:
        return 0


def zodiac_month(month, year):
    '''Month in CAN-CHI name
    '  Params: month of lunar calendar
    '        : year
    '  rtype: str
    '''
    can_index = (year * 12 + month + 3) % 10
    return "{} {}".format(CAN[can_index], CHI_MONTH[month])


def solar_to_lunar_string(solar_dd, solar_mm, solar_yy, time_zone=7):
    lunar_day = solar_to_lunar(solar_dd, solar_mm, solar_yy, time_zone)
    _day_in_week = day_in_week(solar_dd, solar_mm, solar_yy)
    _zodiac_year = zodiac_year(solar_yy)
    _zodiac_month = zodiac_month(lunar_day[1], lunar_day[3])
    _zodiac_day = zodiac_day(solar_dd, solar_mm, solar_yy)
    if lunar_day[3]:
        return "{} - {}/{}/{} AL {}; ngày :{} tháng: {} năm: {}".\
                format(_day_in_week, lunar_day[0], lunar_day[1],
                       lunar_day[2], "", _zodiac_day, _zodiac_month,
                       _zodiac_year)
    else:
        return "{} - {}/{}/{} AL{}; ngày: {} - tháng: {} - năm: {}".\
                format(_day_in_week, lunar_day[0], lunar_day[1],
                       lunar_day[2], "", _zodiac_day, _zodiac_month,
                       _zodiac_year)


def main():
    '''Example in use'''
    select = input("0. Convert solar to lunar. \n"\
          "1. Convert lunar to solar \n"\
          "Select (0/1): ")
    if select not in ["0", "1"]:
        print("Invalid input")
        return
    select = int(select)
    date_input = input("Enter date in dd/mm/yyyy format: ")
    try:
        solar = date_input.split("/")
        day = int(solar[0])
        month = int(solar[1])
        year = int(solar[2])
    except Exception as ex:
        print(str(ex))
        day = 0
    if day:
        if select:
            leap_month = input("Is leap month ? (0/1) - default 0: ")
            if leap_month not in ["0", "1"]:
                leap_month = 0
            leap_month = int(leap_month)
            if leap_month:
                temp_str = "Date {} leap month in lunar calendar is {} {} in solar calendar"
            else:
                temp_str = "Date {} in lunar calendar is {} {} in solar calendar"
            solar_date = lunar_to_solar(day, month, year, leap_month, 7)
            solar_day = day_in_week(solar_date[0], solar_date[1], solar_date[2], 0)
            print(temp_str.format(date_input, solar_day,
                                  "{}/{}/{}".format(solar_date[0],
                                                    solar_date[1],
                                                    solar_date[2])))
        else:
            print(solar_to_lunar_string(day, month, year, 7))
    else:
        print("Invalid input date dd/mm/YYYY")


if __name__ == "__main__":
    main()
