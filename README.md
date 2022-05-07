# ECRS——forLinux
### 基于深度学习的电商推荐系统（For Linux）
### 项目简介
#### 技术栈
>项目用到的技术如下：
>
>语言：`Python3` 
>
>模型训练： `PaddleRec` , `PaddlePaddle`
>
>深度学习模型:`DNN`, `DeepFM`
>
>向量召回：`milvus`
>
>数据存储： `Redis` 
>
>模型推理： `PaddleServing`
>
>模块通信：`gRPC`,`protobuf`

#### 系统推荐流程
在Youtube的二阶段推荐架构上拓展
![在这里插入图片描述](https://img-blog.csdnimg.cn/3cba81b9678b439d84eb257db4606ffa.png)

![](https://img-blog.csdnimg.cn/img_convert/1368467bec580f0e0c3943c80457edfb.png)
**(1)用户服务/商品服务。将实验用的数据集进行拆分，用户数据和商品数据各一份，数据经过解析保存到非关系型数据库Redis中，外部传入用户和商品的唯一id作为key到Redis中查找对应的value并以二进制流的形式将结果返回。**

**(2)召回服务。召回服务主要有三个任务，当系统中有新用户使用时，上述的用户信息库中无法查询该用户的信息。系统可以利用原有的用户信息训练的模型拟合新增用户，新用户会通过这个用户模型得到用户向量；为了完成召回任务，需要提前将所有商品信息通过商品模型转换成特征向量并导入Milvus中，同理，当有新商品上架时，执行上述步骤以便线商品可以及时的被推荐；最后把用户向量和 Milvus 库中的商品向量做近似搜索，返回只包含商品id信息的候选集列表。**

**(3)排序服务。召回阶段得到的候选集商品id列表通过商品服务查询商品的详细信息，然后与用户向量结合作为排序服务的输入，排序模型通过打分把所有候选待推荐的商品按分数从高到低排序，最后返回这个含有详细商品信息的推荐列表。**

![在这里插入图片描述](https://img-blog.csdnimg.cn/b0b9dfd402274bd6b7a78273a88007c2.png)
#### 快速开始
##### 项目部署依赖
Python3、PaddlePaddle2.2.2、PaddleServing、milvus1.0、redis

##### Linux命令面板执行以下命令
```shell
python3 -m pip install redis pymilvus==1.0.1 paddle_serving_app==0.3.1
sh prepare_server.sh 
sh start_server.sh  
```

##### 相关命令和文件说明
**prepare_server.sh**

> **line 1-2: 解压并启动 redis 服务** 

相关文件:```redis-stable.tar.gz```

>**line 3-6: 解压已经编译完成的 Milvus 源码文件并启动 Milvus 服务**

相关文件:```milvus_1.0.tar.gz```

>**line 8: 将商品数据和用户数据存入 redis 中。**

相关文件:执行脚本```to_redis.py```把```products.dat```和```users.dat```中的数据存入redis，请在执行脚本前将对应的文件放到根目录下

>**line 9: 将商品向量数据导入到milvus中**

相关文件:执行脚本```to_milvus.py```利用```milvus_tool/milvus_insert.py```将```product_vectors.txt```中的向量导入 Milvus 中。

**start_server.sh**

> **line 1-3: 打开```proto```文件夹并编译所有```.proto文件```** 

相关文件:执行```run_codegen.py```脚本利用```protoc```编译```um.proto``````cm.proto``````user_info.proto``````item_info.proto``````recall.proto``````rank.proto``````as.proto```文件解析生成py文件

>**line 4: 启动用户服务**

相关文件:执行```um.py```脚本查询用户信息(仅对老用户生效，新增用户不在此服务处理) 

**输入:** 用户```id ```**输出:** 存储在```redis```中该用户的完整信息，包括id、年龄、性别、所在城市等级、所在的省、市、区/县

**通信端口：```8910```**

>**line 5: 启动内容服务**

相关文件:执行脚本```cm.py```查询对应的商品信息

**输入:** 商品```id```**输出:** 存储在```redis```中该商品的完整信息，包括id、品牌、店铺id、所属品类

**通信端口：```8920```**

>**line 6: 启动召回服务**

相关文件:执行脚本```recall.py```调用```milvus_tool/milvus_recall.py```来召回商品集合中与用户向量相似的商品向量。用户向量通过```get_user_vector()```获取，
这样即使是新用户也可以为他推荐商品。

**输入:** 用户```id```**输出:** 召回排分top_k的商品id列表，显示每一个商品的id和预估分值

**通信端口：```8950```**
>**line 7: 启动排序服务**
 
相关文件:执行脚本```rank.py```将候选集商品与该用户进行更精准的打分。（该服务需要需要配合其他模块使用，如果单独执行此服务则使用默认参数，只返回一个结果）

**输入:** 用户信息和商品候选集  **输出:** 通过打分按照降序排列返回商品信息列表

**通信端口：```8960```**

>**line 8: 启动完整服务流程**
 
相关文件:执行脚本```as.py```将上述的几个服务进行串联，经过用户、召回、粗排序、精排序之后，直观地返回该用户的待推荐商品列表

**输入:** 新用户:完整用户信息 老用户:用户```id```**输出:** 由大到小排序的商品信息，每个商品信息包含了商品的id，品牌、店铺id和所属品类。

**通信端口：```8930```**


#### 结果演示示例
#### 服务展示

**应用服务**

```shell 
export PYTHONPATH=$PYTHONPATH:$PWD/proto
python client.py as 5.0 1.0 3.0 11.0 120.0 741.0 #年龄,性别, 所在市等级,所在省,市,区（县）
```
**输入**：输入一个新用户信息 

**输出**
```shell
error {
  code: 200
}
item_infos {
  sku_id: "99654"
  brand: "5849"
  shopid: "9456"
  cate: "7"
  rank_score: 0.4635670781135559
}
item_infos {
  sku_id: "12048"
  brand: "6200"
  shopid: "7501"
  cate: "35"
  rank_score: 0.46096566319465637
}
item_infos {
  sku_id: "99676"
  brand: "7212"
  shopid: "4874"
  cate: "24"
  rank_score: 0.46056973934173584
}
item_infos {
  sku_id: "257466"
  brand: "8809"
  shopid: "8921"
  cate: "30"
  rank_score: 0.45968693494796753
}
...
```

```shell 
python client.py as 8888 #老用户id
```
**输入**：输入老用户id 

**输出**  

```shell
error {
  code: 200
}
item_infos {
  sku_id: "105825"
  brand: "7388"
  shopid: "7501"
  cate: "62"
  rank_score: 0.4515012204647064
}
item_infos {
  sku_id: "309877"
  brand: "7891"
  shopid: "2875"
  cate: "70"
  rank_score: 0.4484674036502838
}
item_infos {
  sku_id: "342525"
  brand: "2873"
  shopid: "4429"
  cate: "70"
  rank_score: 0.4484269320964813
}
item_infos {
  sku_id: "310626"
  brand: "8745"
  shopid: "10298"
  cate: "7"
  rank_score: 0.4477023482322693
}
...

```


**用户服务**

```shell
python client.py um 8888
```
**输入**:用户id

**输出**

```shell
error {
  code: 200
}
user_info {
  user_id: "8888"
  age: "2.0"
  sex: "0.0"
  city_level: "5.0"
  province: "20.0"
  city: "43.0"
  country: "2459.0"
}
```
```shell
#输入一个不存在的用户id
error {
  code: 500
  text: "UM server get user_info from redis fail. (user_id: \"5\"\n)"
}
```

**内容服务**

```shell
 python client.py cm 99654
```
**输入**:商品id

**输出**
```shell
error {
  code: 200
}
item_infos {
  sku_id: "99654"
  brand: "5849"
  shopid: "9456"
  cate: "7"
}
```
```shell
#输入一个不存在的商品id
error {
  code: 500
  text: "CM server get item_info from redis fail. (item_ids: \"1324142525\"\n)"
}
```

**召回服务**

```shell
python client.py recall 8888
```
**输入**:用户id

**输出**
```shell
error {
  code: 200
}
score_pairs {
  nid: "109610"
  score: 4665.109375
}
score_pairs {
  nid: "316351"
  score: 4680.904296875
}
score_pairs {
  nid: "295368"
  score: 4771.783203125
}
score_pairs {
  nid: "244867"
  score: 4773.31787109375
}
...
```

**排序服务**

```shell
python client.py rank
```
**输入**:无输入，该服务单独执行仅使用默认输入参数

**输出**
```shell
error {
  code: 200
}
score_pairs {
  nid: "1"
  score: 0.47999122738838196
}
```
#### 模型
可以参考[官方项目](https://aistudio.baidu.com/aistudio/projectdetail/1481839)或[我的项目](https://aistudio.baidu.com/aistudio/projectdetail/3370104)自己训练获取模型或者完成一个新的推荐系统，或者私信我获取本项目缺少的模型和对应的数据文件
#### 致谢
>项目遵守[Apache License 2.0](http://www.apache.org/licenses/)协议，将代码更改的部分已作说明非常感谢[PaddleRec](https://github.com/PaddlePaddle/PaddleRec)的demo，本项目
>
>大部分是基于该项目部分改动得到的。
>
>感谢[京东2019用户对品类下店铺的购买预测竞赛数据集](https://jdata.jd.com/html/detail.html?id=8)
>
>感谢[PaddleServing](https://github.com/PaddlePaddle/Serving)、[Redis](https://github.com/Redis)、[milvus](https://github.com/milvus-io/milvus)对项目部署的支持；
>
>感谢[Protobuf](https://github.com/protocolbuffers/protobuf)和[gRPC](https://github.com/grpc/grpc)，实现了本项目的服务模块分布式部署和通信。
