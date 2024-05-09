from skin_cancer.models import SkinUser, SkinData, PredictiveModel
    
def skin_cancer_data_exist(request):
    skin_cancer_data = False
    if request.user.is_authenticated:
        try:
            # skin_cancer_data = SkinData.objects.latest('id')
            skin_cancer_data = SkinData.objects.filter(user=request.user).order_by('-created').first()
        except SkinData.DoesNotExist:
            skin_cancer_data = False

    return {
        'skin_cancer_data': skin_cancer_data
    }