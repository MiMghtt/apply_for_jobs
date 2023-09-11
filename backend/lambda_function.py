import json
import uuid
import time
import boto3

dynamodb = boto3.client('dynamodb')

table_name = 'Senhas'

def generate_password(complexity):
    import random
    import string

    characters = string.ascii_uppercase + string.digits
    password = ''.join(random.choice(characters) for _ in range(12))
    return password

def create_password(event, context):
    try:
        body = json.loads(event["body"])
        complexity = body["complexity"]
        views = body["views"]
        expiration_days = body["expiration_days"]

        password = generate_password(complexity)
        password_id = str(uuid.uuid4())
        expiration_timestamp = int(time.time()) + (expiration_days * 24 * 3600)

        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                'PasswordId': {'S': password_id},  
                'Password': {'S': password},
                'Views': {'N': str(views)},
                'ExpirationTimestamp': {'N': str(expiration_timestamp)}
            }
        )

        password_url = f"http://localhost:3000/view/{password_id}"

        response["body"] = json.dumps({"password_url": password_url})

    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    return response


def get_password_from_dynamodb(password_id):
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'PasswordID': {'S': password_id}
            }
        )

        item = response.get('Item')
        if item:
            return True, item['Password']['S']
        else:
            return False, "Senha não encontrada"

    except Exception as e:
        return False, str(e)

def check_password_availability(event, context):
    try:
        password_id = event["pathParameters"]["passwordId"]
        
        is_available, password = get_password_from_dynamodb(password_id)
        if is_available:
            response = dynamodb.update_item(
                TableName=table_name,
                Key={
                    'PasswordID': {'S': password_id}
                },
                UpdateExpression='SET Views = Views - :val',
                ExpressionAttributeValues={
                    ':val': 1
                },
                ReturnValues='UPDATED_NEW'
            )
            return {
                "statusCode": 200,
                "body": json.dumps({"password": password})
            }
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": password})
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
