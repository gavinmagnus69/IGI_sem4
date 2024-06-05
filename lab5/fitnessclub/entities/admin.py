from django.contrib import admin
from .models import * 
# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'create_date', 'update_date', 'local_create_date', 'local_update_date')

@admin.register(Projectile)
class ProjectileAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('hall_name','id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'local_create_date', 'local_update_date')