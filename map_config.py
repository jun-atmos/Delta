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
                "label": "관측 지점",
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
            },
            {
            "id": "icon_layer",
            "type": "icon",
            "config": {
                "dataId": "LOC",
                "label": "현 위치",
                "color": [0, 255, 255],
                "columns": {
                    "lat": "latitude",
                    "lng": "longitude",
                    "icon": "icon kepler.gl"
                }, 
                "isVisible":True,
                "visConfig": {
                "radius": 50,
                },
            }
            }
        ],
        "interactionConfig": {
            "tooltip": {
            "fieldsToShow": {
                "AWS&ASOS": [
                { "name": "Name" ,"format":None},
                { "name": "tourism_index" ,"format":None}
                ],
                "LOC": [
                { "name": "address" ,"format":None},
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