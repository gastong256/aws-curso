import boto3

# set the region to operate in
region = boto3.session.Session().region_name
# create clients for Cognito Identity Provider (User pools)
idp = boto3.client ('cognito-idp', region_name = region)

# define the user pool this script will work with
user_pool_id = 'us-east-1_Q8ZussZcJ'

def main ():
    """
    Retreive a list of users from the Cognito user pool.
    
    Returns a list of dictionaries in the form of:
    [
        {'username': 'user001', 'email': 'user001@example.com'},
        ...
        {'username': 'scott', 'email': 'tiger@example.com'}
    ]
    """
    import argparse
    # get args from command line (in this case just author_name)
    parser = argparse.ArgumentParser()
    parser.add_argument('author_name', help='The name of the script author.')
    args = parser.parse_args()

    usernames = list ()

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_users
    # getting email form user pool
    users_resp = idp.list_users (
            UserPoolId = user_pool_id,
            AttributesToGet = ['email'])

    # iterate over the returned users and extract username and email
    for user in users_resp['Users']:
        user_record = {'username': user['Username'], 'email': None}

        for attr in user['Attributes']:
            if attr['Name'] == 'email':
                user_record['email'] = attr['Value']

        usernames.append (user_record)
    print('---- Users from Cognito pool ----')
    print(usernames)
    print('Script author: ', args.author_name)
    print('Exiting')
    
if __name__ == '__main__':
    main()