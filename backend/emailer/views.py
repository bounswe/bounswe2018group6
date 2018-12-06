from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.views import View

from api.models import User
from .models import EmailLog
from .tokens import account_activation_token


def send_activation_email(user):
    recipient = user.email
    token = account_activation_token.make_token(user)
    activate_url = urljoin(settings.HOST_ROOT_URL, 
                            'e/activate/{uid}/{token}/'.format(uid=user.pk, token=token))
    
    message = 'Welcome to Cultidate!\n\nTo activate your account please click here: {url}\n\nBest regards,\nCultidate Team'.format(url=activate_url)
    
    try:
        send_mail(
            '[Cultidate] Activate your account',
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
            fail_silently=False
        )
        sent = True
    except:
        sent = False
    
    EmailLog.objects.create(user=user,
                            sender=settings.EMAIL_HOST_USER,
                            recipient=recipient,
                            success=sent)

    return sent


class ActivateAccountView(View):
    # This class is partially gathered from here: https://bit.ly/2Ah5rWW Thanks to him.
    def get(self, request, uid, token):
        try:
            uid = force_text(uid)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return redirect(settings.FRONTEND_LOGIN_URL, permanent=True)
        else:
            # invalid link
            # return HTTP_406_NOT_ACCEPTABLE
            return HttpResponse('Activation unsuccessful.', status=406)
