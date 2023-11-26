import geocoder
from markers.services import algorithms

from django.views.generic.base import (
    TemplateView,
)


class MarkersMapView(TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):

        context = (
            super().get_context_data(
                **kwargs
            )
        )

        # retrieve the IP from the url parameters
        ip = self.kwargs['ip']

        # geolocate the ip
        location = algorithms.geocode(ip)

        coordinates = []
        coordinates.append(location['latitude'])
        coordinates.append(location['longtitude'])

        context['address'] = location['address']
        context['country'] = location['country']
        context['attacker_ip']= ip

        context["markers"] = {
          "type": "FeatureCollection",
          "crs": {
            "type": "name",
            "properties": {
              "name": "EPSG:4326"
            }
          },
          "features": [
            {
              "id": 1,
              "type": "Feature",
              "properties": {
                "name": "Attacker",
                "pk": "1"
              },
              "geometry": {
                "type": "Point",
                "coordinates": coordinates
              }
            }
          ]
        }
        return context


class LatestHackerView(TemplateView):
    template_name = "latest_map.html"

    def get_context_data(self, **kwargs):

        context = (
            super().get_context_data(
                **kwargs
            )
        )

        # geolocate the ip
        timestamp, ip = algorithms.get_latest_ip()
        location = algorithms.geocode(ip)

        coordinates = []
        coordinates.append(location['latitude'])
        coordinates.append(location['longtitude'])

        context['address'] = location['address']
        context['country'] = location['country']
        context['attacker_ip']= ip
        context['timestamp'] = timestamp

        context["markers"] = {
          "type": "FeatureCollection",
          "crs": {
            "type": "name",
            "properties": {
              "name": "EPSG:4326"
            }
          },
          "features": [
            {
              "id": 1,
              "type": "Feature",
              "properties": {
                "name": ip,
                "pk": "1"
              },
              "geometry": {
                "type": "Point",
                "coordinates": coordinates
              }
            }
          ]
        }
        return context

class LatestSeriesHackerView(TemplateView):
    template_name = "latest_series_map.html"

    def get_context_data(self, **kwargs):

        context = (
            super().get_context_data(
                **kwargs
            )
        )

        # geolocate the ips
        ips = algorithms.get_latest_ips(10)

        # convert them to leaflet features
        features = algorithms.create_features(ips)

        context["markers"] = {
          "type": "FeatureCollection",
          "crs": {
            "type": "name",
            "properties": {
              "name": "EPSG:4326"
            }
          },
          "features": features
        }
        return context