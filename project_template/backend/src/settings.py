# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateWriteMiddleware, TemplateMiddleware
from gaecookie.middleware import CSRFMiddleware, CSRFInputToDependency
from gaepermission.middleware import LoggedUserMiddleware, PermissionMiddleware
from tekton.gae.middleware.email_errors import EmailMiddleware
from tekton.gae.middleware.json_middleware import JsonResponseMiddleware
from tekton.gae.middleware.parameter import RequestParamsMiddleware
from tekton.gae.middleware.redirect import RedirectMiddleware
from tekton.gae.middleware.router_middleware import RouterMiddleware, ExecutionMiddleware
from tekton.gae.middleware.webapp2_dependencies import Webapp2Dependencies

SENDER_EMAIL = 'renzon@gmail.com'
TEMPLATE_404_ERROR = 'base/404.html'
TEMPLATE_400_ERROR = 'base/400.html'

MIDDLEWARES = [LoggedUserMiddleware,
               TemplateMiddleware,
               EmailMiddleware,
               Webapp2Dependencies,
               RequestParamsMiddleware,
               CSRFInputToDependency,
               RouterMiddleware,
               CSRFMiddleware,
               PermissionMiddleware,
               ExecutionMiddleware,
               TemplateWriteMiddleware,
               JsonResponseMiddleware,
               RedirectMiddleware]


