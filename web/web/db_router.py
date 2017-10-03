class SS13Router(object):
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to ss13.
        """
        if model._meta.app_label == 'hippie_ss13':
            return 'ss13'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to ss13.
        """
        if model._meta.app_label == 'hippie_ss13':
            return 'ss13'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the ss13 app is involved.
        """
        if obj1._meta.app_label == 'hippie_ss13' or \
           obj2._meta.app_label == 'hippie_ss13':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'hippie_ss13':
            return db == 'ss13'
        return None

class PrimaryRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True