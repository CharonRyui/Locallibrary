# 创建django项目

* 使用django-admin startproject ........  来创建一个项目，这里是locallibrary
  * \_\_init\_\_用于标识文件夹为项目
  * urls是url到view方法的对应，但是一般实现文件里也会有相应的配置
  * wsgi是和数据库交换的必要文件
  * asgi兼容了wsgi并且可以实现异步交流
* 使用python manage.py startapp .........  来创建一个应用，这里是catalog
  * views是在url中收到指令后call的函数
  * apps应用注册
  * admin是网站管理配置
  * models是和sql的交互
* 需要把这个新加入的app注册到settings，app的名字就是apps.py里的class名称
* 更新url映射
* 数据库迁移，使用python manage.py migrate，每次model发生改变都需要运行
* django有强大的运行debug，出现错误时会显示合理的错误信息

# 模型

* 在models.py中编辑

* 在指明数据库类型后，django会自行和数据库沟通

* 对于数据库的数据，django提供了常见的参数和类型

  1. 参数

     * help_text

     * verbose_name：别名

     * default：默认值

     * null：是否自动把可以填为null的值填为null

     * blank：是否允许留空

     * choices：提供和标准文本属性不同的选项
       * 提供的choices应该是一个元组
         * 元组的内容是一对对的键值二元组
         * 其中第一个是写入的choices，第二个是其含义（实际储存的）

     * unique：是否不能重复

     * primary_key

  2. 类型

     * CharField：指定最大长度的文本
     * Text
     * Integer
     * Date和DateTimeField
     * Email
     * File和Image：可以上传文件
     * Auto：也是一个整数，但会自动添加主键
     * ForeignKey：*没有Field后缀* ，用于指定一对多关系，也有on_delete等参数
       * on_delete默认是cascade，一并删除
       * 使用restrict保证存在引用时，外键数据不会被先删除
       * 外键指定的类可以使用字符串，会避免所有的语法检查
     * ManyToMany：指定多对多关系，有on_delete等参数指定关联数据被删除时的行为等

* 可以指定MetaData

  * 用于指定默认排序等
  * 指定表别名
  * 声明访问权限
  * 声明abstract模型

* 可以定义方法

  * 必须要有 \_\_str\_\_方法来返回可读的数据库内容
  * get_absolute_url返回展示的数据的路径

* 数据保存

  * 调用save方法
  * 每次修改记录对象的属性（数据库条目）时需要令改记录对象调用

* 如果没有建立主键，会自动创建id这一栏作为主键

* 查询

  * 需要一个QuerySet对象，使用库.objects.all或filter等方法获得
  * QuerySet对象提供了方法，如count等
  * filter的使用
    * field_name__match_type
      * fieldname是某个需要匹配的属性，match_type有contains，iexact（i是不区分大小写），startswith等
      * 如果匹配的属性是一个外键等多对象，可以再使用双下划线指定对象的属性
        * 如genre\_\_name\_\_icontain
        * 且此方法可以多深度

# 管理员站点

* 在admin.py中编辑
* django的管理员应用可以创建站点来对数据库增删改查
* 必要的包含操作已经在创建项目处完成了，只需要添加模型并注册
* 在admin.py中使用admin.site.register(model_name)来注册
* 允许python manage.py createsuperuser来创建管理账户
* 使用python manage.py runserver启动项目，并登录ip:port/admin界面
* 如果定义了get_absolute_url在编辑界面会出现view on site按键
* 此界面有强大的可自定义性
  * 在admin.py中定义类model_nameAdmin(admin.ModelAdmin)
    * 成员list_display：在库中展示时显示的数据
      * 多对多无法直接显示，需要传入一个方法名称，此方法定义在模型的定义中
    * list_filter：添加过滤器
    * fields：在详情界面中并列（默认所有属性垂直排列）
    * exclude：在详情界面中看不到
    * fieldsets：将属性分块
      * 是一个元组
      * 每一个元组元素是一个二元组
      * 二元组的第一个元素是块名，第二个元素是一个对象，{'fields':TUPLE}
      * 里面的TUPLE是变量名元组
    * inlines：可以在此直接修改关联的其他属性，是一个数组
      * 需要定义另一个类ModelNameInline(admin.TabularInline)
      * 其中的model属性为需要ModelName
      * extra属性可以指定占位数据的个数（默认3个）
  * 注册时额外传入此类作为第二个参数

