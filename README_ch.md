# CDR3PairSearch

基于 CDR3 序列的配对链搜索工具，专为免疫组库数据分析设计，支持重链/轻链 V/J 基因和 CDR3 氨基酸序列的精确与模糊匹配。

## 项目概述

CDR3PairSearch 是一个用于免疫球蛋白（抗体）和 T 细胞受体序列分析的专业工具。它能够根据互补决定区 3（CDR3）的氨基酸序列以及 V/J 基因信息，在大型序列数据库中高效搜索匹配的重链和轻链配对数据。

该工具特别适用于：

- 从高通量测序数据中寻找特定 CDR3 序列的配对链
- 免疫组库多样性分析
- 抗体工程和改造研究
- 疾病相关免疫受体序列的鉴定

## 核心功能

1. **多模式 CDR3 搜索**

   - 重链 CDR3 特异性搜索
   - 轻链 CDR3 特异性搜索
   - 通用 CDR3 序列搜索（同时匹配重链和轻链）

2. **灵活的序列匹配**

   - 汉明距离计算：适用于比较等长序列的差异
   - 编辑距离（Levenshtein）计算：适用于比较不等长序列，可衡量插入、删除和替换操作

3. **基因匹配系统**

   - 支持 V 基因和 J 基因的精确匹配
   - 自动忽略基因亚型信息（如从"IGHV1-69\*01"中提取"IGHV1-69"进行匹配）
   - 可组合基因和 CDR3 序列进行复合条件搜索

4. **高效数据处理**
   - 支持大型 CSV 文件的分块读取，降低内存占用
   - 自动处理文件注释行，兼容多种数据格式
   - 结果自动保存为结构化 CSV 文件，便于后续分析

## 安装方法

### 从 GitHub 安装（推荐）

# 安装最新版本

pip install git+https://github.com/yourusername/cdr3pairsearch.git

# 如需指定版本

pip install git+https://github.com/yourusername/cdr3pairsearch.git@v1.0.0

### 从源码安装

# 克隆仓库

git clone https://github.com/yourusername/cdr3pairsearch.git
cd cdr3pairsearch

# 安装

pip install .

## 快速开始

from cdr3pairsearch import search_paired_chains

# 基础用法：搜索重链 CDR3 序列

results = search_paired_chains(
database_dir="./database",
cdr3_aa_heavy="CARDTGGFDIW",
threshold=1,
distance_method="edit"
)

# 高级用法：组合基因和 CDR3 搜索

results = search_paired_chains(
database_dir="./database",
cdr3_aa_light="GTWHSSLSAWV",
threshold=2,
distance_method="hamming",
v_call_light="IGLV1-51",
j_call_light="IGLJ3",
output_file="./results/light_chain_matches.csv",
chunk_size=10000
)

## 参数详解

`search_paired_chains`函数是工具的核心，以下是其参数的详细说明：

| 参数名称          | 类型   | 默认值                               | 描述                                                                                                                             |
| ----------------- | ------ | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `database_dir`    | 字符串 | 无                                   | 数据库目录的路径，该目录下应包含一个或多个 CSV 格式的数据文件。** 必需参数 **。                                                  |
| `cdr3_aa`         | 字符串 | `None`                               | 通用 CDR3 氨基酸序列，将同时与重链和轻链的 CDR3 序列进行比较。与`cdr3_aa_heavy`和`cdr3_aa_light`互斥，只能指定其中一个。         |
| `cdr3_aa_heavy`   | 字符串 | `None`                               | 重链 CDR3 氨基酸序列，仅与数据库中的重链 CDR3 进行比较。与`cdr3_aa`和`cdr3_aa_light`互斥。                                       |
| `cdr3_aa_light`   | 字符串 | `None`                               | 轻链 CDR3 氨基酸序列，仅与数据库中的轻链 CDR3 进行比较。与`cdr3_aa`和`cdr3_aa_heavy`互斥。                                       |
| `threshold`       | 整数   | `0`                                  | 距离阈值，只有距离小于或等于该值的序列才会被视为匹配。值为 0 表示精确匹配，值越大允许的差异越大。                                |
| `distance_method` | 字符串 | `"edit"`                             | 距离计算方法，可选值：<br>- `"hamming"`: 汉明距离，仅适用于等长序列<br>- `"edit"`: 编辑距离（Levenshtein），适用于任何长度的序列 |
| `v_call_heavy`    | 字符串 | `None`                               | 重链 V 基因名称，如"IGHV1-69"。工具会自动忽略亚型信息（如"\*01"部分）。                                                          |
| `v_call_light`    | 字符串 | `None`                               | 轻链 V 基因名称，如"IGLV1-51"。                                                                                                  |
| `j_call_heavy`    | 字符串 | `None`                               | 重链 J 基因名称，如"IGHJ5"。                                                                                                     |
| `j_call_light`    | 字符串 | `None`                               | 轻链 J 基因名称，如"IGLJ3"。                                                                                                     |
| `output_file`     | 字符串 | `"./paired_chain_search_output.csv"` | 结果输出文件的路径。如果文件已存在，将被覆盖。                                                                                   |
| `chunk_size`      | 整数   | `None`                               | 分块读取时每块的记录数。对于大型文件（百万级记录），建议设置为 10,000-100,000 以减少内存占用。`None`表示一次性读取整个文件。     |
| `ignore_subtype`  | 布尔值 | `True`                               | 是否忽略基因的亚型信息。设置为`True`时，"IGHV1-69*01"将与"IGHV1-69*02"视为匹配。                                                 |

