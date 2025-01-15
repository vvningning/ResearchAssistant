import pymysql
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])
index_name = 'documents'


def get_all_doc():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='test',
        password='123456',
        database='asst'
    )

    cursor = conn.cursor()
    cursor.execute('SELECT eid, username, name, content FROM asst_build WHERE type="pdf"')
    documents = cursor.fetchall()
    cursor.close()
    conn.close()

    return documents


def init_index():
    es.indices.create(
        index=index_name,
        body={
            'settings': {
                'index': {
                    'similarity': {
                        'default': {
                            'type': 'BM25',
                            'k1': 1.5,
                            'b': 0.75
                        }
                    }
                },
                # 'analysis': {
                #     'tokenizer': {
                #         'ik_max_word': {
                #             'type': 'ik_max_word'
                #         }
                #     },
                #     'analyzer': {
                #         'default': {
                #             'type': 'custom',
                #             'tokenizer': 'ik_max_word'
                #         }
                #     }
                # }
            },
            'mappings': {
                'properties': {
                    'username': {
                        'type': 'keyword'
                    },
                    'name': {
                        'type': 'text'
                    },
                    'content': {
                        'type': 'text'
                    }
                }
            }
        }
    )

    documents = get_all_doc()

    for doc in documents:
        eid, username, name, content = doc
        document = {
            'username': username,
            'name': name,
            'content': content
        }

        es.index(index=index_name, id=eid, body=document)


def query(username, keyword):
    query_body = {
        'query': {
            'bool': {
                'should': [
                    {
                        'match': {
                            'name': {
                                'query': keyword,
                                'boost': 4
                            }
                        }
                    },
                    {
                        'match': {
                            'content': {
                                'query': keyword,
                                'boost': 1
                            }
                        }
                    }
                ],
                'filter': [
                    {
                        'term': {
                            'username': username
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        },
        'highlight': {
            'fields': {
                'name': {
                    "fragment_size": 300,
                    "number_of_fragments": 1
                },
                'content': {
                    "fragment_size": 300,
                    "number_of_fragments": 1
                }
            }
        }
    }

    response = es.search(index=index_name, body=query_body)

    return response


def add_index(eid, username, name, content):
    document = {
        'username': username,
        'name': name,
        'content': content
    }
    es.index(index=index_name, id=eid, body=document)


def delete_index(eid):
    es.delete(index=index_name, id=eid)


# test script
if __name__ == '__main__':
    # es.indices.delete(index=index_name)
    init_index()
    # add_index(8, 'user2', '让我们说中文', '南京市长江大桥')
    # add_index(9, 'user1', '让我们说中文', '南京市长江大桥')
    # delete_index(3)
    # res = query('user1', '南京大桥')
    # print(res['hits']['hits'])
