Permissions and Groups Setup:

Book model has custom permissions: can_view, can_create, can_edit, can_delete
Groups:
Admins: all permissions
Editors: can_create, can_edit
Viewers: can_view
Use @permission_required('relationship_app.') in views to enforce permissions