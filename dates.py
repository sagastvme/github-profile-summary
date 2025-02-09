import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
def fromIsoStrToDate(datestr: str, format):
    date = datetime.datetime.fromisoformat(datestr)
    return date.strftime(format)    


def parseIsoDateToDateObject(date):
    return parser.isoparse(date)


def getRelativeDate(years=0, days=0, months=0):
    now = datetime.datetime.now(datetime.timezone.utc)
    return now - relativedelta(days=days, years=years, months=months)
