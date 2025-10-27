from django.db import models
from django.conf import settings

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
    receive_private_message = models.BooleanField(default=True, verbose_name='接收私信')
    receive_system_message = models.BooleanField(default=True, verbose_name='接收系统消息')
    receive_notification = models.BooleanField(default=True, verbose_name='接收通知')
    
    # 隐私设置
    allow_stranger_message = models.BooleanField(default=True, verbose_name='允许陌生人私信')
    message_filter_level = models.SmallIntegerField(choices=[(1, '宽松'), (2, '中等'), (3, '严格')], 
                                                   default=1, verbose_name='消息过滤级别')
    
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