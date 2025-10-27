from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """自定义用户模型"""
    
    # 扩展字段
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    gender = models.SmallIntegerField(default=0, choices=[(0, '未知'), (1, '男'), (2, '女')])
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # 统计字段
    post_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    
    # 状态字段
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """用户详细资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100, blank=True)
    
    # 社交链接
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    weibo = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

class FollowRelation(models.Model):
    """用户关注关系"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    related_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_notification'
        verbose_name = '用户通知'
        verbose_name_plural = '用户通知'
        ordering = ['-created_at']