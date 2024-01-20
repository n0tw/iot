const fetch = require('node-fetch');

const entityId = 'urn:ngsi-ld:Station:Station:MNCA-STram-L02-AP-T2';
const updatedValue ="ngsi-ld:Trafficviolation:234R:0212";
const contextBrokerUrl = `http://150.140.186.118:1026/v2/entities/${entityId}/attrs`;

fetch(contextBrokerUrl, {
    method: 'PATCH', 
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        trafficViolation: {
            "type": "Relationship",
            "value": updatedValue
        }
        /* peopleCount: {
            "type": "Property",
            "value": updatedValue
        } */
    }),
})
    .then(response => {
        if (response.ok) {
            console.log(`Attribute 'peopleCount' of entity ${entityId} updated successfully`);
        } else {
            console.error(`Failed to update attribute 'peopleCount' of entity ${entityId}. Status: ${response.status}`);
        }

        return response.text();
    })
    .then(responseText => console.log('Response Body:', responseText))
    .catch(error => console.error('Error:', error));

    