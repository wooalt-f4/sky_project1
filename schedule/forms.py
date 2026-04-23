from django import forms
from .models import Meeting


class MeetingForm(forms.ModelForm):
    """Form for creating and editing meetings with Bootstrap styling."""

    class Meta:
        model = Meeting
        fields = ['title', 'team', 'date', 'time', 'platform', 'status', 'description', 'location']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sprint Review'}),
            'team':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Alpha Team'}),
            'date':        forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time':        forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'platform':    forms.Select(attrs={'class': 'form-select'}),
            'status':      forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes about this meeting'}),
            'location':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Room 4B or remote link'}),
        }

    def clean_date(self):
        """Prevent meetings from being created with a past date."""
        from datetime import date
        selected_date = self.cleaned_data.get('date')
        if selected_date and selected_date < date.today():
            raise forms.ValidationError('Meeting date cannot be in the past.')
        return selected_date