#!/usr/bin/env python
import logging
import urllib
from pylons import config
from formencode import Invalid, validators
from formencode.validators import *
import formencode
import simplejson

from demisauce.lib.base import *
from demisauce import model
from demisauce.model import meta, mapping
from demisauce.model.person import Person
from demisauce.model.site import Site
from demisauce.model.help import Help
from demisauce.model.cms import Cmsitem
from demisauce.model.rating import Rating

log = logging.getLogger(__name__)

def make_restful(func):
    """??"""
    def wrapper(*arg):
        return func.inner1
    return wrapper

class HelpFormValidation(formencode.Schema):
    """Form validation for the comment web admin"""
    allow_extra_fields = True
    filter_extra_fields = False
    #authorname = formencode.All(String(not_empty=True))
    email = formencode.All(String(not_empty=True))
    content = formencode.All(String(not_empty=True))

class HelpController(BaseController):
    def index(self):
        data = {'success':True,'help_id':1,'html':render('/help/help.html')}
        json = simplejson.dumps(data)
        #response.headers['Content-Type'] = 'text/json'
        return '[%s]' % (json)
    
    def feedback_service(self,id=None):
        return render('/help/help_badge.html')
    
    def ratearticle(self,id=''):
        site = Site.by_slug(str(id))
        data = {'success':False}
        if site and 'resource_id' in request.params:
            userid = 0
            #TODO:  add rating_ct to ??? (context?  help?  cms?)
            displayname = 'anonymous'
            if c.user:
                userid = c.user.id
                displayname = c.user.displayname
            rating_val = int(request.params['rating'])
            r = Rating(userid,'/ds/help/article',rating_val,sanitize(request.params['resource_id']),displayname)
            r.save()
            data = {'success':True,'html':r.id}
        json = simplejson.dumps(data)
        response.headers['Content-Type'] = 'text/json'
        return '%s(%s)' % (request.params['jsoncallback'],json)
    
    @rest.dispatch_on(POST="feedbackform")
    def feedback(self,id):
        site = Site.by_slug(str(id))
        if site:
            c.site_slug = site.slug
        if 'url' in request.params:
            c.current_url = request.params['url']
        c.category = 'help'
        if 'category' in request.params:
            c.category = sanitize(request.params['category'])
        c.isblue = True
        return render('/help/help_feedback.html')
    
    @rest.dispatch_on(POST="feedbackform")
    def submitfeedback(self,id):
        site = Site.by_slug(str(id))
        if site:
            c.site_slug = site.slug
        if 'url' in request.params:
            c.current_url = request.params['url']
        c.hasheader = True
        c.isblue = False
        return render('/help/help_feedback.html')
    
    @validate(schema=HelpFormValidation(), form='feedback')
    def feedbackform(self,id=''):
        site = Site.by_slug(str(id))
        if site:
            c.site = site
            help = Help(site_id=site.id,email=sanitize(self.form_result['email']))
            if c.user:
                help.set_user_info(c.user)
            else:
                if 'authorname' in self.form_result:
                    help.authorname = sanitize(self.form_result['authorname'])
                if 'blog' in self.form_result:
                    help.blog = sanitize(self.form_result['blog'])
                if help.blog == "your blog url":
                    help.blog = ''
            if 'category' in self.form_result:
                help.category = sanitize(self.form_result['category'])
            help.url = sanitize(self.form_result['url'])
            help.content = sanitize(self.form_result['content'])
            if 'HTTP_X_FORWARDED_FOR' in request.environ:
                help.ip = request.environ['HTTP_X_FORWARDED_FOR']
            elif 'REMOTE_ADDR' in request.environ:
                help.ip = request.environ['REMOTE_ADDR']
            help.save()
            if 'goto' in request.POST and len(request.POST['goto']) > 5:
                c.goto_url = request.POST['goto']
                return render('/refresh.html')
            else:
                c.result = True
                return render('/help/help_feedback.html')
            
        else:
            log.error('feedback from came in with no site id=%s, params= %s' % (id,request.params))
        return render('/help/help_feedback.html')
    

