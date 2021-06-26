# cryptology_homework

用于管理密码学相关算法实现的代码

## 1. DES

[DES接口](src/des.h)

## 2. AES

[AES接口](src/aes.h)

## 3. Operation Mode

[工作模式接口](src/operation_mode.hpp)

### (1) ECB

 电码本工作模式

### (2) CBC

密文分组链接工作模式

### (3) OFB

输出反馈工作模式

## 编译

可以直接运行根目录下的 `release.sh` 脚本

```shell
./release.sh
```

或者按照一下步骤操作

第一步： 创建编译目录

```shell
mkdir build && cd build
```

第二步：编译代码

```shell
cmake .. && make
```

第三步：运行示例

```shell
./crypt_impl
```
