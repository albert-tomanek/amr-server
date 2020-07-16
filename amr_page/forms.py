from django import forms

class DownloadForm(forms.Form):
    yt_url = forms.URLField(label='YouTube video URL', max_length=200, required=False)
    yt_search = forms.CharField(label='OR search query', required=False)
    quality = forms.ChoiceField(choices=[
        ('7', 'default'),

        ('0', '4.75 kbit/s'),
        ('1', '5.15 kbit/s'),
        ('2', '5.9 kbit/s'),
        ('3', '6.7 kbit/s'),
        ('4', '7.4 kbit/s'),
        ('5', '7.95 kbit/s'),
        ('6', '10.2 kbit/s'),
        ('7', '12.2 kbit/s'),

        ('8', 'wide 6.6 kbit/s'),
        ('9', 'wide 8.85 kbit/s'),
        ('10', 'wide 12.65 kbit/s'),
        ('11', 'wide 14.25 kbit/s'),
        ('12', 'wide 15.85 kbit/s'),
        ('13', 'wide 18.25 kbit/s'),
        ('14', 'wide 19.85 kbit/s'),
        ('15', 'wide 23.05 kbit/s'),
        ('16', 'wide 23.85 kbit/s'),
    ])
