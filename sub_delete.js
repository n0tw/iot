const fetch = require('node-fetch');

const subscriptionIdToDelete = '6599daaac7608592129ea08e';
const contextBrokerUrl = `http://150.140.186.118:1026/v2/subscriptions/${subscriptionIdToDelete}`;

fetch(contextBrokerUrl, {
    method: 'DELETE',
})
    .then(response => {
        console.log('Response Status:', response.status);

        if (response.ok) {
            console.log(`Subscription ${subscriptionIdToDelete} deleted successfully`);
        } else {
            console.error(`Failed to delete subscription ${subscriptionIdToDelete}. Status: ${response.status}`);
        }

        return response.text(); // Log the response body for further analysis
    })
    .then(responseText => console.log('Response Body:', responseText))
    .catch(error => console.error('Error:', error));
