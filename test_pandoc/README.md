# pandoc转换markdown为html

示例内容参考GitHub项目: [md-publisher](https://github.com/andremueller/md-publisher)

## 安装工具

[pandoc](https://github.com/jgm/pandoc/releases)
[pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases/)

**注意：** `pandoc-crossref` 需要匹配 `pandoc` 的版本，在下载页面会有说明

将以上两个工具解压后，放到系统目录下：

```shell
cp -r pandoc/bin /usr/local/
cp -r pandoc/share /usr/local/
cp pandoc-crossref /usr/local/bin/
```

## 编译

```
./build.sh --output ./demo.html ./posts/demo.md
```

会生成 `output/demo.html` 文件


## 参数解释

### 1. 独立的文件

```
--standalone
```

### 2. 资源嵌入网页

会将样式和图嵌入到html文件中，对于需要推送到 `medium` 的情况，不要设置这个选项 

```
--embed-resources 
```

### 3. 处理引用和参考文献

```
--filter pandoc-crossref --citeproc 
```

### 4. 设置样式

```
--css css/science.css 
```

### 5. 设置能处理的文档类型

```
--from markdown+yaml_metadata_block+implicit_figures+fenced_divs+citations+table_captions 
```

### 6. 设置输出文件的格式

```
--to html5 
```

### 7. 设置支持tex公式

```
--webtex
```
