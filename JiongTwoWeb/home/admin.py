from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from home import models
from django.contrib.admin import SimpleListFilter

# Register your models here.
admin.site.index_title = '欢迎使用囧途后台管理系统'
admin.site.site_title = '后台管理系统'
admin.site.site_header = '欢迎使用囧途后台管理系统'


# 是否启用过滤
class IsEnableFilter(SimpleListFilter):
    title = '是否启用'
    parameter_name = 'is_enable'

    def lookups(self, request, model_admin):
        return [(1, '是'), (0, '否')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_enable=True)
        elif self.value() == '0':
            return queryset.filter(is_enable=False)
        else:
            return queryset.filter()


# 是否领取
class IsGetFilter(SimpleListFilter):
    title = '是否领取'
    parameter_name = 'is_get'

    def lookups(self, request, model_admin):
        return [(1, '已领取'), (0, '未领取')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_get=True)
        elif self.value() == '0':
            return queryset.filter(is_get=False)
        else:
            return queryset.filter()


# 是否已通知
class IsInformFilter(SimpleListFilter):
    title = '是否通知'
    parameter_name = 'is_inform'

    def lookups(self, request, model_admin):
        return [(1, '已通知'), (0, '未通知')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_inform=True)
        elif self.value() == '0':
            return queryset.filter(is_inform=False)
        else:
            return queryset.filter()


# 是否推荐
class IsRecommendFilter(SimpleListFilter):
    title = '是否推荐'
    parameter_name = 'is_recommend'

    def lookups(self, request, model_admin):
        return [(1, '是'), (0, '否')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_recommend=True)
        elif self.value() == '0':
            return queryset.filter(is_recommend=False)
        else:
            return queryset.filter()


# 超级用户状态
class IsSuperUserFilter(SimpleListFilter):
    title = '超级用户状态'
    parameter_name = 'is_superuser'

    def lookups(self, request, model_admin):
        return [(1, '是'), (0, '否')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_superuser=True)
        elif self.value() == '0':
            return queryset.filter(is_superuser=False)
        else:
            return queryset.filter()


# 超级用户状态
class IsActiveFilter(SimpleListFilter):
    title = '是否有效'
    parameter_name = 'is_superuser'

    def lookups(self, request, model_admin):
        return [(1, '是'), (0, '否')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_active=True)
        elif self.value() == '0':
            return queryset.filter(is_active=False)
        else:
            return queryset.filter()


# 管理员
@admin.register(models.JtUserProfile)
class JtUserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'nick_name', 'first_name', 'last_name', 'qq', 'phone', 'sex', 'birthday',
                    'is_superuser', 'is_active', 'avatar')
    list_display_links = ('username', )
    list_editable = ('nick_name', 'qq', 'phone', 'sex', 'is_superuser', 'is_active', 'avatar')
    list_per_page = 30
    list_filter = (IsSuperUserFilter, IsActiveFilter, 'groups')
    search_fields = ('username', 'nick_name', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username', )


# 文章列表
@admin.register(models.JtArticle)
class JtArticleAdmin(admin.ModelAdmin):
    # fields = ()
    # inlines = ()
    list_display = ('title', 'brief', 'read_count', 'like_count', 'oppose_count', 'comment_count', 'sort',
                    'type', 'is_recommend', 'is_enable', 'create_time')
    list_display_links = ('title', 'brief', )
    list_editable = ('type', 'sort', 'is_recommend', 'is_enable', 'read_count', 'like_count', 'oppose_count', 'comment_count')
    list_filter = ('type', IsRecommendFilter, IsEnableFilter, 'create_time', )
    list_per_page = 15
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username', )
    # fieldsets = (
    #     ('基本设置', {
    #         'fields': ('name', 'brief', 'product_type', )
    #     }),
    #     ('高级设置', {
    #         'classes': ('collapse', ),
    #         'fields': ('read_count', 'content', 'cover_image_url', 'sort', 'is_recommand')
    #     }),
    # )
    search_fields = ('title', 'type', 'brief', 'profile')
    # list_max_show_all =
    # list_per_page =
    # list_select_related =
    # change_list_template =
    # sortable_by =
    # '''每页显示条目数'''
    # list_per_page = 10
    # 按日期筛选
    # date_hierarchy = 'create_time'
    # 按创建日期排序
    # ordering = ('-create_time',)
    # prepopulated_fields = {'slug': ('name',)}

    class Media:
        js = (
            '/static/plugins/kindeditor-4.1.10/kindeditor-all-min.js',
            '/static/plugins/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/plugins/kindeditor-4.1.10/config.js',
        )


# 工作机会
@admin.register(models.JtJob)
class JtJobAdmin(admin.ModelAdmin):
    # exclude = ('job_require', 'skill_require', )
    list_display = ('job_name', 'work_year', 'education', 'work_prop', 'profile', 'sort', 'is_enable')
    list_display_links = ('job_name', 'profile', )
    list_editable = ('education', 'work_prop', 'sort', 'is_enable')
    list_filter = ('education', 'work_prop', IsEnableFilter, 'create_time',)
    list_per_page = 30
    search_fields = ('job_name', 'work_year', )
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username', )

    class Media:
        js = (
            '/static/plugins/kindeditor-4.1.10/kindeditor-all-min.js',
            '/static/plugins/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/plugins/kindeditor-4.1.10/config.js',
        )
