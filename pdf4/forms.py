from django import forms
#from . models import Message



#class MessageForm(forms.ModelForm):
#    class Meta:
#        model = Message
#        fields = ('text', 'file1', 'file2', 'file3')



class MergeForm(forms.Form):
    file0 = forms.FileField()
    file1 = forms.FileField()


