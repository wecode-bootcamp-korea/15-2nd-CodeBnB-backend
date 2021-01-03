from django.urls    import path
from bookmarks.views    import BookmarkListView, BookmarkView

urlpatterns = [
        path('/<int:home_pk>', BookmarkView.as_view()),
        path('', BookmarkListView.as_view())
]
