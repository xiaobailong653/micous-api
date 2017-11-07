# -*- coding: utf-8 -*-
import json
import tornado.web
from tornado.web import (
    HTTPError,
    gen,
)
from utils.error import (
    DictError,
    MethodNotFind,
)

__author__ = "Sunlf"


class BaseView(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):

        raise MethodNotFind()

    @gen.coroutine
    def post(self, *args, **kwargs):

        raise MethodNotFind()

    @gen.coroutine
    def delete(self, *args, **kwargs):

        raise MethodNotFind()

    @gen.coroutine
    def put(self, *args, **kwargs):

        raise MethodNotFind()

    @gen.coroutine
    def _execute(self, transforms, *args, **kwargs):
        self._transforms = transforms
        try:
            if self.request.method not in self.SUPPORTED_METHODS:
                raise MethodNotFind()
            try:
                result = self.prepare()
                if result is not None:
                    result = yield result
            except DictError as e:
                self.finish(e.dump())
            if self._prepared_future is not None:
                self._prepared_future.set_result(None)
            if self._finished:
                return

            args = [self.decode_argument(arg) for arg in args]
            kwargs = dict((k, self.decode_argument(v, name=k))
                          for (k, v) in kwargs.iteritems())
            if hasattr(self, 'init'):
                getattr(self, 'init')(*args, **kwargs)
            try:
                method = getattr(self, self.request.method.lower())
                result = method(*args, **kwargs)
                if result is not None:
                    yield result
            except DictError as e:
                self.finish(e.dump())

            if self._auto_finish and not self._finished:
                self.finish()
        except Exception, e:
            # 回写异常, 并结束异常请求.
            self._handle_request_exception(e)

    def render(self, chunk=None):
        response = dict(code=1, message="success")
        if chunk:
            response.update(chunk)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish(json.dumps(response))


class UserView(BaseView):
    '''包含当前登陆用户的View.
    '''

    def _session_new(self, user_id):
        session = Session.new(user_id)
        self.set_cookie('session', session, domain="." + HOST,
                        expires_days=SESSION_EXPIRE)

    def _session_rm(self):
        self.clear_cookie('session', domain="." + HOST)
        Session.rm(self.current_user_id)

    def get_current_user(self):
        if self.current_user_id:
            user = User.find_one(dict(user_id=self.current_user_id))
            if user is not None:
                return user
            else:
                self.clear_cookie('session', domain="." + HOST)
                self.current_user_id = 0
                return None

    def login(self, user):
        if user.can_login:
            self._session_new(user.user_id)
        else:
            raise UserDisabled()

    @property
    def current_user_id(self):
        if not hasattr(self, '_current_user_id'):
            s = self.get_cookie('session')
            self._current_user_id = _current_user_id = Session.id_by_b64(s)
            if s and not _current_user_id:
                self.clear_cookie('session', domain="." + HOST)
        return self._current_user_id or 0

    @current_user_id.setter
    def current_user_id(self, value):
        self._current_user_id = value


class LoginView(UserView):
    '''需要用户登陆后才能访问的View.
    '''

    def prepare(self):
        if not self.get_current_user():
            raise LoginRequired()
            # self.redirect('/login')
        super(LoginView, self).prepare()
