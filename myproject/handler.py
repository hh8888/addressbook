from .models import address

def handle_uploaded_file(file){
    for row in file:
        newItem = address(email=row[0], name=row[1])
        newItem.save()
        #created = address.objects.bulk_create(email=row[0],name=row[1])
}