from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.airbnb
my_set = db.room_1127
# new_set = db.room_info_1127
new_set = db.reviewer_reviewee
for x in my_set.find():
    try:
        # room = {
        #     '_id': x['_id'],
        #     'name': x['name'],
        #     'review_count': x['review_details_interface']['review_count'],
        #     'host_other_property_review_count': x['review_details_interface']['host_other_property_review_count'],
        #     'review_summary_accuracy': x['review_details_interface']['review_summary'][0]['value'],
        #     'review_summary_communication': x['review_details_interface']['review_summary'][1]['value'],
        #     'review_summary_cleanliness': x['review_details_interface']['review_summary'][2]['value'],
        #     'review_summary_location': x['review_details_interface']['review_summary'][3]['value'],
        #     'review_summary_checkin': x['review_details_interface']['review_summary'][4]['value'],
        #     'review_summary_value': x['review_details_interface']['review_summary'][5]['value'],
        #     'review_score': x['review_details_interface']['review_score'],
        #     'localized_city': x['localized_city'],
        #     'response_rate_without_na': x['primary_host']['response_rate_without_na'],
        #     'identity_verified': x['primary_host']['identity_verified'],
        #     'member_since': x['primary_host']['member_since'],
        #     'languages': x['primary_host']['languages'],
        #     'primary_smart_name': x['primary_host']['smart_name'],
        #     'primary_host_name': x['primary_host']['host_name'],
        #     'response_time_without_na': x['primary_host']['response_time_without_na'],
        #     'is_superhost': x['primary_host']['is_superhost'],
        #     'primary_id': x['primary_host']['id'],
        #     'user_id': x['user']['id'],
        #     'user_host_name': x['user']['host_name']
        # }
        for a in x['comment_info']:
            reviewer_reviewee = {
                'id': x['_id'],
                'rating': a['rating'],
                'language': a['language'],
                'localized_date': a['localized_date'],
                'reviewee_id': a['reviewee']['id'],
                'reviewee_host_name': a['reviewee']['host_name'],
                'reviewee_is_superhost': a['reviewee']['is_superhost'],
                'reviewer_id': a['reviewer']['id'],
                'reviewer_host_name': a['reviewer']['host_name'],
                'reviewer_is_superhost': a['reviewer']['is_superhost']
            }
            new_set.insert(reviewer_reviewee)
            print("***********************************")
    except:
        pass
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")