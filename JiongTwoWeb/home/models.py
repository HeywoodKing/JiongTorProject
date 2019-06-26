from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin,BaseUserManager,AbstractBaseUser
# from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from datetime import datetime
from django.db.models import BooleanField as _BooleanField


# Create your models here.
class BooleanField(_BooleanField):
    def get_prep_value(self, value):
        if value in (0, '0', 'false', 'False'):
            return False
        elif value in (1, '1', 'true', 'True'):
            return True
        else:
            return super(BooleanField, self).get_prep_value(value)


# AbstractBaseUser中只含有3个field: password, last_login和is_active.
# 如果你对django user model默认的first_name, last_name不满意,
# 或者只想保留默认的密码储存方式, 则可以选择这一方式.
class JtUserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=255,
                               verbose_name='用户头像')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ')
    phone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号')
    nick_name = models.CharField(max_length=30, verbose_name='昵称')
    sex = models.CharField('性别', max_length=5, choices=(('0', '保密'), ('1', '男'), ('2', '女')), default=0)
    birthday = models.DateTimeField('出生日期', auto_now=True)
    # is_lock = models.BooleanField(default=False, verbose_name='是否锁定', choices=((0, '否'), (1, '是')))
    # is_enable = models.BooleanField(default=True, verbose_name='是否启用', choices=((0, '否'), (1, '是')))

    class Meta(AbstractUser.Meta):
        db_table = 'jt_userprofile'
        swappable = 'AUTH_USER_MODEL'
        ordering = ['-id']
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    # class Meta:
    #     db_table = 'jt_userprofile'
    #     verbose_name = '用户'
    #     verbose_name_plural = verbose_name
    #     ordering = ['-id']

    def __str__(self):
        return self.username

    # def create_user(self, username, nickname, password=None):
    #     # create user here
    #     pass
    #
    # def create_superuser(self, username, password):
    #     # create superuser here
    #     pass


class EmailVerifyRecord(models.Model):
    """
    图形验证码
    """
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码')
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=send_choices, max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class BaseModel(models.Model):
    # default=datetime.now().replace(tzinfo=pytz.utc)
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    create_uid = models.IntegerField('创建人ID', default=123456789, auto_created=True)
    create_username = models.CharField('创建人名称', max_length=30, default='admin', auto_created=True)
    operate_time = models.DateTimeField('操作时间', auto_now=True)
    operate_uid = models.IntegerField('操作人ID', default=123456789, auto_created=True)
    operate_username = models.CharField('操作人名称', max_length=30, default='admin', auto_created=True)

    class Meta:
        abstract = True


# 系统相关
# class SysSetting(BaseModel):
#
#     class Meta:
#         db_table = 'sys_setting'
#         verbose_name = '系统相关'
#         verbose_name_plural = verbose_name


# 系统|站点配置
class JtSysConfig(BaseModel):
    site_name = models.CharField('站点名称', max_length=50)
    site_desc = models.CharField('站点描述', max_length=150)
    site_author = models.CharField('作者', max_length=100)
    site_company = models.CharField('公司', max_length=100)
    address = models.CharField('底部显示地址', max_length=150)
    telephone = models.CharField('底部显示电话', max_length=11)
    email = models.EmailField('邮箱', max_length=50)
    icp = models.CharField('备案号', max_length=15)
    remark = models.CharField('备注', max_length=200)

    class Meta:
        db_table = "jt_sysconfig"
        verbose_name = '站点配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.site_name

# # 广告位
# class JtAdPosition(BaseModel):
#     name = models.CharField('广告位名称', max_length=50)
#     target_type = models.CharField('广告位类型', max_length=20)
#     width = models.IntegerField("广告位宽度", default=0)
#     height = models.IntegerField("广告位高度", default=0)
#     is_enable = models.BooleanField('是否启用', default=True)
#
#     class Meta:
#         db_table = "jt_adposition"
#         ordering = ['-create_time']
#         verbose_name = '广告位'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
#
# # 广告记录
# class JtAdRecord(BaseModel):
#     name = models.CharField('广告名称', max_length=30)
#     slug = models.SlugField('Slug', max_length=255, unique=True, null=True, blank=True,
#                             help_text='根据name生成的，用于生成页面URL，必须唯一')
#     path = models.CharField('广告图片路径', max_length=200)
#     image = models.ImageField('广告图片', max_length=255, null=True, blank=True, upload_to='ad/%Y/%m')
#     is_enable = models.BooleanField('是否启用', default=True)
#     sort = models.IntegerField('排序', default=0)
#     adposition = models.ForeignKey(to='JtAdPosition', to_field='id')
#
#     class Meta:
#         db_table = 'jt_adrecord'
#         ordering = ['sort', '-create_time']
#         verbose_name = '广告记录'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('jt_adrecord', args=(self.slug, ))


