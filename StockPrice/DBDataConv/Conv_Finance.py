from DBDataConv import AbstracterConversionClass as acc
import decimal

class Conv_Finance(acc.AbstracterConversionClass):

    def DBData_to_List(self, Item):
        return_list = []
        for items in Item['Items']:
            local_list = []
            local_list.append(int(items['Settlement']['N']))
            local_list.append(items['Stock_Code']['S'])
            local_list.append(float(items['Ope_Profit']['N']))
            local_list.append(float(items['Share_Profit']['N']))
            local_list.append(float(items['Ord_Profit']['N']))
            local_list.append(float(items['Amo_Salse']['N']))
            local_list.append(float(items['Net_Profit']['N']))
            return_list.append(local_list)

        return sorted(return_list, key=lambda x: x[0])