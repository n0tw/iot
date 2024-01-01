const axios = require('axios');

const deleteEntity = async (entityId) => {
  try {
    const response = await axios.delete(`http://150.140.186.118:1026/v2/entities/${entityId}`);
    console.log('Entity deleted successfully:', response.data);
  } catch (error) {
    console.error('Error deleting entity:', error.message);
  }
};

// Usage
deleteEntity('bus123');
deleteEntity('station123');