# 创建主页

* 页面的创建需要url map，view和template

## url

* path：三个参数，第一个为匹配模式，第二个为调用的view方法，第三个为url的名字
  * 名字在html中被使用，href="{% url URLNAME %}"

## view

* view负责和数据库交互获得数据，使用html模板修饰渲染页面并回复http
* views.py引入了render来渲染html页面
* render接收参数
  1. request：http请求，一般在view处接收
  2. template：渲染的html模板
  3. context：一个Python字典，包含需要被传入模板中占位符的数据

## template

* 使用startapp创建的应用会在templates文件夹下寻找模板
* 可以将css等静态文件放置在static/css下，static是默认的load路径
  * load还可以用于上传本地文件
  * 事实上这里的静态路径在项目名下的urls里被static方法指定
* 允许使用extends继承基础模板，并用block/endblock表明替换父模板的部分
* template中有某些模板标签可以实现特殊功能如插入实际值，循环遍历等
  * 一般插值是{{  }}，模板标签是{%  %}

# 添加页面

* 在一个应用下的urls.py中写的url默认有改应用的文件夹前缀
* view可以通过类的方式被定义
  * 需要调用as_view方法来作为view函数使用
  * 引入generic from django.views
  * 定义一个类，继承ListView
    * 其中的model属性为所使用的模型
    * ListView模型会遍历整个数据库，找到该模型的数据并在templates/APPNAME/MODELNAME_list.html的渲染下返回页面
    * 也可以使用template_name属性手动指定路径
    * paginate_by参数用于指定分页
      * 其值为每页的最大数量
      * 需要访问其他页面时，应添加url为/?page=XXX
      * 这在数据量大的情况下可以加快加载而不只是显示问题
      * 当使用了分页时
        * 方法is_paginated会返回true
        * 存在内置的page_obj对象来控制分页操作
          * 此对象拥有has_previous等方法
          * 以及number等属性
      * 一个常见的路径跳转方法是结合request这一页面自带的对象
        * href='{{request.path}}?page={{page_obj.next_page_number}}'
  * 可以重写generic中的类的方法
    * 比如as_view
* 模板标签的逻辑控制
  * if，else，elif，endif：条件控制
  * for VAL in LIST，endfor：循环控制
    * empty：如果LIST是空的则执行
    * for中还提供了许多变量，比如forloop.last记录最后一次循环进程
* 在模板中使用get_absolute_url获取详细时无法传入参数
* url中的模型匹配，使用尖括号，里面是TYPE:VAL
  * 对，还可以在匹配里面定义名称
  * 如果使用了generic的模型，默认的变量名称是pk（short for primary-key）
* 需要更详细的匹配建议使用re_path
  * 三个参数，和path含义相同
  * 字符串的匹配部分中，字符串需要使用raw string，即r'TEXT'
    * r'^book/(?P<pk>\d+)$‘：匹配book/NUMBER，并把后面的数字作为pk传回
    * r'^book/(\d+)$'：一样的，但是数字是匿名的变量
    * r'^book/(?P<stug>[-\w]+)$'：匹配book的后面是char和-的结合
* path有一个可选参数为一个字典，可以传入参数
  * 如果url捕捉和此处的变量名重复了，那么最后的值会是字典中的（字典在url的后面写的嘛）
* generic.DetailView父类处理了不存在的情况（也可以自定义），如果自己用view方法，需要try except来错误处理Http404
  * 或者使用提供了的get_object_or_404方法来获取
  * 否则默认的query行为会自动带有错误处理
