from django.shortcuts import render
from .models import address

import csv
import codecs
from django.shortcuts import HttpResponse, render, render_to_response
from django.template import RequestContext
from django.contrib import messages
from .forms import AddForm#, UploadFileForm
from django.core.files.storage import FileSystemStorage
from django.template.context_processors import csrf

#import pdb; pdb.set_trace()

def addressbook(request):
    form = AddForm()
    addressList = address.objects.all()
    return render(request, 'myapp/index.html', locals())


def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            if address.objects.filter(email=email).exists():
                row = [email, name]
                request.session["email"] = email
                request.session["name"] = name
                return askConfirm(row, 0, request)
            else:
                addRecord(email, name)
                messages.info(request, 'New contact "%s" added.' % email)
    return addressbook(request)

def upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            try:
                csvfile = request.FILES['file']
                if not request.FILES['file'].name.split(".")[-1] == "csv":
                    raise("File extenxion is not csv.")
                handle_uploaded_file(csvfile)
                reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
            except:
                return HttpResponse("You need a proper csv file.")
        else:
            return HttpResponse("You need to select a csv file.")
    count = 0
    for row in reader:
        if not handleRow(row, count):
            return askConfirm(row, count, request)
        count += 1
    return addressbook(request)

def continueProcessCSV(request):
    count = 0
    currentRow = int(request.POST["current"])
    # single add through form
    if currentRow==0:
        if 'Yes' in request.POST:
            email = request.session["email"]
            name = request.session["name"]
            updateRecord(email=email, name=name)
            messages.info(request, 'Single record updated.')
        elif 'No' in request.POST:
            messages.info(request, 'Single record skiped.')
        return addressbook(request)
    # multiple add through csv
    with open('addsave.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if count==currentRow :
                if 'Yes' in request.POST:
                    updateRecord(email=row[0], name=row[1])
                    messages.info(request, 'Updated %s.' % row[0])
                elif 'No' in request.POST:
                    messages.info(request, 'Skiped %s.' % row[0])
            elif count > currentRow:
                if not handleRow(row, count):
                    return askConfirm(row, count, request)
            count += 1
    messages.info(request, 'CSV processed.')
    return addressbook(request)

def ifExist(row):
    return address.objects.filter(email=row[0]).count()>0

def handleRow(row, currentRowIndex):
    if currentRowIndex == 0: #is csv header
        return True
    if ifExist(row):    # existed
        return False
    else:
        addRecord(row)  # add new
        return True

def askConfirm(row, currentRowIndex, request):
    message = 'Found existed record %s, override?' % row[0]
    current = currentRowIndex
    action_link = "/myapp/continue/"
    return render(request, 'myapp/confirm.html', locals())

def addRecord(email, name):
    newItem = address(email=email, name=name)
    newItem.save()

def updateRecord(email, name):
    oldItem = address.objects.get(email=email)
    oldItem.name = name
    oldItem.save()

def handle_uploaded_file(f):
    destination = open('./addsave.csv', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
