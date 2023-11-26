from django.conf import settings
import geocoder


def get_latest_ip():
    """
    Find the latest IP entry in the auth.log file
    """

    # open auth.log
    auth_log_file = settings.AUTH_LOG_FILE

    # read the log file in memory in reversed order
    with open(auth_log_file) as f:
        lines = reversed(f.readlines())

    # read through the lines in reversed order
    for line in lines:
        # check for a IP... this can be recognized by the keyword 'port' following it
        # from 159.203.72.79 port 41636
        if ' port' in line:
            try:
                a = line.split(' port ')
                b = a[0].split(' from ')
                c = b[0].split(' nico-mint ')

                timestamp = c[0]

                # if b[1] still contains spaces, then it is not the expected format. Ignore this line
                if ' ' in b[1]:
                    continue

                ip = b[1]
                return timestamp, ip
            except:
                pass

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
