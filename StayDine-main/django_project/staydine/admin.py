from django.contrib import admin
from .models import Contact, Dining, Accommodation, MenuItem, RoomType, Highlights, BedType

# Register your models here.
admin.site.register(Contact)
admin.site.register(MenuItem)
admin.site.register(Dining)
admin.site.register(RoomType)
admin.site.register(Accommodation)
admin.site.register(Highlights)
admin.site.register(BedType)
