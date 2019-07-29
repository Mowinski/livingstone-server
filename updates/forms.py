from django import forms
from django.db.models import Max

from updates.models import Level


class AdminLevelForm(forms.ModelForm):
    def clean(self):
        order = self.cleaned_data.get('order')
        levels_set = self.cleaned_data.get('set')

        has_level = levels_set.level_set.filter(order=order).exists()
        if has_level:
            next_level = levels_set.level_set.aggregate(Max('order'))['order__max'] + 1
            self.add_error('order', "Selected numer level exists in database. Next available level is: {}".format(next_level))

        return self.cleaned_data

    class Meta:
        model = Level
        exclude = ['id', ]
