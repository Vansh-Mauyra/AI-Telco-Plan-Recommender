from app.db.database import fetch_all
from app.utils.plan_categories import categorize_plans

def get_all_plans_categorized():
    plans = fetch_all("""
        SELECT 
            p.plan_id,
            p.plan_name,
            p.monthly_fee,
            p.validity_days,
            p.plan_type,
            p.data_gb,
            p.daily_data_gb,
            p.voice_minutes,
            p.sms_count,
            p.roaming_included,
            p.international_roaming,
            p.network_type,
            c.carrier_name
        FROM telco_plan p
        JOIN carrier c ON p.carrier_id = c.carrier_id
        WHERE p.is_active = true
    """)

    addons = fetch_all("""
        SELECT 
            a.addon_id,
            a.addon_name,
            a.price,
            a.data_gb,
            a.voice_minutes,
            a.sms_count,
            a.validity_days,
            c.carrier_name
        FROM addon a
        JOIN carrier c ON a.carrier_id = c.carrier_id
        WHERE a.is_active = true
    """)

    return categorize_plans(plans, addons)
