from django.conf import settings


def handle_uploaded_file(file):  
    with open(settings.MEDIA_ROOT+file.name, 'wb+') as destination:  

        for chunk in file.chunks():
            destination.write(chunk)
            
        return settings.MEDIA_ROOT+file.name
