# 说明

pull代码后需设置部分：  

1. 按照`语音识别模型`部分下载模型并解压  
2. 修改[api.py](https://github.com/jadeite777sea/-Speech_Recognition-/blob/master/backend/api.py)中的`SQLALCHEMY_DATABASE_URI`为自己的mysql数据库
3. 如果前端默认端口不为`8080`，在上一条位置附近修改`#跨域`相关端口
4. pip 安装缺少的python依赖
5. 启动前后端

## 目前进度

除了生成摘要部分基本完成

<!-- 前端目前效果：

![image-20240828202911054](C:\Users\岁月荒唐我不负你\AppData\Roaming\Typora\typora-user-images\image-20240828202911054.png)

主要是红色框中的发言按钮，其他都是空的。这里实现的比较简陋，是点击按钮开始发言，此时按钮会变成Stop Recording，再次点击会将这段时间的发言内容音频数据发送给后端。

后端的接口目前设为：<http://url:port/upload> 。然后目前传回后端的音频格式是WAV格式，这个可以后续调整为mp3等音频格式。由于目前只是测试能够成功传输并且内容是否一致。这里每次发言后的音频数据会进行覆盖（因为文件名设为了定值，后续可以更改）。 -->

## 语音识别模型

语音识别模型地址

[https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

找到    vosk-model-cn-0.22（1.3G）

和        vosk-model-spk-0.4  (13M 在最下面  Speaker identification model)

下载下来  都解压到  api.py同级目录   或者 更改api.py文件里的模型路径
