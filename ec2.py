import boto3
import sys
from statistics import mean
dynamodb = boto3.resource('dynamodb')
table_name = 'Course'
table = dynamodb.Table(table_name)


def main():
    avg_var95 = []
    avg_var99 = []

    for arg in sys.argv[1:]:
        resp = table.get_item(Key={'id': arg})
        item = resp.get('Item', {})
        avg_var95.append(item['var95'])
        avg_var99.append(item['var99'])

    avg_var95 = [mean(g) for g in zip(*avg_var95)]
    avg_var99 = [mean(g) for g in zip(*avg_var99)]
    sum_var95 = mean(avg_var95)
    sum_var99 = mean(avg_var99)
    resp = table.get_item(Key={'id':"HISTORY"}) # List of prev runs contains Dictionary of values
    item = resp.get('Item',{})
    hist = item['data']
    last = hist.pop()
    last['var95'] = sum_var95
    last['var99'] = sum_var99
    hist.append(last)

    table.put_item(Item={"id":"HISTORY","data":hist})
    table.put_item(Item={"id":"lst95","data":avg_var95})
    table.put_item(Item={"id":"lst99","data":avg_var99})
