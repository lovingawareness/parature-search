# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Customer(models.Model):
    alternate_phone = models.TextField(blank=True, null=True)
    building = models.TextField(blank=True, null=True)
    cell_phone = models.TextField(blank=True, null=True)
    class_year = models.TextField(blank=True, null=True)
    customer_feedback = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    find_group = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    home_office = models.TextField(blank=True, null=True)
    klp_participant = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    netid = models.TextField(blank=True, null=True)
    office_media = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    password_confirm = models.TextField(blank=True, null=True)
    preferred_number = models.TextField(blank=True, null=True)
    program = models.TextField(blank=True, null=True)
    receive_email_updates_for_tickets = models.TextField(blank=True, null=True)
    retiredcustomerfielddonotuse01 = models.TextField(blank=True, null=True)
    retiredcustomerfielddonotuse02 = models.TextField(blank=True, null=True)
    room = models.TextField(blank=True, null=True)
    section_number = models.TextField(blank=True, null=True)
    service_level_agreement = models.TextField(blank=True, null=True)
    signed_tsa = models.TextField(blank=True, null=True)
    signed_tsa_date = models.TextField(blank=True, null=True)
    special_interest = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    customerid = models.IntegerField(unique=True, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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


class TicketDetails(models.Model):
    app_tag_or_name = models.TextField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    customer_service = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    extra_action = models.TextField(blank=True, null=True)
    faculty_netid = models.TextField(blank=True, null=True)
    known_error_notes_and_workaround = models.TextField(blank=True, null=True)
    loaner_purpose = models.TextField(blank=True, null=True)
    operating_system = models.TextField(blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    overall = models.TextField(blank=True, null=True)
    pilot_or_project = models.TextField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)
    problem_analysis = models.TextField(blank=True, null=True)
    problem_flags = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    room_or_area = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    service_detail = models.TextField(blank=True, null=True)
    service_family = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    student_migration_tracker = models.TextField(blank=True, null=True)
    submitted_by = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    supported = models.TextField(blank=True, null=True)
    ticket_product = models.TextField(blank=True, null=True)
    technical_support = models.TextField(blank=True, null=True)
    ticket_location = models.TextField(blank=True, null=True)
    ticket_origin = models.TextField(blank=True, null=True)
    ticket_request_type = models.TextField(blank=True, null=True)
    timeliness = models.TextField(blank=True, null=True)
    accountname = models.TextField(blank=True, null=True)
    amid = models.TextField(blank=True, null=True)
    assignedto = models.TextField(blank=True, null=True)
    createdby = models.TextField(blank=True, null=True)
    customeremail = models.TextField(blank=True, null=True)
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customerid', blank=True, null=True)
    datecreated = models.DateTimeField(blank=True, null=True)
    dateupdated = models.DateTimeField(blank=True, null=True)
    hoursspent = models.TextField(blank=True, null=True)
    sla = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    ticketid = models.IntegerField(unique=True, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'ticket_details'


class TicketHistory(models.Model):
    action_date = models.DateTimeField(blank=True, null=True)
    action_name = models.TextField(blank=True, null=True)
    assigned_to_csr = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    performed_by_csr = models.TextField(blank=True, null=True)
    ticket = models.ForeignKey(TicketDetails, models.DO_NOTHING, blank=True, null=True)
    time_spent = models.TextField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'ticket_history'
