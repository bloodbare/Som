# encoding: utf-8
"""
login.py

Created by Victor Fernandez de Alba on 2010-11-18.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized

from pyramid.view import view_config
from pyramid.url import model_url

from pyramid.security import remember
from pyramid.security import forget

from prova.security import USERS

@view_config(name='login', renderer='templates/login.pt')
def login(request):
    login_url = model_url(request.context, request, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    
    plugins = request.environ.get('repoze.who.plugins', {})
    auth_tkt = plugins.get('auth_tkt')
        
    login_counter = request.environ['repoze.who.logins']
    if login_counter > 0:
        display_message("Wrong credentials", status="error")
    came_from = request.params.get("came_from") or "/"
    
    if request.params.get('form.submitted', None) is not None:
        login = request.POST.get('login')
        password = request.POST.get('password')
        if login is None or password is None:
            return HTTPFound(location='%s/login.html'
                                        % request.application_url)
        credentials = {'login': login, 'password': password}
        max_age = request.POST.get('max_age')
        if max_age is not None:
            credentials['max_age'] = int(max_age)

        # authenticate
        authenticators = filter(None, 
                                [plugins.get(name)
                                   for name in ['zodb', 'zodb_impersonate']])
                                   
        userid = None
        if authenticators:
           reason = 'Bad username or password'
        else:
           reason = 'No authenticatable users'

        for plugin in authenticators:
           userid = plugin.authenticate(request.environ, credentials)
           if userid:
               break

        # if not successful, try again
        if not userid:
           challenge_qs['reason'] = reason
           return HTTPFound(location='%s/login.html?%s'
                            % (request.application_url, 
                               urlencode(challenge_qs, doseq=True)))

        # else, remember
        credentials['repoze.who.userid'] = userid
        if auth_tkt is not None:
           remember_headers = auth_tkt.remember(request.environ, credentials)
        else:
           remember_headers = []

        # log the time on the user's profile.
        #       profiles = find_profiles(context)
        #       if profiles is not None:
        #           profile = profiles.get(userid)
        #           if profile is not None:
        #               profile.last_login_time = datetime.utcnow()

        # and redirect
        return HTTPFound(headers=remember_headers, location=came_from)
        
    
    return render("login", login_counter=login_counter, came_from=came_from)
    
# def login(request):
#     login_url = model_url(request.context, request, 'login')
#     referrer = request.url
#     if referrer == login_url:
#         referrer = '/' # never use the login form itself as came_from
#     came_from = request.params.get('came_from', referrer)
#     message = ''
#     login = ''
#     password = ''
#     if 'form.submitted' in request.params:
#         login = request.params['login']
#         password = request.params['password']
#         if USERS.get(login) == password:
#             headers = remember(request, login)
#             return HTTPFound(location = came_from,
#                              headers = headers)
#         message = 'Failed login'
# 
#     return dict(
#         message = message,
#         url = request.application_url + '/login',
#         came_from = came_from,
#         login = login,
#         password = password,
#         )
    
@view_config(name='logout')
def logout(request, reason='Logged out'):
    unauthorized = HTTPUnauthorized()
    unauthorized.headerlist.append(
        ('X-Authorization-Failure-Reason', reason))
    return unauthorized
    
    # headers = forget(request)
    # return HTTPFound(location = model_url(request.context, request),
    #                  headers = headers)