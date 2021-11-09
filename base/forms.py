from django.forms import ModelForm, fields
from .models import Message, Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields =  '__all__'
        exclude = ['host', 'participants']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields =  '__all__'