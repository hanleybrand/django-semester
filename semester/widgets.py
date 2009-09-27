from django import forms
from ajaxwidgets.widgets import OtherSelectWidget

class SplitSeasonYearWidget(forms.MultiWidget):
    def __init__(self, seasons, years, attrs=None):
        widgets = (
            forms.Select(choices=seasons, attrs=attrs),
            OtherSelectWidget(choices=years, attrs=attrs),
        )
        super(SplitSeasonYearWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if not value:
            return [None, None]
        elif not isinstance(value, Semester):
            raise ValueError("Value is not a Semester object")
        return [value.season, str(value.year)]

    def value_from_datadict(self, data, files, name):
        if isinstance(data.get(name, None), Semester):
            for i, subvalue in enumerate(self.decompress(data[name])):
                data['%s_%d' % (name, i)] = subvalue
        ret = super(SplitSeasonYearWidget, self).value_from_datadict(data, files, name)
        return ret

