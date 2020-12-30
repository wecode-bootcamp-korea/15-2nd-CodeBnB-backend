from django.db import models

class BookMark(models.Model):
    user          = models.ForeignKey("users.User",on_delete=models.CASCADE)
    home          = models.ForeignKey("homes.Home",on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookmarks"
