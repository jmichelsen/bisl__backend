from django.contrib.auth.mixins import PermissionRequiredMixin


class AdminOrOwnerPermissionMixin(PermissionRequiredMixin):

    def has_permission(self):
        # check for the admin permissions on the view: recipes.delete, recipes.change
        is_admin = super().has_permission()
        return is_admin or self.get_object().user == self.request.user

