from django import forms
from semester.semester import Semester
from semester.widgets import SplitSeasonYearWidget
from ajaxwidgets.fields import OtherChoiceField

class SemesterFormField(forms.CharField):
    def clean(self, value):
        try:
            return Semester(value)
        except InvalidSemester, e:
            raise forms.ValidationError("Semester is invalid")

_GRAD_SEASON_CHOICES = (("sp", "Spring"), ("fa", "Fall"))
_GRAD_YEAR_CHOICES = [(x, x) for x in range(2015, 2005, -1)]

class SemesterSplitFormField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        seasons = kwargs.pop('seasons', _GRAD_SEASON_CHOICES)
        years = kwargs.pop('years', _GRAD_YEAR_CHOICES)
        fields = (
            forms.ChoiceField(choices=seasons),
            OtherChoiceField(choices=years, field_class=forms.IntegerField(min_value=1900, max_value=2100)),
        )
        self.widget = SplitSeasonYearWidget(seasons, years)
        super(SemesterSplitFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if not data_list:
            return None
        if data_list[0] in (None, ''):
            raise forms.ValidationError("Enter a valid season")
        if data_list[1] in (None, ''):
            raise forms.ValidationError("Enter a valid year")
        return Semester(season_name=data_list[0], year=data_list[1])
