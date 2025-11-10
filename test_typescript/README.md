# TypeScript示例

## 运行

安装依赖

```shell
npm install -D typescript @types/node
```

### 编译运行

编译

```shell
npx tsc
```

运行

```shell
node dist/index.js
```

### 打包运行

安装依赖

```shell
npm install pkg
```

打包成可执行文件

```shell
npx pkg .
```

运行

```shell
./dist-exec/my-ts-app-macos
```

### 直接运行

需要先安装 `tsx`

```shell
npm install -D tsx
```

再运行

```shell
npx tsx src/index.ts
```