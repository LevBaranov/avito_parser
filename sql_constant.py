QUERY_INSERT_ADS = '''
    INSERT INTO ads(ad_id, ad_name, category_id, owner_name, description, img, link, address, date_posted, date_added, status, "views", price, "source")
    VALUES {}
'''
QUERY_INSERT_CATEGORIES = '''
    INSERT INTO categories (category_id, category_name)
    VALUES {}
    ON CONFLICT (category_id) DO NOTHING
'''
QUERY_PUT_REGIONS = '''
    INSERT INTO regions (region_id, region_name)
    VALUES {}
    ON CONFLICT (region_id) DO UPDATE SET region_name = EXCLUDED.region_name
'''
QUERY_PUT_ADS = '''
    INSERT INTO ads(ad_id, ad_name, category_id, region_id, owner_name, description, img, link, address, date_posted, date_added, status, "views", price, "source")
    VALUES {}
    ON CONFLICT (ad_id) DO UPDATE SET "views" = EXCLUDED."views", price = EXCLUDED.price, date_update = current_timestamp
'''
QUERY_SELECT_ACTIVE_MONITOR = '''
    SELECT category_id, region_id
    FROM monitoring m 
    WHERE m.status is true 
'''
QUERY_PUT_MONITOR = '''
    INSERT INTO monitoring (category_id, region_id)
    VALUES {}
    ON conflict on constraint uni_rid_cid DO UPDATE SET status = true
'''