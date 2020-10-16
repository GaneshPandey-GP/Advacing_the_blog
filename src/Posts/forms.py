from django import forms
from django.contrib.auth import logout,get_user_model,authenticate,login
from pagedown.widgets import PagedownWidget
from .models import Post

User = get_user_model() 

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = ('title',
                   'image',
                  'content',
                  'draft',
                  'publish',)

class UserLoginForm(forms.Form):
    username =  forms.CharField()
    password =  forms.CharField(widget=forms.PasswordInput) 
    
    def clean(self,*args,**kwargs):
        username =  self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("This  user does  not exits.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password.")
            if not user.is_active:
                raise forms.ValidationError("This  user is not longer active.")
        return super(UserLoginForm,self).clean(*args,**kwargs)    

class UserRegisterForm(forms.ModelForm):
    email  = forms.EmailField(label="Emali Address")
    password = forms.CharField(label="Password",widget=forms.PasswordInput) 
    password1 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput) 
    class Meta:
        model = User
        fields = ["username","email","password","password1"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has been already registerd.")
        return email

    def clean_password1(self):
       password  = self.cleaned_data.get("password")
       password1 = self.cleaned_data.get("password1")
       if password != password1:
           raise forms.ValidationError("Password Does not match.")
       return password