## 处理逻辑详解

`search_paired_chains`函数的内部处理流程如下：

1. **参数验证**

   - 检查 CDR3 参数的互斥性（确保只有一个 CDR3 参数被设置）
   - 验证距离计算方法的有效性
   - 检查数据库目录是否存在及是否包含 CSV 文件

2. **数据库读取**

   - 遍历指定目录下的所有 CSV 文件
   - 对于每个文件：
     - 跳过第一行注释信息（如果存在）
     - 使用第二行作为列名
     - 根据`chunk_size`参数决定是分块读取还是一次性读取

3. **数据过滤**

   - **基因过滤**：根据提供的 V/J 基因参数过滤数据

     - 自动处理基因名称，移除亚型信息（如"\*01"）
     - 仅保留基因匹配的记录

   - **CDR3 序列过滤**：
     - 根据指定的 CDR3 参数（重链、轻链或通用）计算距离
     - 对每个序列计算与查询序列的距离（汉明或编辑距离）
     - 仅保留距离小于等于阈值的记录

4. **结果处理**
   - 为结果添加额外信息列：
     - `query_cdr3`：存储查询时使用的 CDR3 序列
     - `cdr3_aa_dist_heavy`/`cdr3_aa_dist_light`：计算得到的距离值
     - `inference_cdr3_type`：标记匹配类型（重链、轻链或两者）
   - 合并所有匹配结果
   - 将最终结果保存到指定的输出文件

## 数据库格式要求

数据库文件应为 CSV 格式，且至少包含以下字段（字段名区分大小写）：

### 重链相关字段

- `cdr3_aa_heavy`：重链 CDR3 氨基酸序列
- `v_call_heavy`：重链 V 基因分配结果
- `j_call_heavy`：重链 J 基因分配结果

### 轻链相关字段

- `cdr3_aa_light`：轻链 CDR3 氨基酸序列
- `v_call_light`：轻链 V 基因分配结果
- `j_call_light`：轻链 J 基因分配结果

> 注意：CSV 文件应在第二行包含列名，第一行将被视为注释行自动跳过。

## 示例输出

输出文件是一个 CSV 文件，包含原始数据中所有匹配的记录，并添加了以下额外列：

| 新增列名              | 描述                                         |
| --------------------- | -------------------------------------------- |
| `query_cdr3`          | 搜索时使用的 CDR3 查询序列                   |
| `cdr3_aa_dist_heavy`  | 重链 CDR3 与查询序列的距离                   |
| `cdr3_aa_dist_light`  | 轻链 CDR3 与查询序列的距离                   |
| `inference_cdr3_type` | 匹配类型，可能的值为"heavy"、"light"或"both" |

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 贡献指南

欢迎通过 GitHub 提交 issue 和 pull request 来改进这个工具。贡献前请确保：

- 所有新功能都包含相应的测试
- 代码遵循 PEP 8 规范
- 文档已更新以反映新功能或变化
