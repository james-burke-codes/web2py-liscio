#
# CKEditor widget function
def advanced_editor(field, value):
    return TEXTAREA(_id = str(field).replace('.','_'), _name=field.name, _class='text ckeditor', value=value, _cols=80, _rows=10)


#
# cms_page - cms_pages of the website
#
#db.define_table('cms_page',
#    Field('main_menu', 'boolean'))

db.define_table('cms_page',
    Field('title'), # , unique=True
    Field('url', default=None, comment='Redirect to external page'),
    Field('main_menu', 'boolean', default=True, comment='add to the main menu'),
    #Field('parent_menu', 'reference cms_page', default=None),
    Field('parent_menu', default=None),
    Field('body', 'text', default=''),
    Field('side', 'text', default=''),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', db.auth_user, default=auth.user_id),
    Field('page_index', 'integer', comment='position page will appear on the main menu, blank if n/a' ),
    Field('published', 'boolean', default=True, comment='make the page public'),
    Field('members_only', 'boolean', default=False, comment='only members can view this page'),
    format='%(title)s')
    #,redefine=True)


db.cms_page.body.widget = advanced_editor
db.cms_page.side.widget = advanced_editor

db.cms_page.created_by.readable = db.cms_page.created_by.writable = False
db.cms_page.created_on.readable = db.cms_page.created_on.writable = False
db.cms_page.main_menu.writable = True
db.cms_page.page_index.required = False

# Restrict the parent menu to only existing pages in the main menu - 2 tier menu system.
db.cms_page.parent_menu.requires = IS_EMPTY_OR(IS_IN_DB(
    db((db.cms_page.main_menu == True) & (db.cms_page.parent_menu == None)), db.cms_page.id, 'cms_page.title'))

# Create a default page index, total + 1 of pages in the main menu
db.cms_page.page_index.default = len(db((db.cms_page.id>0) & (db.cms_page.main_menu == True)).select(db.cms_page.ALL))

#
#  cms_file - cms_files for the website
#

db.define_table('cms_file',
    Field('cms_file', 'upload'),
    #Field('name', default=lambda v=request.post_vars:v.cms_file.cms_filename if v.cms_file else ''), #db.cms_file.cms_file.retrieve(r.cms_file)[0]
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id),
    format='%(name)s')

db.cms_file.created_on.writable = False
db.cms_file.created_by.writable = False
db.cms_file.id.readable = False


#
# CUSTOMISE - customisable cms_files that allow the user to change html/css etc.
#
db.define_table('customise',
    Field('name', unique=True),
    Field('cms_file'),
    Field('body', 'text'),
    format='%(name)s'
    )

db.customise.id.readable = db.customise.id.writable = False
db.customise.cms_file.readable = db.customise.cms_file.writable = False

#db.cms_page.insert(title = 'test123', subtitle = 'test123', body = 'test', parent_menu = None, main_menu = True, page_index = 79)

#db.customise.drop()

def check_initialize():
    if not db().select(db.cms_page.ALL).first():        
        db.cms_page.insert(
            title = 'Index',
            body = '<p>Welcome Home</p>',
            parent_menu = None,
            main_menu = True,
            published = True,
            page_index = 0
        )
    if not db().select(db.customise.ALL).first():
        db.customise.insert(
            name='css_general',
            body=None
        )
        db.customise.insert(
            name='css_desktop',
            body=None
        )
        db.customise.insert(
            name='css_mobile',
            body=None
        )
cache.ram('db_initialized', check_initialize(), time_expire=None)

