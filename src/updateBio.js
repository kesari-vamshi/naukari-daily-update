const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const logger = require('./logger');
const { login } = require('./auth');

// Path to the state file
const STATE_FILE_PATH = path.join(__dirname, '..', 'state.json');

/**
 * Reads the current state from the state file
 * @returns {Object} The current state
 */
function readState() {
  try {
    if (fs.existsSync(STATE_FILE_PATH)) {
      const data = fs.readFileSync(STATE_FILE_PATH, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    logger.error(`Error reading state file: ${error.message}`);
  }
  
  // Default state if file doesn't exist or can't be read
  return { lastUpdate: null, spacesAdded: false };
}

/**
 * Writes the current state to the state file
 * @param {Object} state The current state
 */
function writeState(state) {
  try {
    fs.writeFileSync(STATE_FILE_PATH, JSON.stringify(state, null, 2));
  } catch (error) {
    logger.error(`Error writing state file: ${error.message}`);
  }
}

/**
 * Updates the bio by adding or removing spaces
 * @param {string} currentBio The current bio text
 * @param {boolean} addSpaces Whether to add spaces or remove them
 * @returns {string} The updated bio text
 */
function modifyBio(currentBio, addSpaces) {
  if (addSpaces) {
    // Add a space between each character
    return currentBio.split('').join(' ');
  } else {
    // Remove all spaces
    return currentBio.replace(/\s+/g, '');
  }
}

/**
 * Main function to update the Naukri bio
 */
async function updateNaukriBio() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    
    // Set a reasonable viewport
    await page.setViewport({ width: 1280, height: 800 });
    
    // Login to Naukri
    await login(page, process.env.NAUKRI_EMAIL, process.env.NAUKRI_PASSWORD);
    
    // Navigate to profile page
    logger.info('Navigating to profile page');
    await page.goto('https://www.naukri.com/mnjuser/profile', { waitUntil: 'networkidle2' });
    
    // Click on the "Edit Profile Summary" button
    logger.info('Opening profile summary editor');
    await page.waitForSelector('a[href="#profileSummary"]');
    await page.click('a[href="#profileSummary"]');
    
    // Wait for the editor to appear
    await page.waitForSelector('.summaryEditor');
    
    // Get the current bio text
    const currentBio = await page.$eval('.summaryEditor', el => el.textContent);
    
    // Read the current state
    const state = readState();
    
    // Determine whether to add or remove spaces
    const addSpaces = !state.spacesAdded;
    
    // Update the bio
    const newBio = modifyBio(currentBio, addSpaces);
    
    // Clear the current bio and type the new one
    logger.info(`Updating bio - ${addSpaces ? 'adding' : 'removing'} spaces`);
    await page.$eval('.summaryEditor', el => el.textContent = '');
    await page.type('.summaryEditor', newBio);
    
    // Click the Save button
    await page.click('button.saveBtn');
    
    // Wait for save confirmation
    await page.waitForSelector('.toast-message', { timeout: 10000 });
    
    // Update the state
    state.lastUpdate = new Date().toISOString();
    state.spacesAdded = addSpaces;
    writeState(state);
    
    logger.info(`Bio updated successfully. Spaces ${addSpaces ? 'added' : 'removed'}.`);
  } catch (error) {
    logger.error(`Error in updateNaukriBio: ${error.message}`);
    throw error;
  } finally {
    await browser.close();
  }
}

module.exports = { updateNaukriBio };