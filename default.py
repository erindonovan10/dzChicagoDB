# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def index():
    events=db().select(db.events_info.ALL)
    levels=db().select(db.membership_level.ALL)
    spotlights=db().select(orderby=~ db.sister_spotlight.id, limitby=(0,1))
    return dict(events=events, levels=levels, spotlights=spotlights)

def download():
    return response.download(request, db)

def about_us():
    return dict()

def exec_board():
    return dict()

def sister_spotlight():
    spotlights = db().select(db.sister_spotlight.ALL)
    return dict(spotlights=spotlights)

def college():
    news=db().select(db.collegiate_news.ALL, db.schools.ALL, left=db.collegiate_news.on(db.collegiate_news.school == db.schools.id))
    return dict(news=news)

def login():
    return dict()

def rec_member():
    return dict()

def contact_us():
    newsletters=db().select(db.newsletters.ALL)
    return dict(newsletters=newsletters)

@auth.requires(auth.has_membership(group_id='President') or auth.has_membership(group_id='Secretary'))
def delete_member():
    mid = request.args(0)
    db(db.members.id == mid).delete()
    return dict(form=redirect(URL('view_members')))

@auth.requires(auth.has_membership(group_id='President') or auth.has_membership(group_id='VP Programming'))
def delete_event():
    mid = request.args(0)
    db(db.event_attendance.id == mid).delete()
    return dict(form=redirect(URL('view_events')))

@auth.requires(auth.has_membership(group_id='President') or auth.has_membership(group_id='VP Membership'))
def delete_level():
    mid = request.args(0)
    db(db.membership_level.id == mid).delete()
    return dict(form=redirect(URL('view_levels')))

@auth.requires(auth.has_membership(group_id='VP Membership') or auth.has_membership(group_id='President') or auth.has_membership(group_id='Secretary'))
def add_member():
    form = SQLFORM(db.members)
    form.process()
    return dict(form=form)

@auth.requires(auth.has_membership(group_id='VP Programming') or auth.has_membership(group_id='President'))
def add_event():
    form = SQLFORM(db.event_attendance)
    if form.process().accepted:
        redirect(URL('view_events'))
    return dict(form=form)

@auth.requires(auth.has_membership(group_id='VP Membership') or auth.has_membership(group_id='President'))
def add_level():
    form = SQLFORM(db.membership_level)
    if form.process().accepted:
        redirect(URL('view_levels'))
    return dict(form = form)


def view_members():
    levels=db().select(db.members.ALL, db.membership_level.ALL,
                       left=db.members.on(db.members.member_level == db.membership_level.id))
    return dict(levels=levels)

@auth.requires(auth.has_membership(group_id='Member'))
def view_events():
    levels=db().select(db.event_attendance.ALL, db.members.ALL,
                       left=db.members.on(db.event_attendance.members.contains( db.members.id)))
    return dict(levels=levels)

@auth.requires(auth.has_membership(group_id='Member'))
def view_levels():
    rows = db(db.membership_level).select()
    return dict(rows=rows)

@auth.requires(auth.has_membership(group_id='Secretary') or auth.has_membership(group_id='President'))
def member_update():
    update = db.members(request.args(0))
    form = SQLFORM(db.members, update)
    if form.process().accepted:
        redirect(URL('view_members'))
    return dict(form=form)

@auth.requires(auth.has_membership(group_id='Member'))
def member_events():
    member=db.members(request.args(0))
    rows= db(db.event_attendance.members.contains(member.id)).select(db.event_attendance.ALL)
    return dict(rows=rows)


from gluon.tools import Crud
@auth.requires(auth.has_membership(group_id='Member'))
def search_members():
    crud = Crud(db)
    form, table=crud.search(db.members)
    return dict(form=form, table=table)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
