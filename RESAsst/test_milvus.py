from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection


def create_collection():
    # 定义字段
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=255)
    ]

    # 定义集合模式
    schema = CollectionSchema(fields, description="测试集合")

    # 创建集合
    collection = Collection(name="example_collection", schema=schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)


def insert():
    import random

    # 生成随机向量数据
    vectors = [random.random() for _ in range(128)]

    # 插入数据
    collection = Collection("example_collection")
    collection.load()
    collection.insert([{"id": 0, "embedding": vectors, "text": "This is a test."}])


def search():
    collection = Collection("example_collection")
    expr = f"id == 0"
    results = collection.query(expr=expr, output_fields=["id", "embedding", "text"])
    print(results)


if __name__ == '__main__':
    # 连接到 Milvus 服务器
    connections.connect("default", host="localhost", port="19530")
    create_collection()
    insert()
    # search()
