from django.contrib import admin
from .models import AffPartner, Referral, Commission

@admin.register(AffPartner)
class AffPartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "website", "commission_rate", "total_earned", "created_at"]
    list_filter = ["status", "payment_method"]
    search_fields = ["name", "email"]

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ["partner_name", "referred_email", "product", "status", "click_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["partner_name", "referred_email", "product"]

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ["partner_name", "amount", "referral_count", "period", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["partner_name", "period"]
