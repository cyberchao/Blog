本项目是工作之余学python时做的web项目

> 基于Django2.1，Python3.6.5，mysql8.0的个人博客，运行于nginx1.16+uwsgi+docker，主机设在美国洛杉矶，图床和媒体数据位于阿里云oss

#### 主页：

![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216151113.png)

#### 功能：

1. 注册登录，验证过注册邮箱才可以登录

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216145128.png)

2. 多级评论功能(登录过的用户才可以评论)

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216145426.png)

3. 修改用户资料

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/1581836136946.png)

4. 多级分类，标签云

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216145814.png)

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216145732.png)

5. 以来访用户的ip作为标识，防止刷新文章阅读数就加一

6. 支持分页，并控制分页显示最大5页

7. 归档

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216150143.png)

8. 听音乐

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216150249.png)

9. 上传音乐

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216150352.png)

   10.离线下载和私人云盘是github上另外两个独立的工具，这里只是入口方便使用。

   ![](https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/倾听/20200216150540.png)

   顺便推荐一下我用的这两款工具：

   - [cloud-torrent](https://github.com/jpillora/cloud-torrent):  一款基于go的离线下载工具，非常轻便易部署
   - [nextcloud](https://nextcloud.com/)：非常受欢迎的一个私人云盘项目，我运行在树莓派上
