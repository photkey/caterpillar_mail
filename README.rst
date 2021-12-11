caterpillar_mail
================

caterpillar_mail 简介
---------------------

caterpillar_mail
主要为收发邮件、解析邮件做的进一步高层封装，使用起来极其方便，追求极简的编码方式

caterpillar_mail 安装方式
-------------------------

.. code:: bash

   pip install -U caterpillar_mail

caterpillar_mail 使用说明
-------------------------

发送邮件
~~~~~~~~

如下，总共三行代码，即可实现邮件发送，目前已支持的邮箱类型见
`当前已支持的邮箱类型 <email_suffix_to_server.json>`__\ ，如需新增类型请提issue

.. code:: python

   from caterpillar_mail import Email

   # 初始化对象，初始化参数为发件箱及授权码
   email=Email(username="hitredrose@163.com",auth_code="LRRDUxxxxEMLK")
   # 发送邮件，第一个参数为收件人地址，第二个邮件标题，第三个标题为邮件内容
   email.send(to_addrs="redrose2100@163.com",subject="发送邮件测试标题",context="你好啊\n哈哈哈\n我是用来测试邮件的！")

发送邮件带单个文件

.. code:: python

   from caterpillar_mail import Email

   email=Email(username="hitredrose@163.com",auth_code="LRRDxxxxxxxEMLK")
   email.send(to_addrs="redrose2100@163.com",subject="发送邮件测试标题",context="你好啊\n哈哈哈\n我是用来测试邮件的，而且带附件！",attach="G:/src/caterpillar_mail/dist/caterpillar_mail-1.0.9.tar.gz")

如果发送邮件的附件为多个，中间使用逗号分隔

.. code:: python

   from caterpillar_mail import Email

   email=Email(username="hitredrose@163.com",auth_code="LRRDxxxxxxxEMLK")
   email.send(to_addrs="redrose2100@163.com",subject="发送邮件测试标题",context="你好啊\n哈哈哈\n我是用来测试邮件的，而且带附件！",attach="G:/src/caterpillar_mail/dist/caterpillar_mail-1.0.9.tar.gz,E:/private/title.png")

如果收件人为多人时，收件人使用逗号分隔

.. code:: python

   from caterpillar_mail import Email

   # 初始化对象，初始化参数为发件箱及授权码
   email=Email(username="hitredrose@163.com",auth_code="LRRDUxxxxEMLK")
   # 发送邮件，第一个参数为收件人地址，第二个邮件标题，第三个标题为邮件内容
   email.send(to_addrs="redrose2100@163.com,redrose2200@163.com",subject="发送邮件测试标题",context="你好啊\n哈哈哈\n我是用来测试邮件的！")

接收解析邮件
~~~~~~~~~~~~

获取最新的邮件并解析
^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from caterpillar_mail import Email

   email=Email(username="redrose2100@163.com",auth_code="XTSDDxxxxxxZBIO")
   obj = email.get_latest_email()
   print(obj.from_name)   # 发件人名字
   print(obj.from_addr)   # 发件人邮箱
   print(obj.to_name)     # 收件人名字
   print(obj.to_addr)     # 收件人邮箱
   print(obj.date)        # 邮件时间
   print(obj.subject)     # 邮件标题
   print(obj.context)     # 邮件内容

通过邮件标题过滤，查询符合过滤条件的最新的邮件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from caterpillar_mail import Email

   email=Email(username="redrose2100@163.com",auth_code="XTSDDxxxxxZBIO")
   obj = email.get_latest_email(subject="测试邮件收发")
   print(obj.from_name)   # 发件人名字
   print(obj.from_addr)   # 发件人邮箱
   print(obj.to_name)     # 收件人名字
   print(obj.to_addr)     # 收件人邮箱
   print(obj.date)        # 邮件时间
   print(obj.subject)     # 邮件标题
   print(obj.context)     # 邮件内容

通过发件人过滤，查询符合过滤条件的最新的邮件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from caterpillar_mail import Email

   email=Email(username="redrose2100@163.com",auth_code="XTSDDNxxxxxxxBIO")
   obj = email.get_latest_email(from_addr="985224350@qq.com")
   print(obj.from_name)   # 发件人名字
   print(obj.from_addr)   # 发件人邮箱
   print(obj.to_name)     # 收件人名字
   print(obj.to_addr)     # 收件人邮箱
   print(obj.date)        # 邮件时间
   print(obj.subject)     # 邮件标题
   print(obj.context)     # 邮件内容

通过一个收件人过滤，查询符合条件的最新的邮件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from caterpillar_mail import Email

   email=Email(username="redrose2100@163.com",auth_code="XTSDDxxxxxZBIO")
   obj = email.get_latest_email(to_addr="redrose2200@163.com")
   print(obj.from_name)   # 发件人名字
   print(obj.from_addr)   # 发件人邮箱
   print(obj.to_name)     # 收件人名字
   print(obj.to_addr)     # 收件人邮箱
   print(obj.date)        # 邮件时间
   print(obj.subject)     # 邮件标题
   print(obj.context)     # 邮件内容

subject，from_addr，to_addr 三个参数均支持正则表达式，比如发件人使用正则过滤
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from caterpillar_mail import Email

   email=Email(username="redrose2100@163.com",auth_code="XTSDDNxxxxxBIO")
   obj = email.get_latest_email(from_addr="\d{9}")
   print(obj.from_name)   # 发件人名字
   print(obj.from_addr)   # 发件人邮箱
   print(obj.to_name)     # 收件人名字
   print(obj.to_addr)     # 收件人邮箱
   print(obj.date)        # 邮件时间
   print(obj.subject)     # 邮件标题
   print(obj.context)     # 邮件内容

caterpillar_mail 发布记录
-------------------------

1.1.0 发布日期：2021-12-11
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  增加对谷歌邮箱的支持以及可以发送带一个或者多个文件附件，文件格式不限，修复json数据文件

1.0.13 发布日期：2021-12-11
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  增加对谷歌邮箱的支持以及可以发送带一个或者多个文件附件，文件格式不限

1.0.12 发布日期：2021-11-22
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  解决获取邮件数量和最新邮件不实时同步的问题

1.0.11 发布日期：2021-11-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  增加对yeah.net邮箱的支持

.. _发布日期2021-11-19-1:

1.0.10 发布日期：2021-11-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  接收解析邮件提供更高层封装，两行代码即可接收解析邮件，同时发件人支持多人

1.0.9 发布日期：2021-11-18
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  发送邮件提供更高层封装，两行代码即可发送邮件，同时收件人支持多人

.. _发布日期2021-11-18-1:

1.0.8 发布日期：2021-11-18
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  增加QQ邮箱的发送和收取及解析操作

.. _发布日期2021-11-18-2:

1.0.7 发布日期：2021-11-18
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  格式化发布文档

.. _发布日期2021-11-18-3:

1.0.6 发布日期：2021-11-18
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  格式化发布文档

.. _发布日期2021-11-18-4:

1.0.5 发布日期：2021-11-18
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  增加126邮箱的读取和发送

.. _发布日期2021-11-18-5:

1.0.4 发布日期：2021-11-18
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  增加解析邮件内容

1.0.3 发布日期：2021-11-17
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  更新说明文档格式

.. _发布日期2021-11-17-1:

1.0.2 发布日期：2021-11-17
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  更新说明文档为.rst格式

.. _发布日期2021-11-17-2:

1.0.1 发布日期：2021-11-17
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  发送邮件功能
