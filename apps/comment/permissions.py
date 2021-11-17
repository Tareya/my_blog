from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    '''
        用户本人可以执行所有操作（包括非安全请求）
        其他用户拥有只读权限
    '''

    message = "You must be the owner to update."


    def owner_or_safe_methods(self, request, func):
        '''
            接收匿名函数
        '''
        if request.method in permissions.SAFE_METHODS:
            return True

        return func()


    
    def has_permission(self, request, view):
        '''
            匿名函数: 验证认证状态
        '''
        return self.owner_or_safe_methods(
            request, 
            lambda: request.user.is_authenticated
        )



    def has_object_permission(self, request, view, obj):
        '''
            匿名函数: 验证当前验证用户与评论用户是否为同一人
        '''
        return self.owner_or_safe_methods(
            request, 
            lambda: obj.author == request.user
        )

