def map_config(lat,lon):
    config = {
    "version": "v1",
    "config": {
        "visState": {
        "filters": [],
        "layers": [
            {
            "id": "l2kvqvp",
            "type": "point",
            "config": {
                "dataId": "AWS&ASOS",
                "label": "point",
                "color": [255, 203, 153],
                "columns": {
                "lat": "Latitude",
                "lng": "Longitude"
                },
                "isVisible":True,
                "visConfig": {
                "radius": 10,
                "opacity": 0.8,
                "colorRange": {
                    "name": "PiYG",
                    "type": "diverging",
                    "category": "ColorBrewer",
                    "colors": [
                    "#8E0152",
                    "#DD72AD",
                    "#FADDED",
                    "#E1F2CA",
                    "#80BB47",
                    "#276419"
                    ]
                }
                },
                "textLabel": [
                {
                    "color": [255, 255, 255],
                    "size": 18
                }
                ]
            },
            "visualChannels": {
                "colorField": {
                "name": "tourism_index",
                "type": "real"
                },
                "colorScale": "quantile",
                "sizeField": {
                "name": "tourism_index",
                "type": "real"
                },
                "sizeScale": "sqrt"
            }
            }
        ],
        "interactionConfig": {
            "tooltip": {
            "fieldsToShow": {
                "AWS&ASOS": [
                { "name": "Name" ,"format":None},
                { "name": "tourism_index" ,"format":None}
                ]
            },
            "enabled": True
            }
        },
        "layerBlending": "normal",
        "animationConfig": {
            "speed": 1
        }
        },
        "mapState": {
        "bearing": 0,
        "latitude": lat,
        "longitude": lon,
        "pitch": 0,
        "zoom": 9.45
        },
        "mapStyle": {
        "styleType": "dark",
        }
    }
    }

    return config