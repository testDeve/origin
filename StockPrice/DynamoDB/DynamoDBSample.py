import boto3

table = boto3.client('dynamodb')

'''
print('-----------------------------------')
print('case1 全件取得')
result = table.scan(TableName='Music')
print(result)
'''

insertItem={'Artist':{'S':'堂珍嘉邦'},'SongTitle':{'S':'You And I'},'info': {'S':'J-POP'}}

response = table.batch_write_item(
    RequestItems={
        'Music':[
            {
                'PutRequest':{
                    'Item':insertItem
                }
            },
            {
                'PutRequest':{
                    'Item':{'Artist':{'S':'CHEMISTRY'},'SongTitle':{'S':'ユメノツヅキ'},'info': {'S':'J-POP'}}
                }
            }
        ]
    }

)
"""
response = table.put_item(
    TableName='Music',
    Item=insertItem
)
"""

print('-----------------------------------')
print('case2 条件取得')
result = table.query(TableName='Music',
                     Select='ALL_ATTRIBUTES',
                     KeyConditions={
                         "Artist": {
                             "AttributeValueList": [{"S": "CHEMISTRY"}],
                             "ComparisonOperator": "EQ"
                         }
                     })
for i in range(0,result['Count']):
    print(result['Items'][i]['Artist']['S'],end=",")
    print(result['Items'][i]['SongTitle']['S'])