* 如果有一个“many”的属性，并且没有定义获取方式，django会自动分配一个方法
  * 方法的名称为FIELDNAME_set，其中属性名是全小写的
  * 使用XXX_set.all来获取数据集合
  * 但是其中的排序如果没有在Meta里面指定并在无法使用filter或sort_by的插值中使用会因无法确定顺序而收到警告
    * 也就是说，model和view中至少有一者定义了数据的返回顺序
    * 在meta中定义ordering或者在queryset或get_queryset中使用order_by
    * 无声明情况下使用主键排序，但是可能出现警告
* 如果某一个属性被指定为choices，django也会自动分配一个查询方法
  * 方法名为get_FIELDNAME_display

# 会话框架

* 会话可以用来保存特点的网页状态
* django使用一个包含会话id的cookie来识别会话
  * 而实际的会话数据保存在网站的数据库中而非cookie中
  * 可以手动改变配置保存在cookie、文件或者缓存等地方
* 在setting中的django.contrib.sessions和middleware中包含了相关配置
* 使用request.session['FIELDNAME']来获取当前http请求对象的session值
  * request.session.get('FIELDNME',DEFAULTVALUE)可以在获取的同时设置默认值（如果不存在）
  * del requst.session['FIELDNAME']来删除这个会话属性
* django会自动对session中属性的改变做保存
  * 但是如果属性中还有属性，这个更改不会被检测到
  * 需要手动使用request.session.modified = True来设置保存
  * 可以将settings中的SESSION_SAVE_EVERY_REQUEST = True开启，则每次网页发送请求都会更新会话属性

* 在view方法中添加相关的属性获取
* _似乎session属性的创建除了在定义和更改时使用和session有关的方法，使用上和一般的view变量并没有什么区别_

# 用户认证

* *django提供了基础的认证服务，但是更多的服务需要第三方包（如第三方登录、节流等）*
  * 本次使用django提供的stock认证服务
  * 通过使用API，认证服务可以非常地灵活，建立url、表、views、模板等等
* 使用django-admin startproject的时候自动配置了支持认证的配置，并在第一次使用imigrate的时候创建了用户和数据的数据库表
  * 即settings.py中的INSTALLED_APPS内的django.contrib.auth和django.contrib.contenttypes
  * 由于认证基于会话，所以需要MIDDLEWARE中的SessionMiddleware和AuthenticationMiddleware
* 创建django数据库的时候需要添加一个root用户（即使用python manage.py createsuperuser）
  * 可以使用superuser创建普通用户
  * 也可以在代码中创建用户，使用django.contrib.auth.models中的User
    * User.objects.create_user(INFOMATION)的返回值是一个新的用户
    * 可以使用.语法来给用户的其他属性赋值
    * 最后使用User对象的save()方法保存
    * 可以定制一个User的model，使用django.contrib.auth中的get_user_model获取这个User子类
      * 然后令User = get_user_model()
      * 此后该User是一个自定义的User而非默认models中的User
* django提供了认证的url、view、表，但是没有提供模板，需要自己创建template
* 在urls.py中加入一个指向include('django.contrib.auth.urls')的path
  * 但是需要使用accounts作为url标签
  * django提供了内置的许多以accoun-ts/开头的url来支持认证操
    * 并且单个这个accounts是不可访问的
  * 其中的url会在registration/下寻找对应名称的template
    * 这个registration所在的templates文件夹需要在根目录下（即和catalog同级）
    * 创建文件夹后需要在setting.py中注册
      * 在TEMPLATES中的‘DIRS'内添加os.path.join(BASE_DIR, 'templates')
      * 'APP_DIRS'设置为True
  * 默认的登录成功会重定向到accounts/profile
    * 可以在settings.py中修改LOGIN_REDIRECT_URL
* 由于django不允许使用GET来跳转到logout界面，需要使用form跳转
  * 也需要一个logged_out.html来提供登出成功界面的渲染
  * 通常使用一个button来提交form，但是有的渲染中提供了相关的css将其伪装为一个link
    * 如使用class="btn btn-link"
