from django.shortcuts import render
from .models import Contact
from nettools.forms import ContactForm
# Create your views here.

def display_phone_book(request):
    added = False
    err = False
    if request.method == 'POST':
        print('Info: Request method POST')
        contacts = ContactForm(request.POST, prefix='contact')
        if contacts.is_valid():
            print('Info: Contact Form is valid')
            try:
                contacts.save()
                added = True
            except Exception as e:
                print('Error: Contact data has not been saved in Contact DB.')
                added = False
        else:
            print('Error: Contact Form is not valid')
            print(contacts.errors)
            err = contacts
    else:
        print('Info: Request method GET')
        if 'del' in request.GET:
            d = request.GET['del']
            print(d)
            print('Info: Trying to delete "{}" from Contact DB.'.format(d))
            try:
                Contact.objects.filter(id=d).delete()
                print('Info: "{}" has been deleted from Contact DB.'.format(d))
            except Exception as e:
                print('Error: "{}" can not be removed from Contact DB.'.format(d))
                print('Error: {}'.format(e))
        if 'q' in request.GET:
            search = request.GET['q']
            if search != '':
                print('Info: Searching for "{}" in Contact DB.'.format(search))
                contacts = Contact.objects.filter(organization__icontains=search)
                return render(request, 'phones.html', {'contacts': contacts})
    contacts = Contact.objects.all().order_by('organization')
    print('Info: Default output.')
    return render(request, 'phones.html', {'contacts':contacts, 'added':added, 'err':err})