import arrow

def get_last_month():
    now = arrow.utcnow()
    if now.month != 1:
        last_month = now.replace(month=(now.month - 1))
    else:
        last_month = now.replace(year=(now.year - 1), month=12)
    return last_month.format("YYYY-MM-DD")
