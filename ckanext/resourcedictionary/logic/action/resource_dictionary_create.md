# Create/Update resource data dictionary

Creates new or updates existing data dictionary for a given CKAN resource.

*Note:* For resources that don't have datastore records, the data dictionary can be edited in every way (adding/removing/editing fields) and even completely deleted.
For resources that contain datastore records editing data dictionary is limited only to the info properties of a field.

**URL** : `/api/v3/action/resource_dictionary_create`

**Method** : `POST`

**Auth required** : YES, [details](https://docs.ckan.org/en/2.9/api/#authentication-and-api-tokens).


**Data example**

```json
{
    "resource_id":"7a50a2c8-7af5-46bc-b87d-272978c58a78 - REQUIRED",
    "fields": [{
            "id": "name - REQUIRED",
            "type": "text - REQUIRED",
            "info": {
                "label": "",
                "notes": "",
                "type_override": ""
            }
        },{
            "id": "time",
            "type": "time",
            "info": {
                "label": "Time Label",
                "notes": "This is the time field",
                "type_override": "timestamp"
            }
        }
        
    ]
}
```

# Delete resource data dictionary

**URL** : `/api/v3/action/resource_dictionary_create`

**Method** : `POST`

**Auth required** : YES, [details](https://docs.ckan.org/en/2.9/api/#authentication-and-api-tokens).

**Data example**

```json
{
    "resource_id":"7a50a2c8-7af5-46bc-b87d-272978c58a78 - REQUIRED",
    "fields": []
}
```

## Success Response on create/update

**Condition** : If everything is OK.

**Code** : `200 OK`

**Content example**

```json
{
    "help": "http://localhost:5000/api/3/action/help_show?name=resource_dictionary_create",
    "success": true,
    "result": {
        "resource_id": "7a50a2c8-7af5-46bc-b87d-272978c58a78",
        "fields": [
            {
                "id": "name",
                "info": {
                    "label": "",
                    "notes": "",
                    "type_override": ""
                },
                "type": "text"
            },
            {
                "id": "time",
                "info": {
                    "label": "Time Label",
                    "notes": "This is the time field",
                    "type_override": "timestamp"
                },
                "type": "time"
            }
        ],
        "method": "insert"
    }
}
```

## Error Responses

**Condition** : If resource_id is missing.

**Code** : `409 CONFLICT`

**Content example**

```json
{
    "help": "http://localhost:5000/api/3/action/help_show?name=resource_dictionary_create",
    "error": {
        "resource_id": [
            "Missing value"
        ],
        "__type": "Validation Error"
    },
    "success": false
}
```

### Or

**Condition** : If fields id or type missing.

**Code** : `409 CONFLICT`

**Content example**

```json
{
    "help": "http://localhost:5000/api/3/action/help_show?name=resource_dictionary_create",
    "error": {
        "fields": [
            {
                "id": "Missing value"
            }
        ],
        "__type": "Validation Error"
    },
    "success": false
}
```
