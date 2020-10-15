# Generated by Django 3.0.7 on 2020-10-15 17:13

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_mysql.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='姓名')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号')),
                ('avatar', models.CharField(blank=True, default='/media/default/avatar.png', max_length=1000, null=True, verbose_name='头像')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Dict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
                ('is_deleted', models.BooleanField(default=False, help_text='删除标记', verbose_name='删除标记')),
                ('name', models.CharField(max_length=1000, verbose_name='名称')),
                ('code', models.CharField(blank=True, max_length=30, null=True, verbose_name='编号')),
                ('fullname', models.CharField(blank=True, max_length=1000, null=True, verbose_name='全名')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('other', django_mysql.models.JSONField(blank=True, default=dict, null=True, verbose_name='其它信息')),
                ('sort', models.IntegerField(default=1, verbose_name='排序')),
                ('is_used', models.BooleanField(default=True, verbose_name='是否有效')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Dict', verbose_name='父')),
            ],
            options={
                'verbose_name': '字典',
                'verbose_name_plural': '字典',
            },
        ),
        migrations.CreateModel(
            name='DictType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
                ('is_deleted', models.BooleanField(default=False, help_text='删除标记', verbose_name='删除标记')),
                ('name', models.CharField(max_length=30, verbose_name='名称')),
                ('code', models.CharField(max_length=30, unique=True, verbose_name='代号')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.DictType', verbose_name='父')),
            ],
            options={
                'verbose_name': '字典类型',
                'verbose_name_plural': '字典类型',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
                ('is_deleted', models.BooleanField(default=False, help_text='删除标记', verbose_name='删除标记')),
                ('name', models.CharField(max_length=60, verbose_name='名称')),
                ('type', models.CharField(choices=[('公司', '公司'), ('部门', '部门')], default='部门', max_length=20, verbose_name='类型')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Organization', verbose_name='父')),
            ],
            options={
                'verbose_name': '组织架构',
                'verbose_name_plural': '组织架构',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
                ('is_deleted', models.BooleanField(default=False, help_text='删除标记', verbose_name='删除标记')),
                ('name', models.CharField(max_length=30, verbose_name='名称')),
                ('type', models.CharField(choices=[('目录', '目录'), ('菜单', '菜单'), ('接口', '接口')], default='接口', max_length=20, verbose_name='类型')),
                ('is_frame', models.BooleanField(default=False, verbose_name='外部链接')),
                ('sort', models.IntegerField(default=1, verbose_name='排序标记')),
                ('method', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='方法/代号')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Permission', verbose_name='父')),
            ],
            options={
                'verbose_name': '功能权限表',
                'verbose_name_plural': '功能权限表',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
                ('is_deleted', models.BooleanField(default=False, help_text='删除标记', verbose_name='删除标记')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='名称')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '职位/岗位',
                'verbose_name_plural': '职位/岗位',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
                ('is_deleted', models.BooleanField(default=False, help_text='删除标记', verbose_name='删除标记')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='角色')),
                ('datas', models.CharField(choices=[('全部', '全部'), ('自定义', '自定义'), ('同级及以下', '同级及以下'), ('本级及以下', '本级及以下'), ('本级', '本级'), ('仅本人', '仅本人')], default='本级及以下', max_length=50, verbose_name='数据权限')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='描述')),
                ('depts', models.ManyToManyField(blank=True, to='system.Organization', verbose_name='权限范围')),
                ('perms', models.ManyToManyField(blank=True, to='system.Permission', verbose_name='功能权限')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
            },
        ),
        migrations.CreateModel(
            name='HistoricalDict',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(blank=True, editable=False, help_text='修改时间', verbose_name='修改时间')),
                ('is_deleted', models.BooleanField(default=False, help_text='删除标记', verbose_name='删除标记')),
                ('name', models.CharField(max_length=1000, verbose_name='名称')),
                ('code', models.CharField(blank=True, max_length=30, null=True, verbose_name='编号')),
                ('fullname', models.CharField(blank=True, max_length=1000, null=True, verbose_name='全名')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('other', django_mysql.models.JSONField(blank=True, default=dict, null=True, verbose_name='其它信息')),
                ('sort', models.IntegerField(default=1, verbose_name='排序')),
                ('is_used', models.BooleanField(default=True, verbose_name='是否有效')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='system.Dict', verbose_name='父')),
                ('type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='system.DictType', verbose_name='类型')),
            ],
            options={
                'verbose_name': 'historical 字典',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
                ('is_deleted', models.BooleanField(default=False, help_text='删除标记', verbose_name='删除标记')),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='名称')),
                ('size', models.IntegerField(blank=True, default=1, null=True, verbose_name='文件大小')),
                ('file', models.FileField(upload_to='%Y/%m/%d/', verbose_name='文件')),
                ('mime', models.CharField(blank=True, max_length=300, null=True, verbose_name='文件格式')),
                ('type', models.CharField(choices=[('文档', '文档'), ('视频', '视频'), ('音频', '音频'), ('图片', '图片'), ('其它', '其它')], default='文档', max_length=50, verbose_name='文件类型')),
                ('path', models.CharField(blank=True, max_length=1000, null=True, verbose_name='地址')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_update_by', to=settings.AUTH_USER_MODEL, verbose_name='最后编辑人')),
            ],
            options={
                'verbose_name': '文件库',
                'verbose_name_plural': '文件库',
            },
        ),
        migrations.AddField(
            model_name='dict',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.DictType', verbose_name='类型'),
        ),
        migrations.AddField(
            model_name='user',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.Organization', verbose_name='组织'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.ManyToManyField(blank=True, to='system.Position', verbose_name='岗位'),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, to='system.Role', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='user',
            name='superior',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='上级主管'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='dict',
            unique_together={('name', 'is_used', 'type')},
        ),
    ]
