# -*- coding: utf-8 -*-

@auth.requires_membership("admin")
def clear_cache():
	cache.ram.clear()
	redirect(URL('admin', 'index'))


def clear_cache_btn(fields, url):
	return A(SPAN(T('Clear Cache'), _class='buttontext button'), _href=URL('clear_cache'), _class='w2p_trap button btn')


@auth.requires_membership("admin")
def index():
	## Customise page model default
	db.cms_page.id.readable = False
	db.cms_page.url.readable = False
	deletable = True

	# If editing the index page
	if 'edit' in request.args:
		deletable = False
		if db.cms_page(request.args(2)).page_index == 0:
			#db.cms_page.title.writable = db.cms_page.title.readable = False
			db.cms_page.url.writable = db.cms_page.url.readable = False
			db.cms_page.main_menu.writable = db.cms_page.main_menu.readable = False
			db.cms_page.page_index.writable = db.cms_page.page_index.readable = False
			db.cms_page.published.writable = db.cms_page.published.readable = False
			db.cms_page.members_only.writable = db.cms_page.members_only.readable = False
	if 'delete' in request.args and db.cms_page(request.args(2)).page_index == 0:
		session.flash = "Cannot delete this page"
		redirect(URL('admin'))

	## SQLFORM parameters
	links = [dict(header='URL', body=lambda row: URL('default', 'page', args=[row.title]) if row.page_index != 0 else '/'), lambda row: A(SPAN(_class='icon magnifier icon-zoom-in'),SPAN(_class='buttontext button', _title='View'), 'Preview', _class='w2p_trap button btn', _href=URL("admin", "page_preview",args=[row.id]))]
	query = db.cms_page.id>0 #.main_menu == False
	fields = [db.cms_page.id, db.cms_page.title, db.cms_page.main_menu, db.cms_page.published, db.cms_page.parent_menu, db.cms_page.members_only, db.cms_page.page_index]
	orderby = [db.cms_page.page_index]

	form = SQLFORM.grid(query=query, links=links, fields=fields, orderby=orderby, deletable=deletable, searchable=True, details=False, csv=False, search_widget=clear_cache_btn)
	#.add_button('Clear Cache', cache.ram.clear())
	return dict(form=form)


@auth.requires_membership("admin")
def page_preview():
	try:
		page = db.cms_page(int(request.args(0)))
	except:
		raise HTTP(404)

	return dict(page=page)


@auth.requires_membership("admin")
def style_sheet():
	""" Create form for updating customised style sheets """ 
	form = SQLFORM.grid(db.customise, 
						create=False,
						details=False,
						deletable=False,
						orderby=~db.customise.id,
						csv=False, 
						searchable=False)
	return dict(form=form)


@auth.requires_membership("admin")
def file():
	""" Manage files """ 
	if 'new' in request.args:
		db.cms_file.created_on.readable = False
		db.cms_file.created_by.readable = False

	#links = [dict(header='Name', body=lambda row: db.file.file.retrieve(row.file)[0]), dict(header='URL', body=lambda row: '/init/default/download/%s' %(db.file.file.retrieve(row.file)[0]))]
	links = [dict(header='URL', body=lambda row: '/init/default/download/%s' %(db.cms_file.cms_file.retrieve(row.cms_file)[0]))]
	fields =[db.cms_file.cms_file]

	form = SQLFORM.grid(db.cms_file, links=links, searchable=False, csv=False, orderby=~db.cms_file.created_on)

	return dict(form=form)


@auth.requires_membership("super_admin")
def manage_membership():
	user_id = request.args(0)
	db.auth_membership.user_id.default = int(user_id)
	db.auth_membership.user_id.writable = False
	form = SQLFORM.grid(db.auth_membership.user_id == user_id,
						args=[user_id],
						searchable=False,
						details=False,
						selectable=False,
						csv=False)
	return form


@auth.requires_membership("super_admin")
def manage_user():
	user_id = request.args(0) or redirect(URL('list_users'))

	form = SQLFORM(db.auth_user, user_id)
	membership_panel = LOAD(request.controller,
							'manage_membership.html',
							 args=[user_id],
							 ajax=True)
	return dict(form=form, membership_panel=membership_panel)


@auth.requires_membership("super_admin")
def list_users():
	links = [lambda row: A(SPAN(_class='icon pen icon-pencil'),SPAN(_class='buttontext button', _title='Edit'), 'Edit', _class='w2p_trap button btn', _href=URL('manage_user', args=row.id))]

	users = SQLFORM.grid(db.auth_user,
						links=links,
						editable=False,
						details=False,
						csv=False)


	return dict(users=users)

@auth.requires_membership("admin")
def help():
	return locals()
