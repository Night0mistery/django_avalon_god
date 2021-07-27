from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RoleVisionForm(forms.Form):
    role_vision = forms.CharField(help_text="Input your role to check your vision.")

    def clean_role_vision(self):
        data = self.cleaned_data['role_vision']
        roles = ['merlin', 'percival', 'servant', 'morgana', 'assassin', 'minion', 'oberon', 'mordred']
        # check if data in roles
        if data.lower() not in roles:
            raise ValidationError(_('Invalid role! Please ckeck your spell.'))

        return data

class VoteForm(forms.Form):
    vote = forms.BooleanField(help_text="Input your vote descision.")

    def clean_vote(self):
        data = self.cleaned_data['vote']

        return data

class NameForm(forms.Form):
    name = forms.CharField(help_text="Input your name here.")

    def clean_name(self):
        data = self.cleaned_data['name']

        return data