from django.forms import ModelForm
from . models import Room



class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields = '__all__'# it creat all form field  accoding to  Room Field
        