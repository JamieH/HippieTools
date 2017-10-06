# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from hippie_admin.utils.cache import cache_ckey_callable
from django.utils import timezone

import socket, struct

class Admin(models.Model):
    ckey = models.CharField(max_length=32)
    rank = models.CharField(max_length=32)
    level = models.IntegerField()
    flags = models.IntegerField()
    email = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'

    def get_player(self):
        return Player.objects.get(ckey=self.ckey)

class AdminLog(models.Model):
    datetime = models.DateTimeField()
    adminckey = models.CharField(max_length=32)
    adminip = models.CharField(max_length=18)
    log = models.TextField()

    class Meta:
        managed = False
        db_table = 'admin_log'


class AdminRanks(models.Model):
    rank = models.CharField(max_length=40)
    flags = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_ranks'


class Ban(models.Model):
    bantime = models.DateTimeField()
    server_ip = models.IntegerField()
    server_port = models.SmallIntegerField()
    round_id = models.IntegerField()
    bantype = models.CharField(max_length=14)
    reason = models.CharField(max_length=32768)
    job = models.CharField(max_length=32, blank=True, null=True)
    duration = models.IntegerField()
    expiration_time = models.DateTimeField()
    ckey = models.CharField(max_length=32)
    computerid = models.CharField(max_length=32)
    ip = models.IntegerField()
    a_ckey = models.CharField(max_length=32)
    a_computerid = models.CharField(max_length=32)
    a_ip = models.IntegerField()
    who = models.CharField(max_length=2048)
    adminwho = models.CharField(max_length=2048)
    edits = models.TextField(blank=True, null=True)
    unbanned = models.IntegerField(blank=True, null=True)
    unbanned_datetime = models.DateTimeField(blank=True, null=True)
    unbanned_ckey = models.CharField(max_length=32, blank=True, null=True)
    unbanned_computerid = models.CharField(max_length=32, blank=True, null=True)
    unbanned_ip = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Ban on {} {} by {} on {} for {}".format(self.ckey, self.bantype, self.a_ckey, self.bantime, self.duration)

    def is_expired(self):
        if self.unbanned == 1:
            return True
        if self.get_type() == "PERMA" or self.get_type() == "PERMABAN" or self.get_type() == "JOB_PERMABAN":
            return False
        return self.expiration_time < timezone.now()

    def get_ip(self):
        return socket.inet_ntoa(struct.pack('!L', self.ip))

    def get_what(self):
        if self.bantype == "JOB_TEMPBAN" or self.bantype == "JOB_PERMABAN":
            return self.job
        else:
            return "Server"

    def get_icon(self):
        if self.bantype == "JOB_TEMPBAN" or self.bantype == "JOB_PERMABAN":
            return "fa-briefcase"
        elif self.bantype == "JOB_TEMPBAN":
            return "fa-clock-o"
        elif self.bantype == "PERMA" or self.bantype == "PERMABAN":
            return "fa-ban"

    def get_type(self):
        if self.bantype == "TEMPBAN":
            return "Server (Temporary)"
        elif self.bantype == "JOB_TEMPBAN":
            return "Job (Temporary)"
        elif self.bantype == "JOB_PERMABAN":
            return "Job (Permanent)"
        elif self.bantype == "PERMA" or self.bantype == "PERMABAN":
            return "Server (Permanent)"
        else:
            return "TELL JAMIE"

    def get_css(self):
        if self.is_expired():
            return "bg-success text-white"

        if self.bantype == "TEMPBAN":
            return "warning"
        elif self.bantype == "JOB_TEMPBAN":
            return "bg-warning text-white"
        elif self.bantype == "JOB_PERMABAN":
            return "bg-danger text-white"
        elif self.bantype == "PERMA" or self.bantype == "PERMABAN":
            return "bg-danger text-white"
        else:
            return ""

    class Meta:
        managed = False
        db_table = 'ban'
        ordering = ["-bantime"]


