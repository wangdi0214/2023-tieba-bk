"""
百度贴吧项目 - 完整Django模型汇总
==================================

此文件汇总了所有应用的模型定义，包含：
1. 用户表(User)模型
2. 贴吧表(Tieba)模型  
3. 帖子表(Post)模型
4. 评论表(Comment)模型
5. 关注关系表模型
6. 消息通知表模型

所有模型都包含完整的字段定义、关系和外键约束。
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# ============================================================================
# 用户应用模型 (user_app/models.py)
# ============================================================================

class User(AbstractUser):
    """自定义用户模型"""
    
    # 扩展字段
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name='昵称')
    gender = models.SmallIntegerField(default=0, choices=[(0, '未知'), (1, '男'), (2, '女')], verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    
    # 统计字段
    post_count = models.IntegerField(default=0, verbose_name='发帖数')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    follower_count = models.IntegerField(default=0, verbose_name='粉丝数')
    following_count = models.IntegerField(default=0, verbose_name='关注数')
    
    # 状态字段
    is_verified = models.BooleanField(default=False, verbose_name='是否认证')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='最后登录IP')
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """用户详细资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    location = models.CharField(max_length=100, blank=True, verbose_name='所在地')
    website = models.URLField(blank=True, verbose_name='个人网站')
    company = models.CharField(max_length=100, blank=True, verbose_name='公司')
    school = models.CharField(max_length=100, blank=True, verbose_name='学校')
    
    # 社交链接
    github = models.URLField(blank=True, verbose_name='GitHub')
    twitter = models.URLField(blank=True, verbose_name='Twitter')
    weibo = models.URLField(blank=True, verbose_name='微博')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

class FollowRelation(models.Model):
    """用户关注关系"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='关注者')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='被关注者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')
    
    class Meta:
        db_table = 'follow_relation'
        unique_together = ('follower', 'following')
        verbose_name = '关注关系'
        verbose_name_plural = '关注关系'

class UserNotification(models.Model):
    """用户通知"""
    NOTIFICATION_TYPES = [
        ('post_like', '帖子点赞'),
        ('post_comment', '帖子评论'),
        ('comment_reply', '评论回复'),
        ('follow', '关注'),
        ('system', '系统通知'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='用户')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='通知类型')
    title = models.CharField(max_length=200, verbose_name='通知标题')
    content = models.TextField(verbose_name='通知内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    related_url = models.URLField(blank=True, verbose_name='相关链接')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'user_notification'
        verbose_name = '用户通知'
        verbose_name_plural = '用户通知'
        ordering = ['-created_at']

# ============================================================================
# 贴吧应用模型 (tieba_app/models.py)
# ============================================================================

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

# ============================================================================
# 帖子应用模型 (post_app/models.py)
# ============================================================================

class Post(models.Model):
    """帖子主表"""
    title = models.CharField(max_length=200, verbose_name='帖子标题')
    content = models.TextField(verbose_name='帖子内容')
    
    # 关系字段
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='posts', verbose_name='作者')
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, 
                            related_name='posts', verbose_name='所属贴吧')
    
    # 帖子类型
    TYPE_CHOICES = [
        (1, '普通帖'),
        (2, '精华帖'),
        (3, '置顶帖'),
        (4, '公告帖'),
        (5, '投票帖'),
    ]
    post_type = models.SmallIntegerField(choices=TYPE_CHOICES, default=1, verbose_name='帖子类型')
    
    # 统计字段
    view_count = models.IntegerField(default=0, verbose_name='浏览数')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    collect_count = models.IntegerField(default=0, verbose_name='收藏数')
    share_count = models.IntegerField(default=0, verbose_name='分享数')
    
    # 状态字段
    STATUS_CHOICES = [
        (1, '正常'),
        (2, '审核中'),
        (3, '已删除'),
        (4, '封禁'),
        (5, '草稿'),
    ]
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    
    # 权限设置
    can_comment = models.BooleanField(default=True, verbose_name='允许评论')
    can_share = models.BooleanField(default=True, verbose_name='允许分享')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_reply_at = models.DateTimeField(null=True, blank=True, verbose_name='最后回复时间')
    
    class Meta:
        db_table = 'post'
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-last_reply_at', '-created_at']
        indexes = [
            models.Index(fields=['tieba', 'post_type']),
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['last_reply_at']),
        ]
    
    def __str__(self):
        return self.title

class PostImage(models.Model):
    """帖子图片"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='帖子')
    image = models.ImageField(upload_to='post_images/', verbose_name='图片')
    caption = models.CharField(max_length=200, blank=True, verbose_name='图片说明')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    
    class Meta:
        db_table = 'post_image'
        verbose_name = '帖子图片'
        verbose_name_plural = '帖子图片'
        ordering = ['sort_order', 'id']

