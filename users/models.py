from django.db    import models
from homes.models import Home

class User(models.Model):
    last_name           = models.CharField(max_length=16)
    first_name          = models.CharField(max_length=32)
    email               = models.EmailField()
    password            = models.CharField(max_length=256)
    birthday            = models.DateField()
    mailing_check       = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    profile_image       = models.URLField(default="https://i0.wp.com/prikachi.com/wp-content/uploads/2020/07/DPP1.jpg",max_length=512)
    bookmarks           = models.ManyToManyField("homes.Home",through="bookmarks.Bookmark",related_name="bookmark_users")

    class Meta:
        db_table = "users"

class Host(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_host")
    home            = models.ForeignKey(Home,on_delete=models.CASCADE,related_name="home_host")
    contact         = models.CharField(max_length=32)
    is_valid        = models.BooleanField(default=False)
    description     = models.TextField()
    commission_date = models.DateTimeField(auto_now_add=True)
    is_superhost    = models.BooleanField(default=False)

    class Meta:
        db_table = "hosts"