* 默认的密码修改需要填入一个mail地址，发送邮件认证
  * 并且需要添加password_reset_form.html和password_reset_done.html
  * 需要password_reset_email.html来提供邮件的页面
    * 但是现在的项目中还不支持发送邮件，无法实现效果
    * 可以打印在控制台上实验
    * 在settings.py中添加：EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
  * 需要password_reset_confirm.html来输入新的密码
  * password_reset_complete.html提示重置成功
* 可以根据用户的认证情况展示页面
  * 在{%%}中可以使用user.来查看当前的用户情况
  * 在view中，在view方法前使用@login_required即可
    * 此方法在未登录时会自动重定向
    * 目标是settings.py中的LOGIN_URL
    * 并且将现在的URL设置为next以便于登陆后重定向回当前页面
    * 也可以使用request.user.is_authenticated，但是显然麻烦
  * 在class-based的view中，继承LoginRequiredMixin是最简单的限制方法
    * 默认情况下采用和login_required修饰符相同的定向行为
    * 可以在本view类中使用login_url指定登录路径
    * redirect_field_name来指定重定向目标
* 在models.py中import django.conf里的settings，其中的AUTH_USER_MODEL可以用作默认user类
  * 也可以直接在django.contrib.auth.model中导入User类，以及自己的定义
* 权限
  * 默认的对model的权限为添加，修改，删除
  * 可以自定义对其的操作权限并赋予特点用户
  * 在Meta中定义权限
    * 使用permission = ((PERMISSION_NAME, PERMISSION_CONTENT), (), () ...)来添加权限
  * template里的perms属性储存了权限，调用对应的权限名返回是否有此权限
  * view中使用permission_required(PERMISSION_NAME)修饰符来要求调用权限
    * 如果是class-based的view，在类中的permission_required = (PERMISSON_NAME1, PERMISSON_NAME2 ...)中指定需要的权限
    * 默认下，修饰符重定向到登录界面，而class-based的重定向是403
      * 如果希望修饰符达到同样的效果，使用@permission_required(P_N, raise_exception=True)

# 表单

* django的表单提交同样将信息提交到request对象，并调用相应的view
  * 处理信息后将相关的渲染完成的页面返回
  * 但是在信息不合法的时候需要做出判断并通知
* django的表单处理主要负责
  1. 在表单被申请时展示表单（可能包含空值与非空值）
     * 这些值可能是默认的或者查询等操作所出现的原有值
     * 此时表单不和用户的数据相关联
  2. 接收用户的输入信息，并把信息和表单进行关联
     * 关联过程关联了错误和信息
     * 这些错误和信息可以在需要的时候被重新展示
  3. 处理（过滤）用户的输入信息，使其不会危害数据库，并转化为python的类型
  4. 如果发现了不合法的数据，需要重新返回并展示表单（以及错误的原因和信息）
  5. 当数据合法时，执行要求的操作（保存、发送等）
  6. 重定向到页面
* django提供了许多相关的方法和类来提供对于上述操作的支持，典型的类是Form，也是django表单处理的核心
  * Form类规定了表单的元素排布、展示组件、标签、初始值、合法数值、错误信息等内容
  * 也提供了渲染和预定义格式的方法
  * 以及从特点位置获取数值的方式
* 定义表单的方式和定义model差不多，需要import forms，并创建一个类继承forms.Form
  * 通常表单的类名是XXXForm
  * 通常将表单放置在forms.py下（和views..py同级）
* 表单中的数据类型由django提供
  1. BooleanField
  2. Char
  3. Choice
  4. TypedChoice
  5. Date
  6. Datetime
  7. Decimal
  8. Duration
  9. Email
  10. File
  11. FilePath
  12. Float
  13. Image
  14. Integer
  15. GenericIPAddress
  16. MultipleChoice
  17. NullBoolean
  18. Regex
  19. Slug
  20. Time
  21. URL
  22. UUID
  23. Combo
  24. MultiValue
  25. SplitDateTime
  26. ModelMultipleChoice
  27. ModelChoice
