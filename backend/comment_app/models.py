from django.db import models
from django.conf import settings

class Comment(models.Model):
    """评论主表"""
    content = models.TextField(verbose_name='评论内容')
    
    # 关系字段
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='comments', verbose_name='评论者')
    post = models.ForeignKey('post_app.Post', on_delete=models.CASCADE, 
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