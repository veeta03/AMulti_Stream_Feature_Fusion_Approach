from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import datetime
import openpyxl
import numpy as np

from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,traffic_prediction_type,detection_ratio,detection_accuracy

def login(request):
    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            enter = ClientRegister_Model.objects.get(
                username=username,
                password=password
            )

            request.session["userid"] = enter.id
            return redirect('ViewYourProfile')

        except Exception as e:
            return HttpResponse(str(e))

    return render(request, 'RUser/login.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city)

        return render(request, 'RUser/Register1.html')
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_Traffic_Type(request):
    if request.method == "POST":

        if request.method == "POST":

            TRAFFIC_DATE= request.POST.get('TRAFFIC_DATE')
            TRAFFIC_TIME= request.POST.get('TRAFFIC_TIME')
            BOROUGH= request.POST.get('BOROUGH')
            ZIP_CODE= request.POST.get('ZIP_CODE')
            LATITUDE= request.POST.get('LATITUDE')
            LONGITUDE= request.POST.get('LONGITUDE')
            LOCATION= request.POST.get('LOCATION')
            ON_STREET_NAME= request.POST.get('ON_STREET_NAME')
            CROSS_STREET_NAME= request.POST.get('CROSS_STREET_NAME')
            OFF_STREET_NAME= request.POST.get('OFF_STREET_NAME')
            CONTRIBUTING_FACTOR_VEHICLE= request.POST.get('CONTRIBUTING_FACTOR_VEHICLE')
            REFERENCE_ID= request.POST.get('REFERENCE_ID')
            TRAFFIC_VEHICLE_TYPE_CODE1= request.POST.get('TRAFFIC_VEHICLE_TYPE_CODE1')
            TRAFFIC_VEHICLE_TYPE_CODE2= request.POST.get('TRAFFIC_VEHICLE_TYPE_CODE2')
            Junction= request.POST.get('JUNCTION')

        data = pd.read_csv("Traffic_Datasets.csv", encoding='latin-1')

        def apply_results(status):
            if (status == 0):
                return 0  # No Traffic
            elif (status == 1):
                return 1  # Traffic

        data['Results'] = data['Label'].apply(apply_results)

        x = data['REFERENCE_ID']
        y = data['Results']

        # cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))

        cv = CountVectorizer()

        # x = cv.fit_transform(data['text'].apply(lambda x: np.str_(x)))
        x = cv.fit_transform(data['REFERENCE_ID'].apply(lambda x: np.str_(x)))
        y = data['Results'].apply(lambda y: np.int_(y))

        print(x)
        print("Y")
        print(y)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Naive Bayes")

        from sklearn.naive_bayes import MultinomialNB

        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        predict_nb = NB.predict(X_test)
        naivebayes = accuracy_score(y_test, predict_nb) * 100
        print(naivebayes)
        print(confusion_matrix(y_test, predict_nb))
        print(classification_report(y_test, predict_nb))
        models.append(('naive_bayes', NB))

        # SVM Model
        print("SVM")
        from sklearn import svm

        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression

        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        REFERENCE_ID1 = [REFERENCE_ID]
        vector1 = cv.transform(REFERENCE_ID1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = str(pred.replace("]", ""))

        prediction = int(pred1)

        if prediction == 0:
            val = 'No Traffic Found'
        elif prediction == 1:
            val = 'Traffic Found'

        print(prediction)
        print(val)

        traffic_prediction_type.objects.create(
        TRAFFIC_DATE=TRAFFIC_DATE,
        TRAFFIC_TIME=TRAFFIC_TIME,
        BOROUGH=BOROUGH,
        ZIP_CODE=ZIP_CODE,
        LATITUDE=LATITUDE,
        LONGITUDE=LONGITUDE,
        LOCATION=LOCATION,
        ON_STREET_NAME=ON_STREET_NAME,
        CROSS_STREET_NAME=CROSS_STREET_NAME,
        OFF_STREET_NAME=OFF_STREET_NAME,
        CONTRIBUTING_FACTOR_VEHICLE=CONTRIBUTING_FACTOR_VEHICLE,
        REFERENCE_ID=REFERENCE_ID,
        TRAFFIC_VEHICLE_TYPE_CODE1=TRAFFIC_VEHICLE_TYPE_CODE1,
        TRAFFIC_VEHICLE_TYPE_CODE2=TRAFFIC_VEHICLE_TYPE_CODE2,
        Junction=Junction,
        Prediction=val)

        return render(request, 'RUser/Predict_Traffic_Type.html',{'objs': val})
    return render(request, 'RUser/Predict_Traffic_Type.html')



