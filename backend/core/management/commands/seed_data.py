from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import AffPartner, Referral, Commission
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusAffiliate with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusaffiliate.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if AffPartner.objects.count() == 0:
            for i in range(10):
                AffPartner.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    website=f"https://example.com/{i+1}",
                    commission_rate=round(random.uniform(1000, 50000), 2),
                    total_earned=round(random.uniform(1000, 50000), 2),
                    total_referrals=random.randint(1, 100),
                    status=random.choice(["active", "pending", "suspended"]),
                    joined_date=date.today() - timedelta(days=random.randint(0, 90)),
                    payment_method=random.choice(["bank", "paypal", "upi"]),
                )
            self.stdout.write(self.style.SUCCESS('10 AffPartner records created'))

        if Referral.objects.count() == 0:
            for i in range(10):
                Referral.objects.create(
                    partner_name=f"Sample Referral {i+1}",
                    referred_email=f"demo{i+1}@example.com",
                    product=f"Sample {i+1}",
                    status=random.choice(["pending", "converted", "rejected"]),
                    click_date=date.today() - timedelta(days=random.randint(0, 90)),
                    conversion_date=date.today() - timedelta(days=random.randint(0, 90)),
                    commission=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 Referral records created'))

        if Commission.objects.count() == 0:
            for i in range(10):
                Commission.objects.create(
                    partner_name=f"Sample Commission {i+1}",
                    amount=round(random.uniform(1000, 50000), 2),
                    referral_count=random.randint(1, 100),
                    period=f"Sample {i+1}",
                    status=random.choice(["pending", "approved", "paid"]),
                    paid_date=date.today() - timedelta(days=random.randint(0, 90)),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Commission records created'))
