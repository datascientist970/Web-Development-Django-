from django.shortcuts import render

from django.http import JsonResponse
import joblib

model = joblib.load('prediction/model/house.pkl')

def prediction(request):
    predicted_price = None
    if request.method=='POST':
        bedroom=int(request.POST['bedrooms'])
        space=int(request.POST['space'])	
        room=int(request.POST['room'])
        Lot=int(request.POST['Lot'])
        tax=int(request.POST['Tax'])
        bathroom=int(request.POST['bathroom'])
        garage=int(request.POST['garage'])
        condition=int(request.POST['cond'])

        prediction_input = [[bedroom,space,room,Lot,tax,bathroom,garage,condition]]

        predicted_price = model.predict(prediction_input)[0]

        print(prediction_input) 
    return render(request,'prediction.html', {'predicted_price': predicted_price})
