from django.core.mail import send_mail,EmailMultiAlternatives,EmailMessage
from Timesheet.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect


class Mail:
    def mailgenerate(request,subject,plain_message,EMAIL_HOST_USER,to,cc,html_content):
        mail = EmailMultiAlternatives(subject,plain_message, EMAIL_HOST_USER, to,cc=cc)
        mail.attach_alternative(html_content,'text/html')
        mail.send()
        messages.success(request, 'Mail Send Successfully \U0001F44D \U0001F44D \U0001F44D')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
