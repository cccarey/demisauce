#!/usr/bin/env python
import logging
import urllib
from pylons import config
from formencode import Invalid, validators
from formencode.validators import *
import formencode
import webhelpers.paginate

from demisauce.lib import helpers as h

from demisauce.lib.base import *
from demisauce import model
from demisauce.model import meta, mapping
from demisauce.model.person import Person
from demisauce.model.site import Site
from demisauce.model.group import Group

log = logging.getLogger(__name__)

class GroupFormValidation(formencode.Schema):
    """Form validation for the comment web admin"""
    allow_extra_fields = True
    filter_extra_fields = False
    name = formencode.All(String(not_empty=True))

class GroupadminController(SecureController):
    def index(self):
        return self.viewlist()
    
    def ajaxget(self,id=''):
        pl = meta.DBSession.query(Person).all()
        s = ''
        for p in pl:
            s += "%s|%s\n" % (p.displayname,p.email)
        return s
    
    def jsonac(self):
        """gets list of users for autocomplete"""
        pass
    
    def viewlist(self,id=0):
        c.item = None
        filter = 'all'
        if 'filter' in request.params:
            filter = request.params['filter']
        c.groups = Group.by_site(c.user.site_id)
        temp = """
        page = 1
        if 'page' in request.params:
            page = int(request.params['page'])
        c.groups = webhelpers.paginate.Page(
                Group.by_site(c.user.site_id),
                page=page,items_per_page=5)
                
        ${h.dspager(c.groups)}
        """
        c.groups = h.dspager(c.groups)
        
        return render('/group/group_admin.html')
    
    def view(self,id=0):
        c.item = Group.get(c.user.site_id,id)
        if not c.item or not c.item.site_id == c.user.site_id:
            c.item = None
        return render('/group/group_view.html')
    
    @rest.dispatch_on(POST="group_submit")
    def addedit(self,id=0):
        return self.viewlist(id)
    
    @validate(schema=GroupFormValidation(), form='addedit')
    def group_submit(self,id=''):
        g = None
        if 'group_id' in self.form_result and self.form_result['group_id'] != '0':
            g = Group.get(c.user.site_id,int(self.form_result['group_id']))
        else:
            g = Group(c.user.site_id)
        g.name = self.form_result['name']
        #print self.form_result['members']
        newtogroup, newtosite = g.add_memberlist(self.form_result['members'])
        g.save()
        #return 'newtogroup= %s,  \n newtosite=%s' % (newtogroup, newtosite)
        return redirect_wsave('/groupadmin')
        
    
    @rest.dispatch_on(POST="group_popup_submit")
    def popup(self,id=0):
        return render('/group/group_popup.html')
    
    def popup_view(self,id=0):
        c.item = Group.get(c.user.site_id,id)
        if not c.item.site_id == c.user.site_id:
            c.item = None
        return render('/group/group_popupview.html')
    
    @validate(schema=GroupFormValidation(), form='popup')
    def group_popup_submit(self,id=''):
        g = None
        if 'group_id' in self.form_result and self.form_result['group_id'] != '0':
            g = Group.get(c.user.site_id,int(self.form_result['group_id']))
        else:
            g = Group(c.user.site_id)
        g.name = self.form_result['name']
        newtogroup, newtosite = g.add_memberlist(self.form_result['members'])
        g.save()
        #return 'newtogroup= %s,  \n newtosite=%s' % (newtogroup, newtosite)
        return redirect_wsave('/groupadmin/popup_view/%s' % g.id)
    
    def edit(self,id=0):
        c.item = Group.get(c.user.site_id,id)
        if not c.item or not c.item.site_id == c.user.site_id:
            c.item = None
        return render('/group/group_edit.html')
    
