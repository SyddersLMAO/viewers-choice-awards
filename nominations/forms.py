
from django import forms


class MultiNominationForm(forms.Form):
    submitter_email = forms.EmailField(
        label='Your email address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
        })
    )

    turnstile_token = forms.CharField(
        required=True,
        widget=forms.HiddenInput()
    )

    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.categories = categories

        for category in categories:
            self.fields[f'category_{category.id}'] = forms.CharField(
                label=category.name,
                required=False,
                max_length=150,
                widget=forms.TextInput(attrs={
                    'placeholder': 'Enter a creator name',
                })
            )

    def clean(self):
        cleaned_data = super().clean()

        if not any(
            cleaned_data.get(f'category_{category.id}')
            for category in self.categories
        ):
            raise forms.ValidationError(
                'Please nominate at least one creator.'
            )

        return cleaned_data
