from django.contrib import admin
from .models import AsciiArt

@admin.register(AsciiArt)
class AsciiArtAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'width')
    list_filter = ('created_at', 'width')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def get_readonly_fields(self, request, obj=None):
        """Make the ASCII result field read-only to avoid accidental edits"""
        if obj:  # Editing an existing object
            return self.readonly_fields + ('ascii_result',)
        return self.readonly_fields