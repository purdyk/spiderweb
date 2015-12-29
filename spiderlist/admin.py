from django.contrib import admin

# Register your models here.

from .models import SearchGroup
from .models import SearchResult
from .models import Report
from .models import MatchedFile

admin.site.register(SearchGroup)
admin.site.register(SearchResult)
admin.site.register(Report)
admin.site.register(MatchedFile)