class ConnectionLog(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    server_ip = models.IntegerField()
    server_port = models.SmallIntegerField()
    round_id = models.IntegerField()
    ckey = models.CharField(max_length=45, blank=True, null=True)
    ip = models.IntegerField()
    computerid = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return "Connection from {} on {}".format(self.ckey, self.datetime)

    class Meta:
        managed = False
        db_table = 'connection_log'
        ordering = ["-datetime"]


class Death(models.Model):
    pod = models.CharField(max_length=50)
    x_coord = models.SmallIntegerField()
    y_coord = models.SmallIntegerField()
    z_coord = models.SmallIntegerField()
    mapname = models.CharField(max_length=32)
    server_ip = models.IntegerField()
    server_port = models.SmallIntegerField()
    round_id = models.IntegerField()
    tod = models.DateTimeField()
    job = models.CharField(max_length=32)
    special = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=96)
    byondkey = models.CharField(max_length=32)
    laname = models.CharField(max_length=96, blank=True, null=True)
    lakey = models.CharField(max_length=32, blank=True, null=True)
    bruteloss = models.SmallIntegerField()
    brainloss = models.SmallIntegerField()
    fireloss = models.SmallIntegerField()
    oxyloss = models.SmallIntegerField()
    toxloss = models.SmallIntegerField()
    cloneloss = models.SmallIntegerField()
    staminaloss = models.SmallIntegerField()
    last_words = models.CharField(max_length=255, blank=True, null=True)
    suicide = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'death'


class Feedback(models.Model):
    time = models.DateTimeField()
    round_id = models.IntegerField()
    var_name = models.CharField(max_length=32)
    var_value = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'
        unique_together = (('round_id', 'var_name'),)


class Ipintel(models.Model):
    ip = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    intel = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ipintel'


class LegacyPopulation(models.Model):
    playercount = models.IntegerField(blank=True, null=True)
    admincount = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()
    server_ip = models.IntegerField()
    server_port = models.SmallIntegerField()
    round_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'legacy_population'


class Library(models.Model):
    author = models.CharField(max_length=45)
    title = models.CharField(max_length=45)
    content = models.TextField()
    category = models.CharField(max_length=11)
    ckey = models.CharField(max_length=32)
    datetime = models.DateTimeField()
    deleted = models.IntegerField(blank=True, null=True)
    round_id_created = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'library'


class Memo(models.Model):
    ckey = models.CharField(primary_key=True, max_length=32)
    memotext = models.TextField()
    timestamp = models.DateTimeField()
    last_editor = models.CharField(max_length=32, blank=True, null=True)
    edits = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'memo'
        ordering = ["-timestamp"]

class Mentor(models.Model):
    ckey = models.TextField()

    class Meta:
        managed = False
        db_table = 'mentor'


class MentorMemo(models.Model):
    ckey = models.CharField(primary_key=True, max_length=32)
    memotext = models.TextField()
    timestamp = models.DateTimeField()
    last_editor = models.CharField(max_length=32, blank=True, null=True)
    edits = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mentor_memo'
        ordering = ["-timestamp"]


class Messages(models.Model):
    type = models.CharField(max_length=15)
    targetckey = models.CharField(max_length=32)
    adminckey = models.CharField(max_length=32)
    text = models.CharField(max_length=8192)
    timestamp = models.DateTimeField()
    server = models.CharField(max_length=32, blank=True, null=True)
    server_ip = models.IntegerField()
    server_port = models.SmallIntegerField()
    round_id = models.IntegerField()
    secret = models.IntegerField()
    lasteditor = models.CharField(max_length=32, blank=True, null=True)
    edits = models.TextField(blank=True, null=True)
    deleted = models.IntegerField()

    def get_css(self):
        if self.type == "message":
            return "bg-success text-white"
        elif self.type == "message sent":
            return "bg-success text-white"
        elif self.type == "watchlist entry":
            return "bg-danger text-white"
        elif self.type == "note":
            return "bg-warning"
        else:
            return ""

    class Meta:
        managed = False
        db_table = 'messages'
        ordering = ["-timestamp"]


