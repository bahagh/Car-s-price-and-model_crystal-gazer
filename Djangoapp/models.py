# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CoreUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=200)
    email = models.CharField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.BigIntegerField(unique=True)
    is_active = models.BooleanField()
    is_staff = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Core_user'


class CoreUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Core_user_groups'
        unique_together = (('user', 'group'),)


class CoreUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Core_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AdminInterfaceTheme(models.Model):
    name = models.CharField(unique=True, max_length=50)
    active = models.BooleanField()
    title = models.CharField(max_length=50)
    title_visible = models.BooleanField()
    logo = models.CharField(max_length=100)
    logo_visible = models.BooleanField()
    css_header_background_color = models.CharField(max_length=10)
    title_color = models.CharField(max_length=10)
    css_header_text_color = models.CharField(max_length=10)
    css_header_link_color = models.CharField(max_length=10)
    css_header_link_hover_color = models.CharField(max_length=10)
    css_module_background_color = models.CharField(max_length=10)
    css_module_text_color = models.CharField(max_length=10)
    css_module_link_color = models.CharField(max_length=10)
    css_module_link_hover_color = models.CharField(max_length=10)
    css_module_rounded_corners = models.BooleanField()
    css_generic_link_color = models.CharField(max_length=10)
    css_generic_link_hover_color = models.CharField(max_length=10)
    css_save_button_background_color = models.CharField(max_length=10)
    css_save_button_background_hover_color = models.CharField(max_length=10)
    css_save_button_text_color = models.CharField(max_length=10)
    css_delete_button_background_color = models.CharField(max_length=10)
    css_delete_button_background_hover_color = models.CharField(max_length=10)
    css_delete_button_text_color = models.CharField(max_length=10)
    list_filter_dropdown = models.BooleanField()
    related_modal_active = models.BooleanField()
    related_modal_background_color = models.CharField(max_length=10)
    related_modal_rounded_corners = models.BooleanField()
    logo_color = models.CharField(max_length=10)
    recent_actions_visible = models.BooleanField()
    favicon = models.CharField(max_length=100)
    related_modal_background_opacity = models.CharField(max_length=5)
    env_name = models.CharField(max_length=50)
    env_visible_in_header = models.BooleanField()
    env_color = models.CharField(max_length=10)
    env_visible_in_favicon = models.BooleanField()
    related_modal_close_button_visible = models.BooleanField()
    language_chooser_active = models.BooleanField()
    language_chooser_display = models.CharField(max_length=10)
    list_filter_sticky = models.BooleanField()
    form_pagination_sticky = models.BooleanField()
    form_submit_sticky = models.BooleanField()
    css_module_background_selected_color = models.CharField(max_length=10)
    css_module_link_selected_color = models.CharField(max_length=10)
    logo_max_height = models.SmallIntegerField()
    logo_max_width = models.SmallIntegerField()
    foldable_apps = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'admin_interface_theme'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class ListingAnalyser(models.Model):
    id = models.BigAutoField(primary_key=True)
    marque = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    prix = models.IntegerField()
    puissance_fiscale = models.IntegerField()
    mise_en_circulation = models.IntegerField()
    kilometrage = models.IntegerField()
    carburant = models.CharField(max_length=100)
    boite_vitesse = models.CharField(max_length=100)
    gouvernorat = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'listing_analyser'


class ListingListing(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.IntegerField()
    title = models.CharField(max_length=100)
    make = models.CharField(db_column='Make', max_length=100)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=100)  # Field name made lowercase.
    mileage = models.IntegerField(db_column='Mileage')  # Field name made lowercase.
    fuel = models.CharField(db_column='Fuel', max_length=100)  # Field name made lowercase.
    engine_horsepower = models.IntegerField(db_column='Engine_Horsepower')  # Field name made lowercase.
    governorate = models.CharField(db_column='Governorate', max_length=100)  # Field name made lowercase.
    number_of_seats = models.IntegerField(db_column='Number_of_seats')  # Field name made lowercase.
    doors = models.IntegerField(db_column='Doors')  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=100)  # Field name made lowercase.
    vehicle_description = models.TextField(db_column='Vehicle_description')  # Field name made lowercase.
    vehicle_extras = models.TextField(db_column='Vehicle_extras')  # Field name made lowercase.
    address = models.CharField(max_length=100)
    transmission = models.CharField(db_column='Transmission', max_length=100)  # Field name made lowercase.
    phone_number = models.IntegerField(db_column='Phone_number')  # Field name made lowercase.
    photo_main = models.CharField(max_length=100)
    photo_1 = models.CharField(max_length=100)
    photo_2 = models.CharField(max_length=100)
    photo_3 = models.CharField(max_length=100)
    photo_4 = models.CharField(max_length=100)
    photo_5 = models.CharField(max_length=100)
    photo_6 = models.CharField(max_length=100)
    is_published = models.BooleanField()
    list_date = models.DateField()
    owner = models.ForeignKey(CoreUser, models.DO_NOTHING)
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    vehicle_extras_interior = models.TextField(db_column='Vehicle_extras_Interior')  # Field name made lowercase.
    vehicle_extras_safety = models.TextField(db_column='Vehicle_extras_Safety')  # Field name made lowercase.
    predictedprice = models.IntegerField(db_column='Predictedprice')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'listing_listing'


class ListingReviewrating(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.FloatField()
    ip = models.CharField(max_length=20)
    status = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    car = models.ForeignKey(ListingListing, models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'listing_reviewrating'
