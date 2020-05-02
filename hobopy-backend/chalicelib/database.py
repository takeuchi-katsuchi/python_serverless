import os
import boto3
import uuid
from boto3.dynamodb.conditions import Key

# DynamoDBへの接続を取得する
def _get_database():
    endpoint = os.environ.get('DB_ENDPOINT')
    if endpoint:
        return boto3.resource('dynamodb', endpoint_url=endpoint)
    else:
        return boto3.resource('dynamodb')

# 全てのレコードを取得する
def get_all_todos():
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    response = table.scan()
    return response['Items']

def create_todo(todo):
    # 登録内容を作成する
    item = {
        'id': uuid.uuid4().hex,
        'title': todo['title'],
        'memo': todo['memo'],
        'priority': todo['priority'],
        'completed': False,
    }

    # DynamoDBにデータを登録する
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    table.put_item(Item=item)
    return item

# 指定されたIDのレコードを取得する
def get_todo(todo_id):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    response = table.query(
        KeyConditionExpression= Key('id').eq(todo_id))
    items = response['Items']
    return items[0] if items else None

#  指定されたIDのToDoを更新する
def update_todo(todo_id, changes):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    # クエリを構築する
    update_expression = []
    expression_attribute_values = {}
    for key in ['title', 'memo', 'priority', 'completed']:
        if key in changes:
            update_expression.append(f"{key} = :{key[0:1]}")
            expression_attribute_values[f": {key[0:1]}"] = changes[key]

            # 2.DynamoDBのデータを更新する
            result = table.update_item(
                Key={
                    'id': todo_id,
                },
                UpdateExpression = 'set' + ','.join(update_expression),
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues ='ALL_NEW'
            )
            return result['Attributes']

# 指定されたIDのtodoを更新する
def delete_todo(todo_id):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    # DynamoDBのデータを削除する
    result = table.delete_item(
        Key={
            'id': todo_id,
        },
        ReturnValues = 'ALL_OLD'
    )
    return result['Attributes']