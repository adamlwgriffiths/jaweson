from __future__ import absolute_import

try:
    from ..serialiser import Serialiser
    import datetime
    from dateutil import parser as dateparser

    class DateTimeSerializer(Serialiser):
        python_types = (datetime.date, datetime.time, datetime.datetime)
        serialised_types = ('date', 'time', 'datetime')

        def to_dict(self, obj):
            # must come first, datetime is an instance of date and time
            if isinstance(obj, datetime.datetime):
                return {
                    '__type__': 'datetime',
                    'data': obj.isoformat(),
                }
            if isinstance(obj, datetime.date):
                return {
                    '__type__': 'date',
                    'data': obj.isoformat(),
                }
            if isinstance(obj, datetime.time):
                return {
                    '__type__': 'time',
                    'data': obj.isoformat(),
                }

            return super(DateTimeSerializer, self).to_dict(obj)

        def from_dict(self, jobj):
            if jobj.get('__type__') == 'datetime':
                return dateparser.parse(jobj['data'])
            if jobj.get('__type__') == 'date':
                return dateparser.parse(jobj['data']).date()
            if jobj.get('__type__') == 'time':
                return dateparser.parse(jobj['data']).time()

            return super(DateTimeSerializer, self).from_dict(jobj)
except:
    # no datetime support
    pass
