from django.contrib import admin

from .models import (
    Category,
    Tag,
    Book,
    Review,
    ReviewTag,
    Selection,
)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)



class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('author', 'title', 'rating', 'created_at')
    readonly_fields = ('created_at',)



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ReviewInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'book',
        'author',
        'rating',
        'created_at',
    )
    list_filter = ('rating', 'created_at')
    search_fields = (
        'title',
        'content',
        'book__title',
        'author__user__username',
    )
    raw_id_fields = ('book', 'author')
    readonly_fields = ('created_at', 'updated_at')



@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = ('review', 'tag')
    search_fields = ('review__title', 'tag__name')


@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('books',)
