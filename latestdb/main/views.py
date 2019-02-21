
import csv,io
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import user, roleper

# Create your views here.
@permission_required('admin.can_add_log_entry')
def contact_upload(request):
    template="contact_upload.html"
    promt={
        'order': 'Order of csv should be proper'
    }
    if request.method=="GET":
        return render(request,template,promt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'This is not a csv file')

    data_set=csv_file.read().decode('UTF-8')
    io_string=io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar='|'):
        _, created=user.objects.update_or_create(
            empId=column[0],
            password =column[1],
            FName=column[2],
            LName = column[3],
            Gender = column[4],
            EmailId =column[5],
            Phone = column[6],
            Address =column[7],
            MgName =column[8],
            Mg_email =column[9],
            Location =column[10],
            RId = roleper.objects.get(pk=column[11])
        )

    context={}
    return  render(request,template,context)