* 默认情况下，一个xxx_xxx的表单field，会被赋予标签Xxx xxx，并且使用默认的相应widget进行渲染
* 这些Field在创建的同时同样接收参数，以下是一些常见的参数
  1. required：如果是True，不能留空，默认是True
  2. label：自定义一个label名称，如果没给出，那么django会将变量名的第一个字母大写，并把下划线替换为空格作为默认的label
  3. label_suffix：label的后缀，允许存放其他字符
  4. initial：初始值
  5. widget：渲染时使用的widget
  6. help_text
  7. error_message：一个list，包含了错误信息，可以在里面重写默认的错误信息
  8. valildators：一个list，里面是一些function会在对数据合法化操作时被调用
  9. localize：允许对field输入数据的localization
  10. disabled：如果是True，这一项field的内容无法被改变
* 数据合法化处理
  * 可以重写clean_FIELDNAME()方法来validate一个field
  * 还有许多其他的方法，如重写Form.clean()
* 使用form的view需要渲染默认的表单并在填入不合法信息时重新渲染
  * 最简单的判断提交方式是通过request.method=='POST'来判断重渲染，而GET是默认渲染
  * 另一种方法是读取表单数据，如某些隐藏数值来作为修改过的依据
* 在view中可以使用request.POST['FIELD_NAME']来获取表单内容，但是使用cleaned_data[]获取到的数据是validated的、python friendly的
* 所有的POST上传都应该先使用{% csrf_token %}生成密钥防止恶意上传
  * 在template中可以使用FORM_VAR_NAME.as_form或as_ul等方式自动渲染表单
* ModelForms
  * django提供了简单的表单用于提交一个model的相关数据
  * 继承ModelForm类
  * 在meta中指定meta和需要的fields即可
    * 需要所有可以使用 fiels = '\_\_all\_\_'
    * 或者用exclude而不是fields来排除部分field
    * 但是上述两种方式都不推荐，因为新加入model的field总是被自动添加到表单
  * 在其中定义 clean_FIELD_NAME方法来创建validation checker
* django还提供了FormView来提供自动的检测操作，只需要自己提供对合法数据的处理即可
* 对于一般的增删改查操作，django同样提供了generic view，而不需要自己提供表单或是FormView
  * update和create中的success_url是对应model的DetailView页面，而delete默认没有
  * create和update的默认template都在PROJECTNAME/templates/PROJECTNAME/MODEL_NAME_form.html
    * 可以把_form这个后缀改为其他的，只需要在方法里定义template_name_suffix为其他值
  * delete的默认模板叫MODEL_NAME_confirm_delete.html

# 网站测试

* 网站规模的扩大会使得各个页面的单元检测难以完成，django提供了根据网页的更新自动进行的测试
* 测试的几种常见种类
  1. 单元测试：测试单个组件的正常运行，一般是类或方法级别
  2. 回归测试：重新测试发生过的bug，确认原来的代码已经正确并且后面的代码没有同样的问题
  3. 集成测试：将组件整合进行测试，主要目标是各个组件之间的互动，可能涉及组件的分组
  4. 其他：如黑箱、白箱、人工、自动、金丝雀、烟雾、一致性、接受性、压力等等测试
