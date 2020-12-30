from django.db    import models

class HomeType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "home_types"

class BuildingType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "building_types"

class Region(models.Model):
    name                  = models.CharField(max_length=16)
    latitude              = models.DecimalField(max_digits=9, decimal_places=6, default=127.03130)
    longitude             = models.DecimalField(max_digits=9, decimal_places=6, default=37.30225)
    zoom_level            = models.IntegerField(default=13)
    around_radius_m       = models.IntegerField()

    class Meta:
        db_table = "regions"

class Bed(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "beds"

class RuleType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "rule_types"

class FacilityType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "facility_types"

class PriceCategory(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "price_categories"

class Home(models.Model):
    name                = models.CharField(max_length=256)
    capacity_guest      = models.IntegerField(default=1)
    description         = models.TextField()
    address             = models.CharField(max_length=64)
    home_type           = models.ForeignKey("HomeType",on_delete=models.SET_NULL,null=True)
    building_type       = models.ForeignKey("BuildingType",on_delete=models.SET_NULL,null=True)
    region              = models.ForeignKey("Region",on_delete=models.SET_DEFAULT,default=1)
    latitude            = models.DecimalField(max_digits=9, decimal_places=6, default=127.03130)
    longitude           = models.DecimalField(max_digits=9, decimal_places=6, default=37.30225)
    rule                = models.ManyToManyField("Rule",through="HomeRule")
    option              = models.ManyToManyField("Option",through="HomeOpiton")
    facility            = models.ManyToManyField("Facility",through="HomeFacility")
    price               = models.ManyToManyField("PriceCategory",through="HomePrice")
    reviewer            = models.ManyToManyField("users.User",through="Review",related_name="reviewed_homes")
    
    class Meta:
        db_table = "homes"

class HomeImage(models.Model):
    home                = models.ForeignKey("Home",on_delete=models.CASCADE,related_name="images")
    url                 = models.URLField()

    class Meta:
        db_table = "home_images"
    
class Option(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "options"

class Facility(models.Model):
    name                = models.CharField(max_length=64)
    facility_type       = models.ForeignKey("FacilityType",on_delete=models.CASCADE)

    class Meta:
        db_table = "facilities"

class Rule(models.Model):
    name                = models.CharField(max_length=64)
    rule_type           = models.ForeignKey("RuleType",on_delete=models.CASCADE)

    class Meta:
        db_table = "rules"

class HomePrice(models.Model):
    home                = models.ForeignKey("Home",on_delete=models.CASCADE)
    price_category      = models.ForeignKey("PriceCategory",on_delete=models.CASCADE)
    cost                = models.IntegerField()

    class Meta:
        db_table = "homes_prices"

class HomeFacility(models.Model):
    home                = models.ForeignKey("Home",on_delete=models.CASCADE)
    facility            = models.ForeignKey("Facility",on_delete=models.CASCADE)
    description         = models.CharField(max_length=128,null=True)

    class Meta:
        db_table = "home_facilities"

class HomeOpiton(models.Model):
    home              = models.ForeignKey("Home",on_delete=models.CASCADE)
    option            = models.ForeignKey("Option",on_delete=models.CASCADE)
    count             = models.IntegerField(default=1)

    class Meta:
        db_table = "homes_options"

class HomeRule(models.Model):
    home              = models.ForeignKey("Home",on_delete=models.CASCADE)
    rule              = models.ForeignKey("Rule",on_delete=models.CASCADE)
    check_in          = models.TimeField(null=True)
    check_out         = models.TimeField(null=True)
    description       = models.CharField(max_length=128,null=True)
    
    class Meta:
        db_table = "homes_rules"

class HomeRoom(models.Model):
    home    = models.ForeignKey("Home",on_delete=models.CASCADE,related_name="rooms")
    name    = models.CharField(max_length=128)

    class Meta:
        db_table = "homes_rooms"

class RoomBed(models.Model):
    home_room   = models.ForeignKey("HomeRoom",on_delete=models.CASCADE)
    bed         = models.ForeignKey("Bed",on_delete=models.CASCADE)
    count       = models.IntegerField(default=1)
    
    class Meta:
        db_table = "rooms_beds"

class Review(models.Model):
    home        = models.ForeignKey("Home",on_delete=models.CASCADE)
    user        = models.ForeignKey("users.User",on_delete=models.CASCADE)
    contents    = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True,null=True)
    rating      = models.IntegerField(default=1)

    class Meta:
        db_table = "reviews"

