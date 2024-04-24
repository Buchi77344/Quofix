from django import forms
from base.models import Available_Balance , NairaWallet ,EURWallet ,GPBWallet
# from .models  import MarchantUser

class AvailableBalanceForm(forms.ModelForm):
    class Meta:
        model =Available_Balance
        fields = ['balance',]
# class MarchantUserForm(forms.ModelForm):
#     class Meat:
#         model= MarchantUser
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']


class Searchform(forms.Form):
    query = forms.CharField(max_length=100, required=False ,label= 'search')

