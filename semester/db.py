from django.db import models
from semester.semester import Semester
import types

class SemesterField(models.CharField):
    """ 
    handles serializing a semester to the database in the following format:
    <sort_prefix><separator><semester> e.g.
    
    sort_prefix will be a date, separator is unique, semester is e.g. fa2007
    """
    __metaclass__ = models.SubfieldBase
    SEPARATOR = "__SEMESTER__"
    PREFIX_DATE_FORMAT = "%Y%m%d"
    """ a format like 20080822 """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 30
        super(SemesterField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not type(value) in types.StringTypes:
            return value
        try:
            semester = value.split(SemesterField.SEPARATOR)
            assert len(semester) == 2
            return Semester(semester[1])
        except:
            return value

    def get_db_prep_value(self, value):
        if value is None:
            return None
        if type(value) in types.StringTypes:
            if len(value.split(SemesterField.SEPARATOR)) == 2:
                return value
            else:
                value = Semester(value)
        if type(value) == Semester:
            return "%s%s%s" % (value.start_date.strftime(SemesterField.PREFIX_DATE_FORMAT),
                               SemesterField.SEPARATOR,
                               value.abbr())
        return value


