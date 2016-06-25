# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """ Display the index page """
    index = db(db.cms_page.page_index==0).select(db.cms_page.ALL).first().as_dict()

    return locals()

def page():
    """" Show a page """
    if not request.args(0):
        redirect(URL('index'))

    try:
        page = db(db.cms_page.id == int(request.args(0))).select().first().as_dict()
    except ValueError:
        try:
            page = db(db.cms_page.title=='%s' % request.args(0).title()).select().first().as_dict() or redirect(URL('default', 'index'))
        except:
            raise HTTP(404)

    if page['members_only'] and not auth.user:
        redirect(URL('index'))
    elif page['members_only'] and not auth.has_membership('member', auth.user.id):
        redirect(URL('index'))
    else:
        return locals()


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
    """ allow user to download files by name """
    
    import contenttype as c
    
    if not request.args:
        raise HTTP(404)
    elif 'cms_file.cms_file' in request.args[-1]:
        return response.download(request, db)
    else:
        file_id = request.args[-1]

        for row in db(db.cms_file.id>0).select():
            # search for the original filename
            if file_id in db.cms_file.cms_file.retrieve(row.cms_file):
                try:
                    filename, file = db.cms_file.cms_file.retrieve(row.cms_file)
                except IOError:
                    raise HTTP(404)
                response.headers["Content-Type"] = c.contenttype(file_id)
                response.headers["Content-Disposition"] = "attachment; filename=%s" % file_id
                stream = response.stream(file, chunk_size=64*1024, request=request)
                raise HTTP(200, stream, **response.headers)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def sitemap():
    sitemap=TAG.urlset(_xmlns="http://www.sitemaps.org/schemas/sitemap/0.9") # & (db.cms_page.published==True)
    sitemap.append(TAG.url(TAG.loc('http://%s' % request.env.http_host),TAG.priority(1.0)))

    posts = db((db.cms_page.page_index >= 0) & (db.cms_page.main_menu == True) & (db.cms_page.published == True) & (db.cms_page.members_only == False)).select(db.cms_page.ALL, orderby=[db.cms_page.page_index])

    for item in posts:
        if item.published and item.page_index != 0:
            sitemap.append(TAG.url(TAG.loc('http://%s/page/%s/%s' %(request.env.http_host, item.id, item.title))))

    sitemap.append(TAG.url(TAG.loc('http://%s/sitemap.xml' % request.env.http_host)))
    return '<?xml version="1.0" encoding="UTF-8"?>\n%s' %sitemap.xml()

