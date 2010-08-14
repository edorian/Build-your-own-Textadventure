from django import forms
from website.adventure.models import Adventure


class AdventureCreateForm(forms.ModelForm):
    class Meta:
        model = Adventure
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(AdventureCreateForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if self._meta.model.objects.filter(author=self.author, name=name).exists():
            raise forms.ValidationError(
                u"You've already created another adventure with the same name. "
                u"Please use a different name.")
        return name

    def save(self, commit=True, *args, **kwargs):
        obj = super(AdventureCreateForm, self).save(commit=False, *args, **kwargs)
        obj.author = self.author
        if commit:
            obj.save()
        return obj
