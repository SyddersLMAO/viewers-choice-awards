
from django.shortcuts import render, redirect
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.db import transaction

from .models import Category, Nomination
from .forms import MultiNominationForm
from .turnstile import verify_turnstile

@ratelimit(key='ip', rate='5/10m', method='POST', block=True)
def nomination_categories(request):
    categories = Category.objects.filter(is_active=True)

    if request.COOKIES.get('nomination_submitted') == 'true':
        return redirect('nomination_success')

    if request.method == 'POST':
        form = MultiNominationForm(categories, request.POST)

        if form.is_valid():
            email = form.cleaned_data['submitter_email'].strip()

            if Nomination.objects.filter(
                submitter_email__iexact=email
            ).exists():
                form.add_error(
                    'submitter_email',
                    'This email address has already submitted nominations.'
                )
            else:
                token = form.cleaned_data['turnstile_token']
                remote_ip = request.META.get('REMOTE_ADDR')

                if not verify_turnstile(token, remote_ip):
                    form.add_error(
                        None,
                        'Verification failed. Please try again.'
                    )
                else:
                    with transaction.atomic():
                        for category in categories:
                            nominee_name = form.cleaned_data.get(
                                f'category_{category.id}'
                            )

                            if nominee_name:
                                Nomination.objects.create(
                                    category=category,
                                    nominee_name=nominee_name,
                                    submitter_email=email,
                                    submitted_by='Website visitor',
                                    reason='',
                                )

                    response = redirect('nomination_success')
                    response.set_cookie(
                        'nomination_submitted',
                        'true',
                        max_age=60 * 60 * 24 * 365,
                        secure=request.is_secure(),
                        httponly=True,
                        samesite='Lax',
                    )
                    return response

    else:
        form = MultiNominationForm(categories)

    category_fields = [
        {
            'category': category,
            'field': form[f'category_{category.id}'],
        }
        for category in categories
    ]

    return render(request, 'nominations/categories.html', {
        'form': form,
        'category_fields': category_fields,
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY,
    })


def nomination_success(request):
    return render(request, 'nominations/success.html')
