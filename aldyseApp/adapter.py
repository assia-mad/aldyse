from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.wilaya = data.get('wilaya')
        user.commune = data.get('commune')
        user.tel= data.get('tel')
        user.age = data.get('age')
        user.role = data.get('role')
        user.gender = data.get('gender')
        user.otp = data.get('otp')
        user.is_active = data.get('is_active')
        user.save()
        return user