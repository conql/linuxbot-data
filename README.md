# 简介
该项目为收集数据所用的Python脚本。

# 安装
1. 命令行输入
```
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

2. 将.env文件放到根目录下

# 数据收集流程
1. 准备题目
2. 从GPT4获取题目知识点、解析、答案
3. 整理GPT4的输出，将输出的csv文件进行解析，得到知识点
4. 把知识点转为 embedding 以供上传

# 各脚本功能

## collect1.py
这个Python脚本主要做的事情是从GPT4获取题目知识点、解析、答案。脚本的主要功能是读取一个文本文件中的问题，然后使用这个API获取每个问题的答案，并将结果保存到一个CSV文件中。以下是每个函数的详细解释：

1. `load_dotenv()`：这个函数是从python-dotenv库中导入的，它用于加载.env文件中的环境变量。在这个脚本中，它被用来加载API_KEY。

2. `complete(messages)`：这个函数是用来调用API并获取回答的。它接收一个消息列表，然后向指定的URL发送一个POST请求，请求的内容是一个JSON对象，包含模型名和消息。然后它返回API的响应。

3. `answer(query)`：这个函数用来构建消息列表并调用`complete`函数。它首先从"prompt.txt"文件中读取第一条用户消息，然后定义消息列表，最后调用`complete`函数并返回响应。

4. `load_data(path)`：这个函数用来从指定路径的文件中读取内容，并将内容按"\n\n"分割，然后返回结果。

5. `get_answers_and_save(data, output_file, wait_time=10)`：这个函数用来获取答案并保存到CSV文件中。它首先尝试从CSV文件中加载现有的DataFrame，如果文件不存在，它会创建一个新的DataFrame。然后，它会遍历每个问题，获取答案，然后将问题和答案添加到DataFrame中，最后将DataFrame保存到CSV文件中。

6. 在主函数中，它首先从"data/课后测验.txt"文件中加载数据，然后调用`get_answers_and_save`函数，将数据和输出文件路径传递给它。

## prompt.txt
定义了GPT4使用的系统prompt，即输出格式、要求等

## parse1.py
这个Python脚本的主要目的是将collect1.py输出的CSV格式的数据，解析并转换为json格式，输出并保存为知识点列表。它从一个CSV文件中读取数据，解析每条记录中的"Response"字段，然后将解析后的数据保存到另一个CSV文件中。以下是每个函数的详细解释：

1. `load_csv_to_json(file_path)`：这个函数用来从CSV文件中加载数据，并将数据转换为JSON对象的列表。它首先从指定路径的文件中加载数据，然后将数据转换为字典列表，最后将每个字典转换为一个JSON对象。

2. `parse_answer(json_obj)`：这个函数用来解析JSON对象中的"Response"字段。它首先加载JSON对象，然后获取"Response"字段，并将其分割为多个部分。然后，它遍历每个部分，获取部分的标题和内容，并将它们添加到一个字典中。然后，它在"知识点"部分中查找所有的知识点，并将它们添加到字典中。最后，它将"Response"字段替换为解析后的答案。

3. 在主函数中，它首先从"data/课后测验.csv"文件中加载数据，并将数据转换为JSON对象。然后，它遍历每个JSON对象，解析每个对象的"Response"字段，并将解析后的对象添加到一个列表中。然后，它从列表中提取所有的知识点，并将它们添加到一个新的列表中。然后，它将知识点列表转换为一个DataFrame，并按"title"列对DataFrame进行分组，并合并每个组的"content"。然后，它按"title"列对DataFrame进行排序。最后，它将所有知识点保存为一个CSV文件。


## embedding1.py
这个Python脚本的主要目的是从一个API服务中获取文本的嵌入向量（embedding），并将结果保存到CSV和JSON文件中。以下是每个函数的详细解释：

1. `get_embedding(text)`：这个函数用来调用API并获取文本的嵌入向量。它接收一个文本字符串，然后向指定的URL发送一个POST请求，请求的内容是一个JSON对象，包含模型名和输入文本。然后它返回API的响应，即文本的嵌入向量。

2. `main()`：这个函数是脚本的主要部分。它首先从"knowledge_points.csv"文件中加载数据，然后检查是否存在'embedding'列，如果不存在，就创建一个。然后，它定义了每分钟的最大请求次数，并计算了每次请求之间的延迟。接着，它遍历每一行数据，对于每一行数据，它首先检查是否已经处理过，如果已经处理过，就跳过。然后，它将'title'和'content'字段组合成一个文本，然后调用`get_embedding`函数获取嵌入向量。如果获取失败，它会尝试重新获取。获取成功后，它将嵌入向量保存到DataFrame中，然后将DataFrame保存到CSV文件中。最后，它将DataFrame转换为一个JSON对象，并将JSON对象保存到一个JSON文件中。

# 备注
GPT4接口限制：每分钟最多10个请求，每天最多1000个请求
Embedding接口限制：每分钟最多40个请求，每天最多2000个请求