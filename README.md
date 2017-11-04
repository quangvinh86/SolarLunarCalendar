# Python_Solar_and_Lunar
Calculate Vietnam lunar calendar (some different with Chinese lunar calendar)

Base on Algorithm: \Algorithm\How to compute the Vietnamese lunar calendar.pdf

----------------------------------
HOW TO USE:

# I. RUN example in terminal (or console)

&gt; python LunarSolar.py

0. Convert solar to lunar. 
1. Convert lunar to solar 
Select (0/1): 0
Enter date in dd/mm/yyyy format: 04/11/2017
Thứ 7 - 16/9/2017 AL; ngày: Ất Mùi - tháng: Bính Tuất - năm: Đinh Dậu

&gt; python LunarSolar.py

0. Convert solar to lunar. 
1. Convert lunar to solar 
Select (0/1): 1
Enter date in dd/mm/yyyy format: 16/9/2017
Is leap month ? (0/1) - default 0: 0
Date 16/9/2017 in lunar calendar is Sat 4/11/2017 in solar calendar

# II. Function in file

## lunar_to_solar(lunar_day, lunar_month, lunar_year, lunar_leap_month, time_zone=7)

Convert a lunar date to the corresponding solar date.

params: 

            dd, mm, yy in lunar calendar
            : leap_month: 1 if leap month; 0 if not leap month
            : time_zone: default = 7 - Hanoi timezone

rtype  : list with 3 elements
            
            0: dd : In solar calendar
            1: mm : In solar calendar
            2: yy : In solar calendar


## solar_to_lunar(solar_dd, solar_mm, solar_yy, time_zone=7):
   
Convert solar date dd/mm/yyyy to the corresponding lunar date

params: 

       day, month, year in solar calendar ;
       time_zone with default = 7 (Ha Noi time zone)

rtype: list with 4 elements
            
            0: dd : In lunar calendar
            1: mm : In lunar calendar
            2: yy : In lunar calendar
            3: Is leap month: 1 --> leap month



## zodiac_month(month, year):
  
Month in CAN-CHI name

Params
      
      : month of lunar calendar
      
      : year

rtype: str


## zodiac_day(solar_dd, solar_mm, solar_yy):
  
Find day in CAN-CHI name

Params: day
      
      : month
      
      : year

rtype: str


## zodiac_year(year):
  
  '''Find year in CAN-CHI (zodiac) name'''

## lunar_leap(yy):

      find leap year

      params: yy - year

       rtype: 1 - leap year

              0 - not leap year


## day_in_week(solar_dd, solar_mm, solar_yy, viet_language=1):
  
Get day in week by algrorithm: get julian day, get mod of julian day and 7

Params: 3 elements and 1 default element
            
            0: dd : In solar calendar
            
            1: mm : In solar calendar
            
            2: yy : In solar calendar
            
            3: viet_language: default = 1 return Vietnamese language
                            : other value return English language
rtype: Str


