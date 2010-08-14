from django import forms
from website.adventure.models import Adventure, Location


class AdventureCreateForm(forms.ModelForm):
    class Meta:
        model = Adventure
        fields = ('name', 'description', 'language')

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(AdventureCreateForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        queryset = self._meta.model.objects.all()
        if self.instance.pk is None:
            queryset = queryset.filter(author=self.author)
        else:
            queryset = queryset.filter(author=self.instance.author)
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.filter(name=name).exists():
            raise forms.ValidationError(
                u"You've already created another adventure with the same name. "
                u"Please use a different name.")
        return name

    def save(self, commit=True, *args, **kwargs):
        obj = super(AdventureCreateForm, self).save(commit=False, *args, **kwargs)
        if self.instance.pk is None:
            obj.author = self.author
        if commit:
            obj.save()
        return obj


class AdventureChangeForm(AdventureCreateForm):
    class Meta:
        model = Adventure
        fields = ('name', 'description', 'language', 'published',)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('title', 'description', 'type',)
        widgets = {
            'type': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        self.adventure = kwargs.pop('adventure', None)
        super(LocationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        obj = super(LocationForm, self).save(commit=False, *args, **kwargs)
        if self.instance.pk is None:
            obj.adventure = self.adventure
        if commit:
            obj.save()
        return obj
