#!/usr/bin/env python
import datetime

_SEASON_MONTHS = {"sp" : 1, "su" : 6, "fa" : 8}
_SEASON_END_MONTHS = {"sp" : 5, "su" : 7, "fa" : 12}
_SEASON_MONTHS_REVERSE = {1 : "sp", 6 : "su", 8 : "fa"}
_SEASON_NAMES = {"sp" : "spring", "fa" : "fall", "su" : "summer"}

class InvalidSemester(ValueError):
    pass

def current_semester():
    from properties import PROPERTIES
    return Semester(PROPERTIES.semester)

def current_year():
    return current_semester().year


class Semester(object):
    @staticmethod
    def for_semester(semester):
        season = semester.lower()[:2]
        year = int(semester[2:])
        return Semester(season_name=season, year=year)

    @staticmethod
    def for_date(date):
        def get_season():
            months = _SEASON_END_MONTHS.items()
            months.sort(key=lambda x: x[1])
            for month in months:
                if date.month <= month[1]:
                    return _SEASON_NAMES[month[0]]
            return None
        return Semester(season_name=get_season(), year=date.year)

    def __init__(self, semester=None, season_name=None, year=None):
        try:
            if semester is not None:
                self.season = semester.lower()[:2]
                self.year = int(semester[2:])
            elif season_name is not None and year is not None:
                self.season = season_name.lower()[:2]
                self.year = int(year)
            else:
                raise InvalidSemester("Need to specify either semester or season_name and year")
        except (IndexError, ValueError), e:
                raise InvalidSemester("Semester value provided is invalid")

        self.semester = "%s%s" % (self.season, str(self.year%100).rjust(2, "0"))
        try:
            self.season_name = _SEASON_NAMES[self.season]
        except KeyError:
            raise InvalidSemester("%s is not a valid season" % self.season)
            

        if self.year < 100:
            self.year += 1900
            if self.year < 1960:
                self.year += 100

    def __str__(self):
        return self.abbr()

    def __unicode__(self):
        return unicode(str(self))

    def __repr__(self):
        return '<Semester: %s>' % str(self)


    def __cmp__(self, other):
        if isinstance(other, str):
            try:
                return cmp(self, Semester(other))
            except InvalidSemester:
                pass
        if not isinstance(other, Semester):
            return -1

        e = cmp(self.year, other.year)
        if e != 0:
            return e
        return cmp(_SEASON_MONTHS[self.season], _SEASON_MONTHS[other.season])
            
    
    def abbr(self):
        return self.semester
    
    def verbose_description(self):
        return "%s %d" % (self.season_name.capitalize(), self.year)

    @property
    def start_date(self):
        return datetime.date(self.year, _SEASON_MONTHS[self.season], 1)

    @property
    def end_date(self):
        return datetime.date(self.year, _SEASON_END_MONTHS[self.season], 30)

    @property
    def next(self):
        s = self.semester[:2]
        if s == "fa":
            y = self.year+1
            return Semester("%s%s" % ("sp", y))
        else:
            y = self.year
            return Semester("%s%s" % ("fa", y))
        
    @property
    def previous(self):
        s = self.semester[:2]
        if s == "sp":
            y = self.year-1
            return Semester("%s%s" % ("fa", y))
        else:
            y = self.year%100            
            return Semester("%s%s" % ("sp", y))

