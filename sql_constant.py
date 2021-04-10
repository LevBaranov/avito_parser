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
    SELECT region_id, category_id
    FROM monitoring m 
    WHERE m.status is true 
'''
QUERY_PUT_MONITOR = '''
    INSERT INTO monitoring (category_id, region_id)
    VALUES {}
    ON conflict on constraint uni_rid_cid DO UPDATE SET status = true
'''
QUERY_SELECT_NAME_ACTIVE_MONITOR = '''
    SELECT m.mon_id, r.region_name, c.category_name 
    FROM monitoring m 
    JOIN regions r
        ON r.region_id = m.region_id 
    JOIN categories c
        ON c.category_id =m.category_id 
    WHERE m.status is true
'''

QUERY_SELECT_RESULTS_MONITOR = '''
    SELECT 
        a.ad_id,
        c.category_name,
        r.region_name,
        a.ad_name,
        a.owner_name,
        a.description,
        a.img,
        a.link,
        a.address,
        a.date_added,
        a.date_posted,
        a.date_update,
        a.views,
        a.price 
    from ads a
    join (
        select category_id, region_id 
        from monitoring where mon_id=%s) m
    on m.category_id = a.category_id AND m.region_id = a.region_id
    join categories c 
    on c.category_id = a.category_id
    join regions r 
    on r.region_id = a.region_id
'''