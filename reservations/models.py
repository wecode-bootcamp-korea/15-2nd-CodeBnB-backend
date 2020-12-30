from django.db    import models

class Guest(models.Model):
    name         = models.CharField(max_length=16)
    description  = models.CharField(max_length=64,null=True)
    
    class Meta:
        db_table = "guests"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "payment_methods"

class Status(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "status"

class Payment(models.Model):
    method          = models.ForeignKey("PaymentMethod",models.SET_NULL,null=True)
    card_number     = models.CharField(max_length=256)
    expire_date     = models.CharField(max_length=256)
    post_code       = models.CharField(max_length=256)
    payment_date    = models.CharField(max_length=256)
    card_holder     = models.CharField(max_length=256)
    total_cost      = models.CharField(max_length=256)

    class Meta:
        db_table = "payments"

class Reservation(models.Model):
    user         = models.ForeignKey("users.User",on_delete=models.CASCADE)
    home         = models.ForeignKey("homes.Home",on_delete=models.CASCADE)
    check_in     = models.DateTimeField(null=True)
    check_out    = models.DateTimeField(null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True,null=True)
    status       = models.ForeignKey("Status",on_delete=models.CASCADE,related_name="reservations")
    payment      = models.OneToOneField("Payment",on_delete=models.SET_NULL,null=True)

    class Meta:
        db_table = "reservations"

class ReservationGuest(models.Model):
    guest        = models.ForeignKey("Guest",on_delete=models.CASCADE)
    reservations = models.ForeignKey("Reservation",on_delete=models.CASCADE)
    count        = models.IntegerField(default=1)

    class Meta:
        db_table = "reservations_guests"

