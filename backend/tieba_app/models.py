from django.db import models
from django.conf import settings

class TiebaCategory(models.Model):
    """贴吧分类"""
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    description = models.TextField(max_length=200, blank=True, verbose_name='分类描述')
    icon = models.CharField(max_length=100, blank=True, verbose_name='分类图标')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    class Meta:
        db_table = 'tieba_category'
        verbose_name = '贴吧分类'
        verbose_name_plural = '贴吧分类'
        ordering = ['sort_order', 'id']
    
    def __str__(self):
        return self.name

class Tieba(models.Model):
    """贴吧主表"""
    name = models.CharField(max_length=100, unique=True, verbose_name='贴吧名称')
    description = models.TextField(max_length=500, blank=True, verbose_name='贴吧描述')
    avatar = models.ImageField(upload_to='tieba_avatars/', null=True, blank=True, verbose_name='贴吧头像')
    banner = models.ImageField(upload_to='tieba_banners/', null=True, blank=True, verbose_name='贴吧横幅')
    
    # 关系字段
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                             related_name='owned_tiebas', verbose_name='创建者')
    category = models.ForeignKey(TiebaCategory, on_delete=models.SET_NULL, 
                                null=True, blank=True, verbose_name='分类')
    
    # 统计字段
    member_count = models.IntegerField(default=0, verbose_name='成员数量')
    post_count = models.IntegerField(default=0, verbose_name='帖子数量')
    today_post_count = models.IntegerField(default=0, verbose_name='今日发帖')
    
    # 状态字段
    STATUS_CHOICES = [
        (1, '正常'),
        (2, '审核中'),
        (3, '封禁'),
        (4, '隐藏'),
    ]
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    
    # 权限设置
    join_permission = models.SmallIntegerField(choices=[(1, '自由加入'), (2, '需要审核'), (3, '禁止加入')], 
                                              default=1, verbose_name='加入权限')
    post_permission = models.SmallIntegerField(choices=[(1, '自由发帖'), (2, '需要审核'), (3, '禁止发帖')], 
                                              default=1, verbose_name='发帖权限')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'tieba'
        verbose_name = '贴吧'
        verbose_name_plural = '贴吧'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name

class TiebaMember(models.Model):
    """贴吧成员关系"""
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, related_name='members', verbose_name='贴吧')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='tieba_memberships', verbose_name='用户')
    
    # 成员角色
    ROLE_CHOICES = [
        (1, '普通成员'),
        (2, '小吧主'),
        (3, '大吧主'),
        (4, '创始人'),
    ]
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=1, verbose_name='角色')
    
    # 成员状态
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    join_date = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')
    last_visit = models.DateTimeField(null=True, blank=True, verbose_name='最后访问')
    
    class Meta:
        db_table = 'tieba_member'
        verbose_name = '贴吧成员'
        verbose_name_plural = '贴吧成员'
        unique_together = ('tieba', 'user')
        indexes = [
            models.Index(fields=['tieba', 'role']),
            models.Index(fields=['user', 'join_date']),
        ]

class TiebaAdmin(models.Model):
    """贴吧管理员"""
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, related_name='admins', verbose_name='贴吧')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='tieba_admin_roles', verbose_name='管理员')
    
    # 权限设置
    can_manage_posts = models.BooleanField(default=True, verbose_name='管理帖子')
    can_manage_comments = models.BooleanField(default=True, verbose_name='管理评论')
    can_manage_members = models.BooleanField(default=True, verbose_name='管理成员')
    can_manage_settings = models.BooleanField(default=False, verbose_name='管理设置')
    
    # 时间字段
    appointed_at = models.DateTimeField(auto_now_add=True, verbose_name='任命时间')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='任期到期')
    
    class Meta:
        db_table = 'tieba_admin'
        verbose_name = '贴吧管理员'
        verbose_name_plural = '贴吧管理员'
        unique_together = ('tieba', 'user')

class TiebaAnnouncement(models.Model):
    """贴吧公告"""
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, related_name='announcements', verbose_name='贴吧')
    title = models.CharField(max_length=200, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='发布者')
    
    # 公告类型
    TYPE_CHOICES = [
        (1, '普通公告'),
        (2, '重要公告'),
        (3, '系统公告'),
    ]
    announcement_type = models.SmallIntegerField(choices=TYPE_CHOICES, default=1, verbose_name='公告类型')
    
    # 状态字段
    is_pinned = models.BooleanField(default=False, verbose_name='是否置顶')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    
    class Meta:
        db_table = 'tieba_announcement'
        verbose_name = '贴吧公告'
        verbose_name_plural = '贴吧公告'
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['tieba', 'is_active']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.title