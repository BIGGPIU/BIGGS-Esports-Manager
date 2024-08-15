from django.db import models

# Create your models here.

from django.db import models


class History(models.Model):
    winner = models.TextField(db_column='Winner', blank=True, null=True)  # Field name made lowercase.
    loser = models.TextField(db_column='Loser', blank=True, null=True)  # Field name made lowercase.
    winnerelo = models.IntegerField(db_column='WinnerElo', blank=True, null=True)  # Field name made lowercase.
    loserelo = models.IntegerField(db_column='LoserElo', blank=True, null=True)  # Field name made lowercase.
    winnerelochange = models.IntegerField(db_column='WinnerEloChange', blank=True, null=True)  # Field name made lowercase.
    loserelochange = models.IntegerField(db_column='LoserEloChange', blank=True, null=True)  # Field name made lowercase.
    gamenumber = models.AutoField(db_column='GameNumber', primary_key=True, blank=True, null=False)  # Field name made lowercase.

    class Meta:
        db_table = 'History'


class Users(models.Model):
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    wins = models.IntegerField(db_column='Wins', blank=True, null=True)  # Field name made lowercase.
    losses = models.IntegerField(db_column='Losses', blank=True, null=True)  # Field name made lowercase.
    elo = models.IntegerField(db_column='ELO', blank=True, null=True)  # Field name made lowercase.
    rival = models.IntegerField(db_column='Rival', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Users'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

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
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

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


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

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