from django.conf import settings
import geocoder


def get_latest_ip():
    """
    Find the latest IP entry in the auth.log file
    """

    # open auth.log
    auth_log_file = settings.AUTH_LOG_FILE

    # reverse file
    with open(auth_log_file) as f:
        lines = reversed(f.readlines())

    # open reverse file
    for line in lines:
        # check for a IP... this can be recognized by the keyword 'port' following it
        # from 159.203.72.79 port 41636
        if ' port' in line:
            try:
                a = line.split(' port ')
                b = a[0].split(' from ')
                c = b[0].split(' nico-mint ')

                timestamp = c[0]
                ip = b[1]
                return timestamp, ip
            except:
                pass

    # extract the latest ip from the auth log
    latest_ip = "82.170.56.148"

    return None

def geocode(ip):
    """
    Get location information based on IP address
    """
    g = geocoder.ip(ip)

    result = {}
    result['latitude'] = g.latlng[1]
    result['longtitude'] = g.latlng[0]
    result['address'] = g.address
    result['country'] = g.country

    return result
