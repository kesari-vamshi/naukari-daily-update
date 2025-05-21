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

  return { lastUpdate: null, spaceAtEnd: false };
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
 * Updates the bio by adding or removing a space at the end
 * @param {string} currentBio The current bio text
 * @param {boolean} addSpace Whether to add a space at the end or remove it
 * @returns {string} The updated bio text
 */
function modifyBio(currentBio, addSpace) {
  if (addSpace) {
    return currentBio.endsWith(' ') ? currentBio : currentBio + ' ';
  } else {
    return currentBio.endsWith(' ') ? currentBio.slice(0, -1) : currentBio;
  }
}

/**
 * Main function to update the Naukri bio
 */
async function updateNaukriBio() {
  if (!process.env.NAUKRI_EMAIL || !process.env.NAUKRI_PASSWORD) {
    throw new Error('Missing NAUKRI_EMAIL or NAUKRI_PASSWORD in environment variables.');
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    // Login
    await login(page, process.env.NAUKRI_EMAIL, process.env.NAUKRI_PASSWORD);

    logger.info('Navigating to profile page');
    await page.goto('https://www.naukri.com/mnjuser/profile', { waitUntil: 'networkidle2' });

    logger.info('Opening profile summary editor');
    await page.waitForSelector('a[href="#profileSummary"]');
    await page.click('a[href="#profileSummary"]');

    await page.waitForSelector('.summaryEditor');

    // Get the current bio text
    const currentBio = await page.$eval('.summaryEditor', el => el.innerText.trim());

    const state = readState();
    const addSpace = !state.spaceAtEnd;
    const newBio = modifyBio(currentBio, addSpace);

    // Replace the bio using contenteditable-safe methods
    logger.info(`Updating bio - ${addSpace ? 'adding' : 'removing'} space at the end`);
    await page.evaluate((bio) => {
      const editor = document.querySelector('.summaryEditor');
      if (editor) {
        editor.innerText = '';
        editor.focus();
        document.execCommand('insertText', false, bio);
      }
    }, newBio);

    // Click Save button
    await page.click('button.saveBtn');

    // Wait for confirmation
    await page.waitForSelector('.toast-message', { timeout: 10000 });

    // Update state
    state.lastUpdate = new Date().toISOString();
    state.spaceAtEnd = addSpace;
    writeState(state);

    logger.info(`Bio updated successfully. Space ${addSpace ? 'added' : 'removed'} at the end.`);
  } catch (error) {
    logger.error(`Error in updateNaukriBio: ${error.message}`);
    throw error;
  } finally {
    await browser.close();
  }
}

module.exports = { updateNaukriBio };
