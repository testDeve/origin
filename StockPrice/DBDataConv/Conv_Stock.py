from DBDataConv import AbstracterConversionClass as acc
import decimal

class Conv_Stock(acc.AbstracterConversionClass):

    def DBData_to_List(self, Item):
        return_list = []
        for items in Item['Items']:
            local_list = []
            local_list.append(int(items['Cal_Day']['N']))
            local_list.append(items['Stock_Code']['S'])
            local_list.append(float(items['Ope_Price']['N']))
            local_list.append(float(items['Low_Price']['N']))
            local_list.append(float(items['High_Price']['N']))
            local_list.append(float(items['Clo_Price']['N']))
            return_list.append(local_list)

        return sorted(return_list, key=lambda x: (x[1],x[0]))