from django.shortcuts import render
from .models import address

import csv
import io
import codecs

#import pdb; pdb.set_trace()

# Create your views here.


from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from .forms import AddForm#, UploadFileForm
from django.core.files.storage import FileSystemStorage

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
                messages.info(request, 'Email "%s" alrealdy exist!' % email)
                oldItem = address.objects.get(email=email)
                oldItem.name=name
                oldItem.save()
            else:
                count = address.objects.count()
                newItem = address(email=email, name=name)
                newItem.save()
                messages.info(request, 'New contact "%s" added.' % email)    

    return addressbook(request)



def upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            csvfile = request.FILES['file']
            reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
        #try:
        count = 0
        current = 1
        if 'current' in request:
            current = request.current
        for row in reader:
            if(count>=current):
                if (address.objects.filter(email=row[0]).count()>0):
                    if(current == count):
                        if ('answer' in request and request['answer']=='Yes'):
                            oldItem = address.objects.get(email=row[0])
                            oldItem.name=row[1]
                            oldItem.save()
                    else:
                        message = 'Found existed record %s, override?' % row[0]
                        current = count
                        print("existed:",row[0])
                        return render(request, 'myapp/confirm.html', locals())
                else:
                    newItem = address(email=row[0],name=row[1])
                    newItem.save()
                    print("added:",row[0])
            count += 1
        #except:
        #    return HttpResponse("You need a csv file.")

        #for line in file.read().split('\n'):
        #for row in file:
            #newItem = address(email=row[0], name=row[1])
        #newItem.save()
        #created = address.objects.bulk_create(email=row[0],name=row[1])
        #    print(row[0])
        # uploadform = UploadFileForm(request.POST, request.FILES)
        # if uploadform.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            # return addressbook(request)
    # return render(request, 'upload.html', {'uploadform': uploadform})
    return addressbook(request)
