from django.contrib import admin

from note.models import Note, Category


class NoteAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title', )} 


admin.site.register(Note, NoteAdmin)
admin.site.register(Category)