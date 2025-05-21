const logger = require('./logger');

/**
 * Logs in to Naukri
 * @param {Object} page Puppeteer page object
 * @param {string} email Naukri email
 * @param {string} password Naukri password
 */
async function login(page, email, password) {
  logger.info('Navigating to Naukri login page');
  await page.goto('https://www.naukri.com/nlogin/login', { waitUntil: 'networkidle2' });
  
  // Check if already logged in
  const alreadyLoggedIn = await page.evaluate(() => {
    return window.location.href.includes('mnjuser/homepage');
  });
  
  if (alreadyLoggedIn) {
    logger.info('Already logged in');
    return;
  }
  
  // Fill in email
  logger.info('Entering login credentials');
  await page.waitForSelector('#usernameField');
  await page.type('#usernameField', email);
  
  // Fill in password
  await page.waitForSelector('#passwordField');
  await page.type('#passwordField', password);
  
  // Click login button
  await page.waitForSelector('button[type="submit"]');
  await page.click('button[type="submit"]');
  
  // Wait for successful login (redirect to homepage)
  logger.info('Waiting for login to complete');
  await page.waitForNavigation({ timeout: 60000 });
  
  // Verify login was successful
  const currentUrl = page.url();
  if (!currentUrl.includes('mnjuser/homepage')) {
    // If there's an error message element visible, get the text
    let errorMessage = 'Unknown login error';
    try {
      errorMessage = await page.$eval('.error-message', el => el.textContent);
    } catch (e) {
      // Element might not exist, so ignore this error
    }
    
    throw new Error(`Login failed. Current URL: ${currentUrl}. ${errorMessage}`);
  }
  
  logger.info('Login successful');
}

module.exports = { login };