class Notes(models.Model):
    ckey = models.CharField(max_length=32)
    notetext = models.TextField()
    timestamp = models.DateTimeField()
    adminckey = models.CharField(max_length=32)
    last_editor = models.CharField(max_length=32, blank=True, null=True)
    edits = models.TextField(blank=True, null=True)
    server = models.CharField(max_length=50)
    secret = models.IntegerField()

    def __str__(self):
        return "Note on {} from {} on {}".format(self.ckey, self.adminckey, self.timestamp)

    class Meta:
        managed = False
        db_table = 'notes'
        ordering = ["-timestamp"]


class Player(models.Model):
    ckey = models.CharField(primary_key=True, max_length=32)
    firstseen = models.DateTimeField()
    firstseen_round_id = models.IntegerField()
    lastseen = models.DateTimeField()
    lastseen_round_id = models.IntegerField()
    ip = models.IntegerField()
    computerid = models.CharField(max_length=32)
    lastadminrank = models.CharField(max_length=32)
    accountjoindate = models.DateField(blank=True, null=True)
    flags = models.IntegerField()

    def get_last_ip(self):
        return socket.inet_ntoa(struct.pack('!L', self.ip))

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Player._meta.fields]

    @cache_ckey_callable
    def get_bans(self):
        return Ban.objects.filter(ckey=self.ckey)

    @cache_ckey_callable
    def get_connections(self):
        return ConnectionLog.objects.filter(ckey=self.ckey)

    @cache_ckey_callable
    def get_notes(self):
        return Notes.objects.filter(ckey=self.ckey)

    @cache_ckey_callable
    def get_messages(self):
        return Messages.objects.filter(targetckey=self.ckey)

    @cache_ckey_callable
    def get_rank(self):
        try:
            return Admin.objects.get(ckey=self.ckey).rank
        except Admin.DoesNotExist:
            return "User"

    @cache_ckey_callable
    def get_rank_bg_colour(self):
        rank = self.get_rank()
        colours = {
            'Host': '#FF008F',
            'HeadAdmin': '#5090E0',
            'GameMaster': '#9E5EE2',
            'GameAdmin': '#DFA02F',
            'TrialAdmin': '#C93D3D',
            'Mentor': '#EEE',
            'Coder': '#009900'
        }
        if self.get_rank() not in colours:
            return "#EEE"
        return colours[rank]

    @cache_ckey_callable
    def get_rank_fg_colour(self):
        rank = self.get_rank()
        colours = {
            'Host': '#FFF',
            'HeadAdmin': '#FFF',
            'GameMaster': '#FFF',
            'GameAdmin': '#FFF',
            'TrialAdmin': '#FFF',
            'Mentor': '#444',
            'Coder': '#FFF'
        }
        if self.get_rank() not in colours:
            return "#444"
        return colours[rank]

    @cache_ckey_callable
    def get_rank_icon(self):
        rank = self.get_rank()
        icons = {
            'Host': 'fa-server',
            'HeadAdmin': 'fa-star',
            'GameMaster': 'fa-star-o',
            'GameAdmin': 'fa-dot-circle-o',
            'TrialAdmin': 'fa-gavel',
            'Mentor': 'fa-github',
            'Coder': 'fa-code'
        }
        if rank not in icons:
            return ""
        return icons[rank]

    @cache_ckey_callable
    def get_deaths(self):
        return Death.objects.filter(byondkey=self.ckey)

    @cache_ckey_callable
    def get_role_time(self):
        return RoleTime.objects.filter(ckey=self.ckey)

    @cache_ckey_callable
    def get_watch(self):
        return Watch.objects.filter(ckey=self.ckey)

    @cache_ckey_callable
    def get_cids(self):
        return set(self.get_connections().values_list('computerid', flat=True))

    @cache_ckey_callable
    def get_ips(self):
        ips = set(self.get_connections().values_list('ip', flat=True))
        def fix_ip(ip):
            return socket.inet_ntoa(struct.pack('!L', ip))
        return list(map(fix_ip, ips))

    class Meta:
        managed = False
        db_table = 'player'
        ordering = ["-lastseen"]


