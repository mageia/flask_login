
from leancloud import User, Query, Object


def get_user(uid):
    query = Query(Object.extend('User'))
    query.equal_to('objectId', uid)
    return query.find()[0] if query.count() else None


def is_authenticated():
    return True


def is_active():
    return True


def is_anonymous():
    return False


def get_id(self):
    return unicode(self.id)


User.get_user = staticmethod(get_user)
User.get_user = staticmethod(is_authenticated)
User.get_user = staticmethod(is_active)
User.get_user = staticmethod(is_anonymous)
User.get_user = classmethod(get_id)
