

from django.shortcuts import render, redirect, reverse
from django.views.generic.base import (
    TemplateView,
)
from markers.services import algorithms

def redirect_with_params(view_name, params):
    return redirect(reverse(view_name) + params)

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):

        context = (
            super().get_context_data(
                **kwargs
            )
        )
        # get the period-to-check from the session
        try:
            period_to_check = self.request.session['period-to-check']
            period = self.request.session['period']
        except:
            # no period_to_check yet, set it to default (1 minute)
            period_to_check = 60
            self.request.session['period-to-check'] = period_to_check
            self.request.session['period'] = "last minute"

        # geolocate the ips
        ips = algorithms.get_latest_ips(period_to_check)

        # convert them to leaflet features
        features = algorithms.create_features(ips)
        if not features:
            features = []

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

        context["period"] = self.request.session['period']

        return context

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
        ips = algorithms.get_latest_ips(60)

        # convert them to leaflet features
        features = algorithms.create_features(ips)
        if not features:
            features = []

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

def SniffLastPeriod(request, period, seconds):

    seconds = int(seconds)
    # write the requested period to the session
    request.session['period-to-check'] = seconds
    request.session['period'] = period

    if seconds == 0:
        return redirect('/sniffers/latest')
    else:
        return redirect('/sniffers')

    #return redirect_with_params('index', period)
