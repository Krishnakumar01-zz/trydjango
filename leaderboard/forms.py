from django import forms

from .models import Scorecard

class ScoreForm(forms.ModelForm):
	class Meta:
		model=Scorecard
		fields=['name','marks']

	def clean_name(self):
		name=self.cleaned_data.get('name')
		return name

	def clean_score(self):
		marks=self.cleaned_data.get('marks')