from rest_framework import permissions


class IsAdminUserorReadonly(permissions.BasePermission):
    '''
        只有管理员用户进行所有操作
        其他用户仅有只读权限
    '''

    def has_permission(self, request, view):
        # 允许所有 GET、HEAD、OPTIONS 请求
        if request.method in permissions.SAFE_METHODS:

            return True

        # 超级用户才可以进行其他操作
        return request.user.is_superuser
