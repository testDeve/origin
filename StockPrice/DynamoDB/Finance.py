from DynamoDB import DynamoDB as dydb

class Finance(dydb.DynamoDB):

    def initialize(self):
        self.TableName='Finance'
        super().aws_DynamoDB()

    def select(self,stock_code,date):
        result = self.dynamo_db.scan(TableName=self.TableName)
        return result

    def query(self,stock_code,settlement):
        print(stock_code,settlement)
        result = self.dynamo_db.query(TableName=self.TableName,
                                      Select='ALL_ATTRIBUTES',
                                      KeyConditions={
                                          "Stock_Code": {
                                              "AttributeValueList": [{"S": stock_code}],
                                              "ComparisonOperator": "EQ"
                                          },
                                          "Settlement": {
                                              "AttributeValueList": [{"S": settlement}],
                                              "ComparisonOperator": "EQ"
                                          }
                                      })
        return result

    def insert(self,stock_code,settlement,amo_salse,ope_profit,ord_profit,net_profit,share_profit,sto_distribution):

        if stock_code is None and settlement is None and amo_salse and ope_profit is None \
                and ord_profit is None and net_profit is None and share_profit is None and sto_distribution is None:
            return

        insert_item = {}

        if stock_code is not None:
            stock_code = {"S": stock_code}
            insert_item['Stock_Code'] = stock_code

        if settlement is not None:
            settlement = {"S": settlement}
            insert_item['Settlement'] = settlement

        if amo_salse is not None:
            amount_salse = {"N": str(amo_salse)}
            insert_item['Amo_Salse'] = amount_salse

        if ope_profit is not None:
            ope_profit = {"N": str(ope_profit)}
            insert_item['Ope_Profit'] = ope_profit

        if ord_profit is not None:
            ord_profit = {"N": str(ord_profit)}
            insert_item['Ord_Profit'] = ord_profit

        if net_profit is not None:
            net_profit = {"N": str(net_profit)}
            insert_item['Net_Profit'] = net_profit

        if share_profit is not None:
            share_profit = {"N": str(share_profit)}
            insert_item['Share_Profit'] = share_profit

        print(insert_item)

        response = self.dynamo_db.put_item(
            TableName=self.TableName,
            Item=insert_item
        )
        return response

