from auth_manager.views import ManageUserView


MANAGE_USER = ManageUserView.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
