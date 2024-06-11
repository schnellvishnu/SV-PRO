class CheckerRouter:
                    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'masterapp':
            return 'Db8'
        elif model._meta.app_label == 'accounts':
            return 'Db8'
        # elif model._meta.app_label == 'serverdataapp':
        #     return 'Line_DB1'
        # elif model._meta.app_label == 'serverdataapp':
        #     return 'Line_DB1'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'masterapp':
            return 'Db8'
        elif model._meta.app_label == 'accounts':
                return 'Db8'
        # elif model._meta.app_label == 'serverdataapp':
        #     return 'Line_DB1'
        
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'masterapp' or obj2._meta.app_label == 'masterapp':
            return True
        elif 'masterapp' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        elif obj1._meta.app_label == 'accounts' or obj2._meta.app_label == 'accounts':
                                return True
        elif 'accounts' not in [obj1._meta.app_label, obj2._meta.app_label]:
                                return True
        # elif obj1._meta.app_label == 'serverdataapp' or obj2._meta.app_label == 'serverdataapp':
        #                         return True
        # elif 'serverdataapp' not in [obj1._meta.app_label, obj2._meta.app_label]:
        #     return True
        
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'masterapp':
            return db == 'Db8'
        elif app_label == 'accounts':
                                return db == 'Db8'
        # elif app_label == 'serverdataapp':
        #     return db == 'Line_DB1'
        # elif app_label == 'localapp':
        #     return db == 'Line_DB1'
       
        return None