from django.conf import settings
import geocoder
from datetime import datetime, timedelta
from ..models import Sniffer

AUTH_DATE_FORMAT = '%b %d %H:%M:%S'

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


def get_latest_ips(seconds):
    """
    Find the latest IP's in auth.log file
    """
    print(get_latest_ips)

    ips = []
    timestamp_start = None

    # open auth.log
    auth_log_file = settings.AUTH_LOG_FILE

    # read the log file in memory in reversed order
    with open(auth_log_file) as f:
        lines = reversed(f.readlines())

    # read through the lines in reversed order
    for line in lines:
        # check for a IP... this can be recognized by the keyword 'port' following it
        # Nov 26 13:55:02 nico-mint sshd[18759]: Failed password for root from 106.54.212.205 port 35102 ssh2

        if ' port' in line:
            try:
                a = line.split(' port ')
                b = a[0].split(' from ')
                c = b[0].split(' nico-mint ')

                t = c[0]

                # convert timestamp to timestamp
                timestamp = datetime.strptime(t, AUTH_DATE_FORMAT)
                if not timestamp_start:
                    timestamp_start = timestamp - timedelta(seconds=seconds)

                # if b[1] still contains spaces, then it is not the expected format. Ignore this line
                if ' ' in b[1]:
                    continue

                ip = b[1]
                ips.append(ip)

                # read back in the file for the number of indicated seconds
                if timestamp < timestamp_start:
                    break

            except:
                pass

    # return a unique list of IP's
    print(ips)
    return list(set(ips))

def geocode(ip):
    """
    Get location information based on IP address
    """
    print("geocode: "+ip)
    result = {}

    # first check in the sniffers database to prevent too many requests to geocoder (only 1000 a day are allowed)
    try:
        sniffer = Sniffer.objects.get(ip=ip)
        result['latitude'] = sniffer.latitude
        result['longtitude'] = sniffer.longtitude
        result['address'] = sniffer.address
        result['country'] = sniffer.country
        result['new'] = False
        print("found: "+str(result))

    except Sniffer.DoesNotExist:
        g = geocoder.ip(ip)

        result['latitude'] = g.latlng[1]
        result['longtitude'] = g.latlng[0]
        result['address'] = g.address
        result['country'] = g.country
        result['new'] = True

        # store in the database
        new_sniffer = Sniffer(
            ip=ip,
            latitude=result['latitude'],
            longtitude = result['longtitude'],
            address=g.address,
            country=g.country)
        new_sniffer.save()
        print("created: " + str(result))

    print(get_latest_ips)
    return result


def create_features(ips):

    features = []
    id = 0

    for ip in ips:
        try:
            id=+1

            # calculate the coordinates
            location = geocode(ip)
            coordinates = []
            coordinates.append(location['latitude'])
            coordinates.append(location['longtitude'])

            feature = {}
            feature['id'] = id
            feature['type'] = 'Feature'

            properties = {}
            properties['name'] = ip
            properties['pk'] = id

            if location['new'] == True:
                properties['color'] = 'red'
                properties['radius'] = 8
            else:
                properties['color'] = 'green'
                properties['radius'] = 4

            feature['properties'] = properties



            geometry = {}
            geometry['type'] = "Point"
            geometry['coordinates'] = coordinates

            feature['geometry'] = geometry

            features.append(feature)
        except:
            pass

    return features