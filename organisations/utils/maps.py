import requests
from django.conf import settings


def get_organisations_geojson():
    """
    Returns all verified organisations as GeoJSON for Google Maps.
    """
    from organisations.models import Organisation

    orgs = Organisation.objects.filter(
        verified=True,
        latitude__isnull=False,
        longitude__isnull=False
    )

    features = []
    for org in orgs:
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(org.longitude), float(org.latitude)]
            },
            'properties': {
                'id':       org.id,
                'name':     org.name,
                'services': org.services,
                'county':   org.county,
                'phone':    org.phone,
                'email':    org.email,
            }
        })

    return {
        'type': 'FeatureCollection',
        'features': features
    }


def get_heatmap_geojson():
    """
    Returns incident report counts per county as GeoJSON for heatmap.
    """
    from reports.models import IncidentReport
    from django.db.models import Count

    county_counts = (
        IncidentReport.objects
        .values('county')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    return list(county_counts)
