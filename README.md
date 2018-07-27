## Steam-Spider

`Python`实现的`Steam`爬虫，能够爬取`Steam`上的游戏、软硬件和捆绑包等信息，并保存为csv文件。目前爬取的信息包括：ID、名称、发布日期、折扣、原价以及当前价格。兼容`Python2`和`Python3`

### 依赖

代码的实现依赖以下Python库

- `bs4`
- `requests`
- `timeout_decorator`
- `multiprocessing`

### Usage

``` bash
python steam_spider.py
```
不加参数执行上述命令将以单线程爬取Steam上的全部内容，并保存为CSV文件。

### 参数

- `-c`

    待爬取的`Steam`类别，目前支持的类别有：

    - `Game`      (游戏)
    - `Software`  (软件)
    - `Hardware`  (硬件)
    - `DLC`       (可下载内容)
    - `Demo`      (游戏试玩)
    - `Video`     (视频)
    - `Trailer`   (宣传片)
    - `Bundle`    (捆绑包)
    - `Mod`       (模组 并非创意工坊Mod)
    - `All`       (以上全部内容)

    例如：
    ``` bash
    python steam_spider.py -c DLC
    ```
    将获取Steam上当前区域下全部DLC信息

- `-j`

    使用的线程数，例如：
    ``` bash
    python steam_spider.py -j 8
    ```
    将以8线程对Steam上的信息进行爬取

- `-o`
    
    指定输出文件名，默认为`steam_message.csv`

- `-l`

    指定输出语言，默认为`english`
