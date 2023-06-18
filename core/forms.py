
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from utils import send__activation_mail



class UserCreationForm(BaseCreationForm):
    class Meta:
        fields = (
            'email', 'name',
            'password1', 'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        send__activation_mail(user)
        return user
