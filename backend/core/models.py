from django.db import models

class AffPartner(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    website = models.URLField(blank=True, default="")
    commission_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_referrals = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("pending", "Pending"), ("suspended", "Suspended")], default="active")
    joined_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[("bank", "Bank"), ("paypal", "PayPal"), ("upi", "UPI")], default="bank")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Referral(models.Model):
    partner_name = models.CharField(max_length=255)
    referred_email = models.EmailField(blank=True, default="")
    product = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("converted", "Converted"), ("rejected", "Rejected")], default="pending")
    click_date = models.DateField(null=True, blank=True)
    conversion_date = models.DateField(null=True, blank=True)
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.partner_name

class Commission(models.Model):
    partner_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    referral_count = models.IntegerField(default=0)
    period = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("approved", "Approved"), ("paid", "Paid")], default="pending")
    paid_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.partner_name
