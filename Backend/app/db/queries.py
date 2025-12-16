from app.db.connection import get_db


# -------------------------------------------------
# Customer profile
# -------------------------------------------------
def get_customer_profile(customer_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            customer_id,
            avg_monthly_data_gb,
            avg_voice_minutes,
            avg_sms,
            budget,
            current_carrier_id,
            current_plan_id
        FROM customer_profile
        WHERE customer_id = %s
    """, (customer_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "customer_id": row[0],
        "avg_monthly_data_gb": float(row[1] or 0),
        "avg_voice_minutes": int(row[2] or 0),
        "avg_sms": int(row[3] or 0),
        "budget": float(row[4]),
        "current_carrier_id": row[5],
        "current_plan_id": row[6]
    }


# -------------------------------------------------
# Usage history aggregation (NEW)
# -------------------------------------------------
def fetch_usage_summary(customer_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            AVG(data_gb) AS avg_data_gb,
            AVG(voice_minutes) AS avg_voice_minutes,
            AVG(sms) AS avg_sms,
            BOOL_OR(international_usage) AS uses_international,
            SUM(roaming_charges) > 0 AS uses_roaming
        FROM usage_history
        WHERE customer_id = %s
          AND month >= CURRENT_DATE - INTERVAL '6 months'
    """, (customer_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return {}

    return {
        "avg_data_gb": float(row[0] or 0),
        "avg_voice_minutes": int(row[1] or 0),
        "avg_sms": int(row[2] or 0),
        "uses_international": bool(row[3]),
        "uses_roaming": bool(row[4])
    }


# -------------------------------------------------
# Candidate plans (UPDATED)
# -------------------------------------------------
def fetch_candidate_plans(
    budget: float | None = None,
    min_data: float | None = None,
    min_voice: int | None = None,
    needs_roaming: bool = False,
    needs_int_roaming: bool = False,
    network_type: str | None = None,
    validity_days: int | None = None,
    limit: int = 20
):
    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT
            plan_id,
            carrier_id,
            plan_name,
            monthly_fee,
            data_gb,
            daily_data_gb,
            voice_minutes,
            sms_count,
            roaming_included,
            international_roaming,
            network_type,
            validity_days
        FROM telco_plan
        WHERE is_active = TRUE
    """

    params = []

    if budget is not None:
        query += " AND monthly_fee <= %s"
        params.append(budget)

    if min_data is not None:
        query += " AND (data_gb >= %s OR daily_data_gb * validity_days >= %s)"
        params.append(min_data)
        params.append(min_data)

    if min_voice is not None:
        query += " AND voice_minutes >= %s"
        params.append(min_voice)

    if needs_roaming:
        query += " AND roaming_included = TRUE"

    if needs_int_roaming:
        query += " AND international_roaming = TRUE"

    if network_type:
        query += " AND network_type = %s"
        params.append(network_type)

    if validity_days:
        query += " AND validity_days >= %s"
        params.append(validity_days)

    query += " LIMIT %s"
    params.append(limit)

    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()

    plans = []
    for r in rows:
        plans.append({
            "plan_id": r[0],
            "carrier_id": r[1],
            "plan_name": r[2],
            "monthly_fee": float(r[3]),
            "data_gb": float(r[4] or 0),
            "daily_data_gb": float(r[5] or 0),
            "voice_minutes": int(r[6] or 0),
            "sms_count": int(r[7] or 0),
            "roaming_included": bool(r[8]),
            "international_roaming": bool(r[9]),
            "network_type": r[10],
            "validity_days": int(r[11])
        })

    return plans
