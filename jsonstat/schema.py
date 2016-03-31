# version was introduced in version 2.0. That’s why this property can’t accept values lower than 2.00.
version = {"type": "string", "pattern": "^[0-9]+\.[0-9]+$"}
# 2012-12-27T12:25:09Z
updated = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}(T\d+:\d+:\d+Z?)?$"}

href = {"type": "string", "pattern": "^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$"}

category_unit = {"type": "object",
                 "properties": {"additionalProperties": {"type": "object",
                                                         "properties": {"label": {"type": "string"},
                                                                        "decimals": {"type": "number"},
                                                                        "type": {"type": "string"},
                                                                        "base": {"type": "string"},
                                                                        "multiplier": {"type": "number"},
                                                                        "position": {"type": "string"}}
                                                         }
                                }
                 }

category_index = {"anyOf": [{"type": "array"},
                            {"type": "object", "properties": {"additionalProperties": {"type": "number"}}}]}

category = {"type": "object", "properties": {"index": category_index,
                                             "label": {"type": "object"},
                                             "note": {"type": "array"},
                                             "unit": category_unit,
                                             "child": {"type": "object",
                                                       "properties": {"additionalProperties": {"type": "array"}}},
                                             "coordinates": {"type": "object",
                                                             "properties": {"additionalProperties": {"type": "array"}}}}
            }

dimension = {"type": "object", "properties": {"version": version,
                                              "href": href,
                                              "class": {"type": "string", "enum": ["dimension"]},
                                              "label": {"type": "string"},
                                              "note": {"type": "array"},
                                              "category": category
                                              }
             }

dataset_role = {"type": "object", "properties": {"time": {"type": "array", "items": {"type": "string"}},
                                                 "geo": {"type": "array", "items": {"type": "string"}},
                                                 "metric": {"type": "array", "items": {"type": "string"}}
                                                 }
                }

dataset_value = {
    "anyOf": [{"type": "array", "items": {"anyOf": [{"type": "number"}, {"type": "null"}, {"type": "string"}]}},
              {"type": "object", "properties": {"additionalProperties": {"type": "number"}}}]}

dataset_link = {"type": "object",
                "properties": {"additionalProperties": {"type": "array",
                                                        "items": {"type": "object",
                                                                  "properties": {"href": href,
                                                                                 "type": {"type": "string"}}}}}
                }

dataset = {"type": "object",
           "properties": {"version": version,
                          "class": {"type": "string", "enum": ["dataset"]},
                          "href": href,
                          "label": {"type": "string"},
                          "note": {"type": "array"},
                          "source": {"type": "string"},
                          "updated": updated,
                          "id": {"type": "array", "items": {"type": "string"}},
                          "size": {"type": "array", "items": {"type": "number"}},
                          "role": dataset_role,
                          "dimension": dimension,
                          "value": dataset_value,
                          "status": {"anyOf": [{"type": "string"}, {"type": "array"}, {"type": "object"}]},
                          "link": dataset_link,
                          "extension": {"type": "object"}
                          }
           }

collection = {"type": "object",
              "properties": {"version": version,
                             "class": {"type": "string", "enum": ["collection"]},
                             "href": href,
                             "label": {"type": "string"},
                             "updated": updated,
                             "link": {"type": "object",
                                      "properties": {
                                          # The items of the collection can be of any class
                                          # (datasets, dimensions, collections, bundles).
                                          "item": {"type": "array", "items": dataset}}}}
              }
