from datetime import datetime

def days_difference(d1, d2):
    """Difference between two datetimes: end-start date"""
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