class PostLike(models.Model):
    """帖子点赞"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='帖子')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='post_likes', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    
    class Meta:
        db_table = 'post_like'
        verbose_name = '帖子点赞'
        verbose_name_plural = '帖子点赞'
        unique_together = ('post', 'user')
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]

class PostCollect(models.Model):
    """帖子收藏"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='collects', verbose_name='帖子')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='post_collects', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')
    
    class Meta:
        db_table = 'post_collect'
        verbose_name = '帖子收藏'
        verbose_name_plural = '帖子收藏'
        unique_together = ('post', 'user')
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

class PostViewHistory(models.Model):
    """帖子浏览历史"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='view_history', verbose_name='帖子')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='post_view_history', verbose_name='用户')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(blank=True, verbose_name='用户代理')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')
    
    class Meta:
        db_table = 'post_view_history'
        verbose_name = '帖子浏览历史'
        verbose_name_plural = '帖子浏览历史'
        indexes = [
            models.Index(fields=['user', 'viewed_at']),
            models.Index(fields=['post', 'viewed_at']),
        ]

class PostReport(models.Model):
    """帖子举报"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports', verbose_name='帖子')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                related_name='post_reports', verbose_name='举报人')
    
    # 举报类型
    REPORT_TYPE_CHOICES = [
        (1, '广告营销'),
        (2, '违法违规'),
        (3, '色情低俗'),
        (4, '人身攻击'),
        (5, '侵犯隐私'),
        (6, '垃圾信息'),
        (7, '其他'),
    ]
    report_type = models.SmallIntegerField(choices=REPORT_TYPE_CHOICES, verbose_name='举报类型')
    
    # 举报内容
    reason = models.TextField(verbose_name='举报原因')
    evidence = models.TextField(blank=True, verbose_name='证据')
    
    # 处理状态
    STATUS_CHOICES = [
        (1, '待处理'),
        (2, '处理中'),
        (3, '已处理'),
        (4, '已驳回'),
    ]
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='处理状态')
    
    # 处理信息
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                 null=True, blank=True, related_name='handled_post_reports', 
                                 verbose_name='处理人')
    handled_at = models.DateTimeField(null=True, blank=True, verbose_name='处理时间')
    handle_result = models.TextField(blank=True, verbose_name='处理结果')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='举报时间')
    
    class Meta:
        db_table = 'post_report'
        verbose_name = '帖子举报'
        verbose_name_plural = '帖子举报'
        indexes = [
            models.Index(fields=['post', 'status']),
            models.Index(fields=['reporter', 'created_at']),
        ]

# ============================================================================
# 评论应用模型 (comment_app/models.py)
# ============================================================================

class Comment(models.Model):
    """评论主表"""
    content = models.TextField(verbose_name='评论内容')
    
    # 关系字段
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='comments', verbose_name='评论者')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
                            related_name='comments', verbose_name='所属帖子')
    
    # 父评论（用于回复功能）
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                             related_name='replies', verbose_name='父评论')
    
    # 楼层号
    floor_number = models.IntegerField(default=0, verbose_name='楼层号')
    
    # 统计字段
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    reply_count = models.IntegerField(default=0, verbose_name='回复数')
    
    # 状态字段
    STATUS_CHOICES = [
        (1, '正常'),
        (2, '审核中'),
        (3, '已删除'),
        (4, '封禁'),
    ]
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['floor_number']
        indexes = [
            models.Index(fields=['post', 'floor_number']),
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['parent', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.author.username}的评论"

class CommentLike(models.Model):
    """评论点赞"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', verbose_name='评论')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='comment_likes', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    
    class Meta:
        db_table = 'comment_like'
        verbose_name = '评论点赞'
        verbose_name_plural = '评论点赞'
        unique_together = ('comment', 'user')
        indexes = [
            models.Index(fields=['comment', 'created_at']),
        ]

class CommentReport(models.Model):
    """评论举报"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reports', verbose_name='评论')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                related_name='comment_reports', verbose_name='举报人')
    
    # 举报类型
    REPORT_TYPE_CHOICES = [
        (1, '广告营销'),
        (2, '违法违规'),
        (3, '色情低俗'),
        (4, '人身攻击'),
        (5, '侵犯隐私'),
        (6, '垃圾信息'),
        (7, '其他'),
    ]
    report_type = models.SmallIntegerField(choices=REPORT_TYPE_CHOICES, verbose_name='举报类型')
    
    # 举报内容
    reason = models.TextField(verbose_name='举报原因')
    evidence = models.TextField(blank=True, verbose_name='证据')
    
    # 处理状态
    STATUS_CHOICES = [
        (1, '待处理'),
        (2, '处理中'),
        (3, '已处理'),
        (4, '已驳回'),
    ]
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='处理状态')
    
    # 处理信息
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                 null=True, blank=True, related_name='handled_comment_reports', 
                                 verbose_name='处理人')
    handled_at = models.DateTimeField(null=True, blank=True, verbose_name='处理时间')
    handle_result = models.TextField(blank=True, verbose_name='处理结果')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='举报时间')
    
    class Meta:
        db_table = 'comment_report'
        verbose_name = '评论举报'
        verbose_name_plural = '评论举报'
        indexes = [
            models.Index(fields=['comment', 'status']),
            models.Index(fields=['reporter', 'created_at']),
        ]