# 文章列表
class JtArticle(BaseModel):
    title = models.CharField('标题', max_length=255)
    slug = models.SlugField('Slug', max_length=255, unique=True, null=True, blank=True,
                            help_text='根据title生成的，用于生成页面URL，必须唯一')
    user = models.ForeignKey(to='JtUserProfile', to_field='id', on_delete=models.CASCADE, verbose_name='作者')
    brief = models.CharField('摘要', max_length=50)
    content = models.TextField('内容', default=None, null=True, blank=True)
    read_count = models.IntegerField('浏览数', default=0)
    like_count = models.IntegerField('点赞数', default=0)
    oppose_count = models.IntegerField('反对数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    cover_image_url = models.ImageField('封面图片', max_length=255, null=True, blank=True, upload_to='article/%Y/%m')
    type = models.CharField('类型', max_length=10, choices=(('0', '文字'), ('1', '图片'), ('2', '视频')), default=0)
    is_recommend = models.BooleanField('是否推荐', default=False)
    sort = models.IntegerField('排序', default=0)
    is_enable = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = 'jt_article'
        ordering = ['sort', '-create_time']
        verbose_name = '文章列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('news', args=(self.slug, ))

    def get_absolute_url(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ChfNews, self).get_absolute_url(*args, **kwargs)

    def profile(self):
        if len(str(self.content)) > 20:
            return '{}...'.format(str(self.content)[0:20])
        else:
            return str(self.content)

    profile.allow_tags = True
    profile.short_description = u'内容'


# 评论列表
class JtComment(BaseModel):
    # to = 'ChfProductType', null = True, blank = True, on_delete = models.CASCADE, verbose_name = '产品类型'
    uid = models.IntegerField('评论人id', default=0)
    username = models.CharField('评论人', max_length=50)
    object_id = models.ForeignKey(to='JtArticle', to_field='id', on_delete=models.CASCADE, verbose_name='被评论文章')
    target_uid = models.IntegerField('被评论人Id', default=0)
    target_username = models.CharField('被评论人', max_length=50)
    message = models.CharField('评论内容', max_length=255)
    is_enable = models.BooleanField('是否启用', default=True)
    is_audit = models.BooleanField('是否审核', default=True)

    class Meta:
        db_table = 'jt_comment'
        ordering = ['-create_time']
        verbose_name = '评论列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message

    def profile(self):
        if len(str(self.message)) > 80:
            return '{}...'.format(str(self.message)[0:80])
        else:
            return str(self.message)

    # 如何将一个TextField字段设为safe ？
    profile.allow_tags = True
    profile.short_description = u'评论内容'


# 工作机会
class JtJob(BaseModel):
    job_name = models.CharField('职位名称', max_length=50)
    slug = models.SlugField('Slug', max_length=255, unique=True, null=True, blank=True,
                            help_text='根据job_name生成的，用于生成页面URL，必须唯一')
    work_year = models.CharField('工作经验', max_length=20, default=None, null=True, blank=True)
    education = models.CharField('学历', max_length=10, choices=(
                                                ('0', '请选择'),
                                                ('1', '博士导师'),
                                                ('2', '博士后'),
                                                ('3', '博士'),
                                                ('4', '硕士'),
                                                ('5', '研究生'),
                                                ('6', '本科'),
                                                ('7', '大专'),
                                                ('8', '高中'),
                                                ('9', '初中'),
                                                ('10', '小学'),
                                                ('11', '其他'),
                                                ),
                                 default=0
                                 )
    work_prop = models.CharField('工作性质', max_length=5,
                                 choices=(
                                     ('0', '全职'),
                                     ('1', '兼职'),
                                     ('2', '自由职业'),
                                     ('3', '其他'),
                                 ), default=0)
    # job_require = models.TextField('岗位要求', default=None, null=True, blank=True)
    # skill_require = models.TextField('技能要求', default=None, null=True, blank=True)
    content = models.TextField('招聘要求', default=None, null=True, blank=True)
    sort = models.IntegerField('排序', default=0)
    is_enable = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = 'jt_job'
        ordering = ['sort', '-create_time']
        verbose_name = '工作机会'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.job_name

    # def get_absolute_url(self):
    #     return reverse('job', args=(self.slug, ))

    def get_absolute_url(self, *args, **kwargs):
        self.slug = slugify(self.job_name)
        super(ChfJobRecruit, self).get_absolute_url(*args, **kwargs)

    def profile(self):
        if len(str(self.content)) > 80:
            return '{}...'.format(str(self.content)[0:80])
        else:
            return str(self.content)

    # 如何将一个TextField字段设为safe
    profile.allow_tags = True
    profile.short_description = u'招聘要求'
