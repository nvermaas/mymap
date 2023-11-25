import geocoder

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

        # geolocate the ip
        ip = self.kwargs['ip']
        g = geocoder.ip(ip)
        coordinates = []
        coordinates.append(g.latlng[1])
        coordinates.append(g.latlng[0])

        context['address'] = g.address
        context['country'] = g.country
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
