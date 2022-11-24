from django import forms
from .models import ML_Model, Evaluation


class MakeMLModelForm(forms.ModelForm):
    class Meta:
        model = ML_Model
        fields = ['title', 'version', 'is_selected']


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['total', 'success']

    def clean_total(self):
        total = self.cleaned_data['total']

        if total < 0:
            self.add_error("total", "Total must bigger than 0")

        return total

    def clean_success(self):
        total = self.cleaned_data['total']
        success = self.cleaned_data['success']

        if success < 0:
            self.add_error("success", "must bigger than 0")
        if total < success:
            self.add_error("success", "cant bigger than total")

        return success

    # def clean_percentage(self):
    #     total = self.cleaned_data['total']
    #     success = self.cleaned_data['success']
    #
    #     percentage = round(success / total, 2)
    #
    #     return percentage
