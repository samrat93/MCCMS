from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(State)
admin.site.register(Country)
admin.site.register(Complain)
admin.site.register(Complaint_Category)
admin.site.register(Complaint_Sub_Category)
admin.site.register(Municipality)
