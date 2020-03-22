
def is_valid(tweet_data):
    valid = False
    try:
        if tweet_data['user']['verified'] and tweet_data['user']['followers_count'] > 5000:
            valid = True
        return valid
    except Exception as e:
        print('ERROR ' + str(e))
        return valid



