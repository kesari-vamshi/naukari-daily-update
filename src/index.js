require('dotenv').config();
const { updateNaukriBio } = require('./updateBio');
const logger = require('./logger');

// AWS Lambda handler
exports.handler = async (event, context) => {
  try {
    logger.info('Starting Naukri profile update');
    await updateNaukriBio();
    logger.info('Naukri profile update completed successfully');
    
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Profile updated successfully' })
    };
  } catch (error) {
    logger.error(`Error updating Naukri profile: ${error.message}`);
    if (error.stack) {
      logger.debug(error.stack);
    }
    
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};