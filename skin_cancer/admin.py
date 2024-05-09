from django.contrib import admin
from .models import SkinUser, SkinData, PredictiveModel


class SkinUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_img', 'gender', 'address', 'country', 'city', 'contact', 'status')
admin.site.register(SkinUser, SkinUserAdmin)



class SkinDataAdmin(admin.ModelAdmin):
    list_display = ('user_img', 'user', 'skin_img', 'is_benign', 'is_malignant', 'status')
admin.site.register(SkinData, SkinDataAdmin)



class PredictiveModelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'accuracy', 'precision', 'recall', 'f1_score', 'status')
admin.site.register(PredictiveModel, PredictiveModelAdmin)
