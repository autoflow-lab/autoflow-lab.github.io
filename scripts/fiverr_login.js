const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: false, args: ['--start-maximized'] });
  const ctx = await browser.newContext({ viewport: null });
  const page = await ctx.newPage();
  
  await page.goto('https://www.fiverr.com/login');
  console.log('BROWSER OFFEN - bitte via Google einloggen!');
  
  // Warte bis Login fertig
  try {
    await page.waitForFunction(() => !window.location.href.includes('/login'), { timeout: 180000 });
  } catch(e) {}
  
  await page.waitForTimeout(4000);
  
  const cookies = await ctx.cookies();
  fs.writeFileSync('C:\\clawy\\fiverr_cookies.json', JSON.stringify(cookies, null, 2));
  console.log('DONE: ' + cookies.length + ' cookies saved');
  
  await browser.close();
})();