class PollOption(models.Model):
    pollid = models.IntegerField()
    text = models.CharField(max_length=255)
    minval = models.IntegerField(blank=True, null=True)
    maxval = models.IntegerField(blank=True, null=True)
    descmin = models.CharField(max_length=32, blank=True, null=True)
    descmid = models.CharField(max_length=32, blank=True, null=True)
    descmax = models.CharField(max_length=32, blank=True, null=True)
    default_percentage_calc = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'poll_option'


class PollQuestion(models.Model):
    polltype = models.CharField(max_length=11)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    question = models.CharField(max_length=255)
    adminonly = models.IntegerField()
    multiplechoiceoptions = models.IntegerField(blank=True, null=True)
    createdby_ckey = models.CharField(max_length=32, blank=True, null=True)
    createdby_ip = models.IntegerField()
    dontshow = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'poll_question'


class PollTextreply(models.Model):
    datetime = models.DateTimeField()
    pollid = models.IntegerField()
    ckey = models.CharField(max_length=32)
    ip = models.IntegerField()
    replytext = models.CharField(max_length=2048)
    adminrank = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'poll_textreply'


class PollVote(models.Model):
    datetime = models.DateTimeField()
    pollid = models.IntegerField()
    optionid = models.IntegerField()
    ckey = models.CharField(max_length=32)
    ip = models.IntegerField()
    adminrank = models.CharField(max_length=32)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'poll_vote'


class Privacy(models.Model):
    datetime = models.DateTimeField()
    ckey = models.CharField(max_length=32)
    option = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'privacy'


class RoleTime(models.Model):
    ckey = models.CharField(primary_key=True, max_length=32)
    job = models.CharField(max_length=128)
    minutes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'role_time'
        unique_together = (('ckey', 'job'),)


class Round(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    server_ip = models.IntegerField()
    server_port = models.SmallIntegerField()
    commit_hash = models.CharField(max_length=40, blank=True, null=True)
    game_mode = models.CharField(max_length=32, blank=True, null=True)
    game_mode_result = models.CharField(max_length=64, blank=True, null=True)
    end_state = models.CharField(max_length=64, blank=True, null=True)
    shuttle_name = models.CharField(max_length=64, blank=True, null=True)
    map_name = models.CharField(max_length=32, blank=True, null=True)
    station_name = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'round'


class SchemaRevision(models.Model):
    major = models.IntegerField(primary_key=True)
    minor = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'schema_revision'
        unique_together = (('major', 'minor'),)


class SpoofCheck(models.Model):
    whitelist = models.IntegerField()
    ckey = models.CharField(max_length=32)
    computerid_1 = models.CharField(max_length=32)
    computerid_2 = models.CharField(max_length=32, blank=True, null=True)
    computerid_3 = models.CharField(max_length=32, blank=True, null=True)
    datetime_1 = models.DateTimeField()
    datetime_2 = models.DateTimeField(blank=True, null=True)
    datetime_3 = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spoof_check'


class Watch(models.Model):
    ckey = models.CharField(primary_key=True, max_length=32)
    reason = models.TextField()
    timestamp = models.DateTimeField()
    adminckey = models.CharField(max_length=32)
    last_editor = models.CharField(max_length=32, blank=True, null=True)
    edits = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'watch'


class WebAudit(models.Model):
    ckey = models.CharField(max_length=50, blank=True, null=True)
    rank = models.CharField(max_length=50, blank=True, null=True)
    action = models.CharField(max_length=200, blank=True, null=True)
    ip = models.CharField(max_length=200, blank=True, null=True)
    date_time = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'web_audit'