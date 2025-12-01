import boto3
import json

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Extract the 'item_id' from the path parameters
    if 'pathParameters' not in event or 'item_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'item_id' path parameter")
        }
    
    if 'queryStringParameters' not in event or 'location_id' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' query parameter")
        }

    key_value = event['pathParameters']['item_id']
    location_value = int(event['queryStringParameters']['location_id'])
    
    # Prepare the key for DynamoDB
    key = {
        'item_id': {'S': key_value},
        'location_id': {'N': str(location_value)}
    }

    # Attempt to delete the item from the table
    try:
        dynamo_client.delete_item(TableName=table_name, Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {key_value} deleted successfully.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }