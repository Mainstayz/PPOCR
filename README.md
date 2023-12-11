
## 安装 paddle OCR

https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/linux-pip.html

### 安装主模块

`conda install paddlepaddle==2.5.2 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/`

### 安装 OCR 模块

https://zhuanlan.zhihu.com/p/638836038

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

CPU：
conda install paddlepaddle==2.5.2 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/





## Windows VSC 激活 Conda 环境异常

解决方案：

開啟權限:使用Windows PowerShell，輸入下列命令後再輸入

```
set-executionpolicy remotesigned
```

或者輸入，我自己是兩個都有輸入

```
Set-ExecutionPolicy RemoteSigned -Force
```

2. 初始化conda:使用Anaconda PowerShell Prompt，輸入下列命令

`conda init`

3. 確認路徑:我會建議兩處星號的Path都必須要有打勾的三項
4. 重啟VS code:搞定