* django通过unittest库提供了单元测试和整合测试的方法
  * 通过继承相关的父类，在类下创建setUp、tearDown等方法可以实现测试
  * 最基本的测试类是TestCase
    * TestCase在运行时创建一个干净的数据库
    * 所有测试基于和这个临时的数据库的交互
    * 此类也提供了一系列方法模拟客户端行为
    * 但是由于数据库的创建消耗资源和时间，在某些情况下并不高效
  * 测试内容：所有有关设计逻辑的地方
    1. 数据长度（定义Char_Field时的max_length）
       * 通常数据的合理性会在提交表单的时候检测
    2. get_absolute_url等方法是否按照希望运作并返回结果
    3. 表单中的字段是否都具有
       * 此时的表单字段需要使用fields['FIELD_NAME']获取
       * 如果字段未被赋予值时，label也会是None
    4. 测试view的内容需要使用Django test Client来模拟GET和POST方法
       * 使用self.client.get(URL)来请求网站，使用view
    5. 对于有登录需求的网站，可以使用User来创建测试用户，并且使用get到的HTTP回应中的user相关数据来确认登录情况
    6. 通常需要确认权限是否被正确地限制
    7. 表单的数据是否被正确地validated了
  * 建议使用一个tests目录，在下方建立test_TESTCONTENT.py文件
  * 使用python manage.py test开启测试
    * 使用 --verbosity NUM来指定测试信息的详细程度，0最少，3最多，默认是1
    * 使用 --parallel auto 来开启并行测试，auto可以改为线程数量
    * 可以在test后指定test的文件或目录名称或方法名称来指导运行的测试文件或方法
    * 使用 --shuffle来进行洗牌测试
    * 使用 --debug-mode开启debug模式，将结果记录在python的logger中
  * 在一个继承了TestCase的类中
    * setUpTestData(cls) 方法在类级创建时被调用，使用它来创建对象
    * setUp(self)方法在每次测试方法被调用时被调用，创建可以被测试方法改变的对象
    * 使用assertEqual而不是assertTrue(XXX==XXX)，尽量让报错信息更可读
  * 可以使用Coverage测试工具来提示应该测试哪些内容
  * Selenium提供了系统测试（整合测试的下一个阶段）的框架

# 产品化和部署

* 在托管网站之前，需要
  1. 更改一些项目设置
  2. 选择运行django应用的环境
  3. 选择运行静态文件的环境
  4. 为网站服务建立生产级的服务框架
* 产品环境：由服务器主机提供的运行环境，包括了
  * 网站运行的电脑硬件
  * 操作系统
  * 编程语言和库
  * 在网页和服务器之间传递动态请求的应用服务器
  * 网站依赖的数据库
  * 其他组件：如逆向代理，传输平衡器等
* 云服务分为三种
  * IaaS：在提供的硬件上建立自己的环境并提供实现
  * PaaS：在提供的环境上提供自己的实现，即不用考虑服务器架构
  * SaaS：用户直接获取的服务，不需要任何实现，只需要贴上自己的标记即可
* django创建项目时的settings.py有许多设置是为了便于开发，在实际发布和产品化之前需要更改
  * 有一个为了产品化的额外的settings文件并不罕见
  * 但是即使整个网站都是开源的，通常这个因为产品化而产生的settings文件不应该被暴露在库中
* 一些关键的属性
  * DEBUG：debug模式，在产品中需要被设置为False
  * SECRET_KEY：决定CSRF防御机制的随机数字等，这个key不可以被外部获取
* django文档建议，秘密的数据应该被设置为环境变量或者从某些设置了权限的文件中读取
  * 这里，使用python dotenv来读入一个.env文件配置环境
  * 所有在.env中的文件都应该是秘密的，把他们添加到gitignore里！
* 使用python manage.py check --deploy来检查可能存在的安全问题
* Gunicorn：一个纯粹的python的HTTP服务器
* django的数据库配置会在一个环境变量DATABASE_URL里保存
  * 通常使用dj-database-url包让django项目从此环境变量中读取配置数据

* 可以先下载包来使得上到的服务器需要具有相关的配置
* 在开发过程中的静态文件数据需要经过django进行渲染，这在服务器上会显得非常低效
  * 通常将静态文件和django应用分开
  * 静态文件在template中使用static等关键字来说明链接到静态文件
  * 使用python manage.py collectstatic来重新指定静态文件，django会在settings.py中指定的静态文件路径来获取相关文件
  * 实际的配置过程通常使用Whitenoise库来实现
    * 在下载了Whitenoise后，在MIDDLEWARE中添加whitenoise.middleware.WhiteNoiseMiddleware
    * 并在STORAGES中设定相关的配置

* 所有对于服务器的配置需求应该被记录在仓库root路径中的requirements.txt中
  * 使用pip freeze > requirements.txt来记录python配置需求

