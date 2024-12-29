from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection


def create_collection():
    # 定义字段
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="paper_id", dtype=DataType.INT64),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=2560),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=256)
    ]

    # 定义集合模式
    schema = CollectionSchema(fields, description="论文片段")

    # 创建集合
    collection = Collection(name="paper_collection", schema=schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {"nlist": 2560}
    }
    collection.create_index(field_name="embedding", index_params=index_params)


if __name__ == '__main__':
    # 连接到 Milvus 服务器
    connections.connect("default", host="localhost", port="19530")
    create_collection()
