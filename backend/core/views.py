import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import AffPartner, Referral, Commission


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['affpartner_count'] = AffPartner.objects.count()
    ctx['affpartner_active'] = AffPartner.objects.filter(status='active').count()
    ctx['affpartner_pending'] = AffPartner.objects.filter(status='pending').count()
    ctx['affpartner_suspended'] = AffPartner.objects.filter(status='suspended').count()
    ctx['affpartner_total_commission_rate'] = AffPartner.objects.aggregate(t=Sum('commission_rate'))['t'] or 0
    ctx['referral_count'] = Referral.objects.count()
    ctx['referral_pending'] = Referral.objects.filter(status='pending').count()
    ctx['referral_converted'] = Referral.objects.filter(status='converted').count()
    ctx['referral_rejected'] = Referral.objects.filter(status='rejected').count()
    ctx['referral_total_commission'] = Referral.objects.aggregate(t=Sum('commission'))['t'] or 0
    ctx['commission_count'] = Commission.objects.count()
    ctx['commission_pending'] = Commission.objects.filter(status='pending').count()
    ctx['commission_approved'] = Commission.objects.filter(status='approved').count()
    ctx['commission_paid'] = Commission.objects.filter(status='paid').count()
    ctx['commission_total_amount'] = Commission.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['recent'] = AffPartner.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def affpartner_list(request):
    qs = AffPartner.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'affpartner_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def affpartner_create(request):
    if request.method == 'POST':
        obj = AffPartner()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.website = request.POST.get('website', '')
        obj.commission_rate = request.POST.get('commission_rate') or 0
        obj.total_earned = request.POST.get('total_earned') or 0
        obj.total_referrals = request.POST.get('total_referrals') or 0
        obj.status = request.POST.get('status', '')
        obj.joined_date = request.POST.get('joined_date') or None
        obj.payment_method = request.POST.get('payment_method', '')
        obj.save()
        return redirect('/affpartners/')
    return render(request, 'affpartner_form.html', {'editing': False})


@login_required
def affpartner_edit(request, pk):
    obj = get_object_or_404(AffPartner, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.website = request.POST.get('website', '')
        obj.commission_rate = request.POST.get('commission_rate') or 0
        obj.total_earned = request.POST.get('total_earned') or 0
        obj.total_referrals = request.POST.get('total_referrals') or 0
        obj.status = request.POST.get('status', '')
        obj.joined_date = request.POST.get('joined_date') or None
        obj.payment_method = request.POST.get('payment_method', '')
        obj.save()
        return redirect('/affpartners/')
    return render(request, 'affpartner_form.html', {'record': obj, 'editing': True})


@login_required
def affpartner_delete(request, pk):
    obj = get_object_or_404(AffPartner, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/affpartners/')


@login_required
def referral_list(request):
    qs = Referral.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(partner_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'referral_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def referral_create(request):
    if request.method == 'POST':
        obj = Referral()
        obj.partner_name = request.POST.get('partner_name', '')
        obj.referred_email = request.POST.get('referred_email', '')
        obj.product = request.POST.get('product', '')
        obj.status = request.POST.get('status', '')
        obj.click_date = request.POST.get('click_date') or None
        obj.conversion_date = request.POST.get('conversion_date') or None
        obj.commission = request.POST.get('commission') or 0
        obj.save()
        return redirect('/referrals/')
    return render(request, 'referral_form.html', {'editing': False})


@login_required
def referral_edit(request, pk):
    obj = get_object_or_404(Referral, pk=pk)
    if request.method == 'POST':
        obj.partner_name = request.POST.get('partner_name', '')
        obj.referred_email = request.POST.get('referred_email', '')
        obj.product = request.POST.get('product', '')
        obj.status = request.POST.get('status', '')
        obj.click_date = request.POST.get('click_date') or None
        obj.conversion_date = request.POST.get('conversion_date') or None
        obj.commission = request.POST.get('commission') or 0
        obj.save()
        return redirect('/referrals/')
    return render(request, 'referral_form.html', {'record': obj, 'editing': True})


@login_required
def referral_delete(request, pk):
    obj = get_object_or_404(Referral, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/referrals/')


@login_required
def commission_list(request):
    qs = Commission.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(partner_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'commission_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def commission_create(request):
    if request.method == 'POST':
        obj = Commission()
        obj.partner_name = request.POST.get('partner_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.referral_count = request.POST.get('referral_count') or 0
        obj.period = request.POST.get('period', '')
        obj.status = request.POST.get('status', '')
        obj.paid_date = request.POST.get('paid_date') or None
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/commissions/')
    return render(request, 'commission_form.html', {'editing': False})


@login_required
def commission_edit(request, pk):
    obj = get_object_or_404(Commission, pk=pk)
    if request.method == 'POST':
        obj.partner_name = request.POST.get('partner_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.referral_count = request.POST.get('referral_count') or 0
        obj.period = request.POST.get('period', '')
        obj.status = request.POST.get('status', '')
        obj.paid_date = request.POST.get('paid_date') or None
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/commissions/')
    return render(request, 'commission_form.html', {'record': obj, 'editing': True})


@login_required
def commission_delete(request, pk):
    obj = get_object_or_404(Commission, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/commissions/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['affpartner_count'] = AffPartner.objects.count()
    data['referral_count'] = Referral.objects.count()
    data['commission_count'] = Commission.objects.count()
    return JsonResponse(data)
