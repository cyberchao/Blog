from django.urls import reverse
from froala_editor.fields import FroalaField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, Count
from mptt.models import MPTTModel, TreeForeignKey


"""
AbstractUser是一个完整的用户模型，包含字段，作为一个抽象类，以便您可以继承它并添加您自己的配置文件字段和方法。
AbstractBaseUser仅包含身份验证功能，但不包含实际字段：当您继承子类时，您必须提供它们。
如果您只是将事情添加到现有用户（即具有额外字段的配置文件数据），则使用AbstractUser是因为它更简单，更简单。
如果您想重新考虑一下Django关于认证的假设，那么AbstractBaseUser会为您提供这样的权力。
AbstractUser 类又继承自 AbstractBaseUser
"""


class Users(AbstractUser):
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to='profile_picture', default='/profile_picture/default.jpg')
    website = models.CharField(null=True, max_length=80, blank=True)
    github = models.CharField(null=True, max_length=80, blank=True)
    introduction = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def image_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url

    class Meta:
        verbose_name = '访客'
        verbose_name_plural = verbose_name
        db_table = 'Users'


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name
        db_table = 'Tag'


"""
查询集方法
>>> dir(TreeQuerySet)
['__and__', '__bool__', '__class__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__or__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_add_hints', '_batched_insert', '_chain', '_clone', '_combinator_query', '_create_object_from_params', '_db', '_earliest_or_latest', '_extract_model_params', '_fetch_all', '_fields', '_filter_or_exclude', '_for_write', '_has_filters', '_hints', '_insert', '_iterable_class', '_iterator', '_known_related_objects', '_merge_known_related_objects', '_merge_sanity_check', '_next_is_sticky', '_populate_pk_values', '_prefetch_done', '_prefetch_related_lookups', '_prefetch_related_objects', '_raw_delete', '_result_cache', '_sticky_filter', '_update', '_validate_values_are_expressions', '_values', 'aggregate', 'all', 'annotate', 'as_manager', 'bulk_create', 'complex_filter', 'count', 'create', 'dates', 'datetimes', 'db', 'defer', 'delete', 'difference', 'distinct', 'earliest', 'exclude', 'exists', 'explain', 'extra', 'filter', 'first', 'get', 'get_ancestors', 'get_cached_trees', 'get_descendants', 'get_or_create', 'in_bulk', 'intersection', 'iterator', 'last', 'latest', 'model', 'none', 'only', 'order_by', 'ordered', 'prefetch_related', 'query', 'raw', 'resolve_expression', 'reverse', 'select_for_update', 'select_related', 'union', 'update', 'update_or_create', 'using', 'values', 'values_list']

mptt实例方法
>>> dir(a)
['DoesNotExist', 'Meta', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD','_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_get_user_field_names', '_is_saved', '_meta', '_mptt_cached_fields', '_mptt_is_tracking', '_mptt_meta', '_mptt_refresh', '_mptt_start_tracking', '_mptt_stop_tracking', '_mptt_track_tree_insertions', '_mptt_track_tree_modified', '_mptt_tracking_base', '_mptt_updates_enabled', '_mpttfield', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_mptt_updates_enabled', '_set_pk_val', '_state', '_threadlocal', '_tree_manager', 'check', 'children', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_ancestors', 'get_blog_count', 'get_children', 'get_children_blogcount', 'get_deferred_fields', 'get_descendant_count', 'get_descendants', 'get_family', 'get_leafnodes', 'get_level', 'get_next_sibling', 'get_previous_sibling', 'get_root', 'get_siblings', 'id', 'insert_at', 'is_ancestor_of', 'is_child_node', 'is_descendant_of', 'is_leaf_node', 'is_root_node', 'level', 'lft', 'move_to', 'objects', 'parent', 'parent_id', 'pk', 'posts_set', 'prepare_database_save', 'refresh_from_db', 'rght', 'save', 'save_base', 'serializable_value', 'title', 'tree_id', 'unique_error_message', 'validate_unique']
"""


class Category(MPTTModel):
    title = models.CharField(max_length=20)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    # 一个model实例下关联的blog数量
    def get_blog_count(self):
        TreeQuerySet = Category.objects.annotate(Count('posts'))
        posts_values = TreeQuerySet.values()
        category = posts_values.get(title=self.title)
        return category['posts__count']

    # 如果本实例有children节点，计算本实例下所有后继节点关联的blog数量之和，
    # 否则是叶子节点，调用get_blog_count()方法
    def get_children_blogcount(self):
        node = Category.objects.get(title=self.title)
        if node.get_children().count():
            num = 0
            for n in node.get_descendants():
                num += n.get_blog_count()
            num += node.get_blog_count()
            return num if num else ''
        else:
            num = node.get_blog_count()
            return num if num else ''

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        db_table = 'Category'


class Posts(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = FroalaField()
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnail', blank=True, null=True)
    tags = models.ManyToManyField(to='Tag')
    views = models.ManyToManyField(to='Remote', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 增加一个字段后make时会提示2选1，选第一个，然后输入True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        db_table = 'Posts'

    # 可以根据blog对象的id生成格式为/blog/2的url，达到点击链接进入文章详情功能
    def get_absolutly_url(self):
        return reverse('blog_detail', kwargs={
            'id': self.id
        })

    def get_update_url(self):
        pass

    @property
    def get_comments(self):
        return self.comment.all().order_by('-timestamp')


class Remote(models.Model):
    ip = models.CharField(max_length=30)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = '客户端'
        verbose_name_plural = verbose_name
        db_table = 'Remote'
