from django.shortcuts import render, redirect
from sklearn.preprocessing import StandardScaler
from django.views.generic import CreateView, View, UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import SkinUser, SkinData, PredictiveModel
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
import cv2
from PIL import Image
from tensorflow import keras
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from django.http import HttpResponse
import os
from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.db.models import Count



def generate_pdf(request):

    context = {
        'predictive_model': PredictiveModel.objects.first(),
        'user': User.objects.get(id=request.user.id),
        'current_date': datetime.now().date(),
        'skin_cancer_data': SkinData.objects.filter(user=request.user).order_by('-created').first()
    }

    template_path = 'report/report.html'
    template_str = render_to_string(template_path, context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="skin-cancer-report.pdf"'

    pisa_status = pisa.CreatePDF(
        template_str, dest=response,
        link_callback=lambda uri, _: os.path.join(settings.MEDIA_ROOT, uri)
    )

    if pisa_status.err:
        return HttpResponse('Failed to generate PDF')

    return response



class Home(View):
    template_name = 'skin_cancer/home.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    template_name = 'user/dashboard.html'

    def get(self, request):
        # ParkinsonUser.objects.get()
        users = User.objects.all()
        try:
            predictive_model = PredictiveModel.objects.order_by('-accuracy').first()
        except:
            predictive_model = 'No Model create yet'
            
        is_benign = SkinData.objects.filter(is_benign=True).values('user_id').annotate(count=Count('user_id')).distinct().count()
        is_malignant = SkinData.objects.filter(is_malignant=True).values('user_id').annotate(count=Count('user_id')).distinct().count()
        return render(request, self.template_name, {'users': users, 'is_benign': is_benign, 'is_malignant': is_malignant, 'predictive_model': predictive_model})


@method_decorator(login_required, name='dispatch')
class User_list(View):
    template_name = 'parkinson/user-list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class Profile(UpdateView):
    template_name = 'user/profile.html'

    def post(self, request):
        if request.POST:
            user = User.objects.get(id=request.user.id)
            try:
                SkinUser.objects.filter(user=user).exists()
                p_user = SkinUser.objects.get(user=user)
            except SkinUser.DoesNotExist:
                p_user = SkinUser.objects.create(user=user)

            user.first_name = self.request.POST['fname']
            user.last_name = self.request.POST['lname']

            p_user.contact = self.request.POST['contact']
            p_user.city = self.request.POST['city']
            p_user.country = self.request.POST['country']
            p_user.address = self.request.POST['address']

            if 'profile' in request.FILES:
                if p_user.profile_image:
                    p_user.profile_image.delete()
                    p_user.profile_image = self.request.FILES['profile']
                else:
                    p_user.profile_image = self.request.FILES['profile']

            user.save()
            p_user.save()

        return redirect('profile')

    def get(self, request):
        return render(request, self.template_name)



@method_decorator(login_required, name='dispatch')
class Start_predict(View):
    template_name = 'user/start-predict.html'

    def post(self, request):
        if request.method == 'POST' and 'input_skin_image' in request.FILES:
            input_skin_image = self.request.FILES['input_skin_image']
            skin_data =  SkinData.objects.create(user=request.user, skin_image=input_skin_image)
            
            input_skin_image = np.array(preprocess_input_image(input_skin_image))
            input_skin_image_reshape = input_skin_image.reshape(1, 224, 224, 3)
            
            prediction = predict(input_skin_image_reshape)
            prediction = np.argmax(prediction, 1)
            
            if prediction[0] == 0:
                skin_data.is_benign = True
            else:
                skin_data.is_malignant = True
            skin_data.save()
            
            return redirect('output')
        return redirect('start-predict')

    def get(self, request):
        return render(request, self.template_name)

    
    
def predict(image):
    model = keras.models.load_model('skin_cancer/final_skin_cancer_multinet_incep_xception_94.h5')
    prediction = model.predict(image)
    
    return prediction


def preprocess_input_image(image_path):
    img = np.asarray(Image.open(image_path).convert("RGB"))
    img = cv2.resize(img, (224, 224))
    img = np.array(img)
    
    return img


@login_required
def output(request):
    context = {
        'predictive_model': PredictiveModel.objects.first(),
        'user': User.objects.get(id=request.user.id),
        'current_date': datetime.now().date(),
    }
    return render(request, 'skin_cancer/output.html', context)






# @login_required
# def report(request):
#     context = {
#         'predictive_model': PredictiveModel.objects.first(),
#         'user': User.objects.get(id=request.user.id),
#         'current_date': datetime.now().date(),
#     }
#     return render(request, 'report/report.html', context) 

# fo,fhi,flo,jitter,jitter_abs,rap,ppq,ddp,shimmer,shimmer_db,apq3,apq5,apq,dda,nhr,hnr,rpde,dfa,spread1,spread2,d2,ppe


    def input_image(image):
        if image:
            input_skin_image = image
            
            input_skin_image = np.array(preprocess_input_image(input_skin_image))
            input_skin_image_reshape = input_skin_image.reshape(1, 224, 224, 3)
            
            prediction = predict(input_skin_image_reshape)
            prediction = np.argmax(prediction, 1)
            
            is_benign = 0
            if prediction[0] == 0:
                is_benign = True
            else:
                is_benign = False
            
        return is_benign