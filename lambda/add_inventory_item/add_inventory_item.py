import json
import boto3
import uuid
from decimal import Decimal

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):  
        return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
    return obj

def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'item_id': unique_id,
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'item_qty': int(data['item_qty']),
                'item_price': Decimal(str(data['item_price'])),
                'location_id': int(data['location_id'])
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }