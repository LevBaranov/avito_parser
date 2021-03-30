QUERY_INSERT_ADS = '''
    INSERT INTO ads(ad_id, ad_name, category_id, owner_name, description, img, link, address, date_posted, date_added, status, "views", price, "source")
    VALUES {}
'''
QUERY_INSERT_CATEGORIES = '''
    INSERT INTO categories (category_id, category_name)
    VALUES {}
'''
QUERY_UPDATE_CATEGORIES = '''
    
'''
QUERY_PUT_ADS = '''
    INSERT INTO ads(ad_id, ad_name, category_id, owner_name, description, img, link, address, date_posted, date_added, status, "views", price, "source")
    VALUES {}
    ON CONFLICT (ad_id) DO UPDATE SET "views" = EXCLUDED."views", price = EXCLUDED.price, date_update = current_timestamp
'''