from django.contrib import admin
from django.utils.html import format_html
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ('titre', 'auteur', 'statut', 'date_publication', 'apercu_image')
    list_filter = ('statut', 'date_publication')
    search_fields = ('titre', 'contenu')
    list_editable = ('statut',)
    ordering = ('-date_publication',)

    def apercu_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:4px;" />',
                obj.image.url
            )
        return "—"
    apercu_image.short_description = "Image"


admin.site.site_header = "Administration du Blog"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Tableau de bord"