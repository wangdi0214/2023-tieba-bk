from django.db import models
from django.conf import settings

class Post(models.Model):
    """帖子主表"""
    title = models.CharField(max_length=200, verbose_name='帖子标题')
    content = models.TextField(verbose_name='帖子内容')
    
    # 关系字段
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='posts', verbose_name='作者')
    tieba = models.ForeignKey('tieba_app.Tieba', on_delete=models.CASCADE, 
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