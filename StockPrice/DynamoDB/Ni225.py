from DynamoDB import DynamoDB as dydb

class Ni225(dydb.DynamoDB):

    def initialize(self):
        self.TableName='Ni225'
        super().aws_DynamoDB()

    def select(self):
        result = self.dynamo_db.scan(TableName=self.TableName)
        return result

    def query(self,cal_day):
        result = self.dynamo_db.query(TableName=self.TableName,
                                      Select='ALL_ATTRIBUTES',
                                      KeyConditions={
                                          "Cal_Day": {
                                              "AttributeValueList": [{"N": cal_day}],
                                              "ComparisonOperator": "EQ"
                                          }
                                      })
        return result

    def insert(self,cal_day,ope_price,high_price,low_price,clo_price):

        if cal_day is None and ope_price and high_price is None and low_price is None and clo_price is None:
            return

        insert_item = {}

        if cal_day is not None:
            cal_day = {"N": cal_day}
            insert_item['Cal_Day'] = cal_day

        if ope_price is not None:
            ope_price = {"N": str(ope_price)}
            insert_item['Ope_Price'] = ope_price

        if high_price is not None:
            high_price = {"N": str(high_price)}
            insert_item['High_Price'] = high_price

        if low_price is not None:
            low_price = {"N": str(low_price)}
            insert_item['Low_Price'] = low_price

        if clo_price is not None:
            clo_price = {"N": str(clo_price)}
            insert_item['Clo_Price'] = clo_price

        print(insert_item)

        response = self.dynamo_db.put_item(
            TableName=self.TableName,
            Item=insert_item
        )
        return response