class CommentMention(models.Model):
    """评论中@的用户"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='mentions', verbose_name='评论')
    mentioned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                     related_name='comment_mentions', verbose_name='被@用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'comment_mention'
        verbose_name = '评论提及'
        verbose_name_plural = '评论提及'
        unique_together = ('comment', 'mentioned_user')
        indexes = [
            models.Index(fields=['mentioned_user', 'created_at']),
        ]

# ============================================================================
# 消息应用模型 (message_app/models.py)
# ============================================================================

class PrivateMessage(models.Model):
    """私信消息"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='sent_messages', verbose_name='发送者')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                related_name='received_messages', verbose_name='接收者')
    
    # 消息内容
    content = models.TextField(verbose_name='消息内容')
    
    # 消息类型
    MESSAGE_TYPE_CHOICES = [
        (1, '文本消息'),
        (2, '图片消息'),
        (3, '文件消息'),
        (4, '系统消息'),
    ]
    message_type = models.SmallIntegerField(choices=MESSAGE_TYPE_CHOICES, default=1, verbose_name='消息类型')
    
    # 状态字段
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    is_deleted_by_sender = models.BooleanField(default=False, verbose_name='发送者删除')
    is_deleted_by_receiver = models.BooleanField(default=False, verbose_name='接收者删除')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='阅读时间')
    
    class Meta:
        db_table = 'private_message'
        verbose_name = '私信消息'
        verbose_name_plural = '私信消息'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sender', 'receiver', 'created_at']),
            models.Index(fields=['receiver', 'is_read', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

class MessageAttachment(models.Model):
    """消息附件"""
    message = models.ForeignKey(PrivateMessage, on_delete=models.CASCADE, 
                                related_name='attachments', verbose_name='消息')
    
    # 附件类型
    ATTACHMENT_TYPE_CHOICES = [
        (1, '图片'),
        (2, '文件'),
        (3, '音频'),
        (4, '视频'),
    ]
    attachment_type = models.SmallIntegerField(choices=ATTACHMENT_TYPE_CHOICES, verbose_name='附件类型')
    
    # 附件文件
    file = models.FileField(upload_to='message_attachments/', verbose_name='附件文件')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_size = models.IntegerField(default=0, verbose_name='文件大小')
    
    # 缩略图（用于图片/视频）
    thumbnail = models.ImageField(upload_to='message_thumbnails/', null=True, blank=True, verbose_name='缩略图')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    
    class Meta:
        db_table = 'message_attachment'
        verbose_name = '消息附件'
        verbose_name_plural = '消息附件'

class Conversation(models.Model):
    """会话（用于私信对话）"""
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='conversations_as_user1', verbose_name='用户1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='conversations_as_user2', verbose_name='用户2')
    
    # 会话统计
    message_count = models.IntegerField(default=0, verbose_name='消息数量')
    unread_count_user1 = models.IntegerField(default=0, verbose_name='用户1未读数')
    unread_count_user2 = models.IntegerField(default=0, verbose_name='用户2未读数')
    
    # 最后一条消息
    last_message = models.ForeignKey(PrivateMessage, on_delete=models.SET_NULL, 
                                    null=True, blank=True, verbose_name='最后消息')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'conversation'
        verbose_name = '会话'
        verbose_name_plural = '会话'
        unique_together = ('user1', 'user2')
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user1', 'updated_at']),
            models.Index(fields=['user2', 'updated_at']),
        ]

class SystemMessage(models.Model):
    """系统消息"""
    title = models.CharField(max_length=200, verbose_name='消息标题')
    content = models.TextField(verbose_name='消息内容')
    
    # 消息类型
    MESSAGE_TYPE_CHOICES = [
        (1, '系统公告'),
        (2, '活动通知'),
        (3, '版本更新'),
        (4, '安全提醒'),
        (5, '其他'),
    ]
    message_type = models.SmallIntegerField(choices=MESSAGE_TYPE_CHOICES, default=1, verbose_name='消息类型')
    
    # 目标用户
    target_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, 
                                         related_name='system_messages', verbose_name='目标用户')
    
    # 发送设置
    is_broadcast = models.BooleanField(default=False, verbose_name='是否广播')
    is_important = models.BooleanField(default=False, verbose_name='是否重要')
    is_pinned = models.BooleanField(default=False, verbose_name='是否置顶')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    
    class Meta:
        db_table = 'system_message'
        verbose_name = '系统消息'
        verbose_name_plural = '系统消息'
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['message_type', 'created_at']),
            models.Index(fields=['is_broadcast', 'created_at']),
        ]
    
    def __str__(self):
        return self.title

class UserMessageSetting(models.Model):
    """用户消息设置"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                related_name='message_settings', verbose_name='用户')
    
    # 通知设置
    receive_private_messages = models.BooleanField(default=True, verbose_name='接收私信')
    receive_system_messages = models.BooleanField(default=True, verbose_name='接收系统消息')
    receive_post_notifications = models.BooleanField(default=True, verbose_name='接收帖子通知')
    receive_comment_notifications = models.BooleanField(default=True, verbose_name='接收评论通知')
    receive_follow_notifications = models.BooleanField(default=True, verbose_name='接收关注通知')
    
    # 隐私设置
    allow_stranger_messages = models.BooleanField(default=True, verbose_name='允许陌生人私信')
    allow_friend_messages = models.BooleanField(default=True, verbose_name='允许好友私信')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_message_setting'
        verbose_name = '用户消息设置'
        verbose_name_plural = '用户消息设置'

class MessageBlacklist(models.Model):
    """消息黑名单"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='message_blacklist', verbose_name='用户')
    blocked_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                    related_name='blocked_by_users', verbose_name='被屏蔽用户')
    
    # 屏蔽原因
    reason = models.CharField(max_length=200, blank=True, verbose_name='屏蔽原因')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='屏蔽时间')
    
    class Meta:
        db_table = 'message_blacklist'
        verbose_name = '消息黑名单'
        verbose_name_plural = '消息黑名单'
        unique_together = ('user', 'blocked_user')
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

# ============================================================================
# 模型关系总结
# ============================================================================

"""
模型关系总结：

1. 用户相关模型：
   - User (主用户表)
   - UserProfile (用户详细资料，一对一)
   - FollowRelation (用户关注关系，多对多)
   - UserNotification (用户通知，一对多)

2. 贴吧相关模型：
   - TiebaCategory (贴吧分类)
   - Tieba (贴吧主表，关联分类和用户)
   - TiebaMember (贴吧成员，关联贴吧和用户)
   - TiebaAdmin (贴吧管理员，关联贴吧和用户)
   - TiebaAnnouncement (贴吧公告，关联贴吧和用户)

3. 帖子相关模型：
   - Post (帖子主表，关联贴吧和用户)
   - PostImage (帖子图片，一对多)
   - PostLike (帖子点赞，多对多)
   - PostCollect (帖子收藏，多对多)
   - PostViewHistory (帖子浏览历史，一对多)
   - PostReport (帖子举报，一对多)

4. 评论相关模型：
   - Comment (评论主表，关联帖子和用户)
   - CommentLike (评论点赞，多对多)
   - CommentReport (评论举报，一对多)
   - CommentMention (评论提及，多对多)

5. 消息相关模型：
   - PrivateMessage (私信消息，关联发送者和接收者)
   - MessageAttachment (消息附件，一对多)
   - Conversation (会话，关联两个用户)
   - SystemMessage (系统消息，多对多)
   - UserMessageSetting (用户消息设置，一对一)
   - MessageBlacklist (消息黑名单，多对多)

所有模型都包含完整的字段定义、外键约束、索引和元数据配置。
"""