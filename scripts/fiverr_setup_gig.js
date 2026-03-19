const { chromium } = require('playwright');
const fs = require('fs');

const GIG = {
  title: 'I will build n8n or Make workflow automations to save you hours every week',
  category: 'Programming & Tech',
  subcategory: 'Automation',
  tags: ['n8n', 'make automation', 'workflow automation', 'api integration', 'business automation'],
  description: `⚡ Stop doing the same task twice. I automate it — permanently.

I build custom workflow automations using n8n, Make (Integromat), or Zapier that connect your apps and run 24/7 — without you lifting a finger.

What I can automate for you:
✅ Lead capture → CRM → Email follow-up (fully automatic)
✅ New customer → Onboarding emails → Slack/Notion notifications
✅ Invoice created → Payment reminder → Accounting sync
✅ Form submission → Google Sheets → Email/WhatsApp notification
✅ Social media scheduling and cross-posting
✅ Data scraping, cleaning and syncing between apps
✅ ANY repetitive task between apps that have an API

Apps I work with:
Gmail, Outlook, HubSpot, Salesforce, Shopify, Stripe, Notion, Airtable, Google Sheets, Slack, WhatsApp Business, Telegram, WordPress, WooCommerce, Calendly, Typeform, and 300+ more.

Why me:
→ 48-hour average delivery
→ Every workflow is tested before delivery
→ You get full documentation so you understand it
→ I stay until it works perfectly — unlimited revisions on Standard/Premium

Message me BEFORE ordering — I'll confirm it's possible and give you an exact timeline. Free.`,
  faq: [
    { q: 'Do I need technical knowledge?', a: 'Not at all. You describe what you want in plain English, I handle everything technical.' },
    { q: 'What if my app is not on your list?', a: 'If it has an API or webhook, I can almost certainly integrate it. Message me to confirm — free.' },
    { q: 'What if it breaks after delivery?', a: 'All packages include a support period. I also provide documentation so you understand exactly how it works.' },
    { q: 'Can you host the automation for me?', a: 'Yes! n8n can be self-hosted on your server, or I can set it up on a cloud instance.' }
  ]
};

(async () => {
  const cookies = JSON.parse(fs.readFileSync('C:\\clawy\\fiverr_cookies.json'));
  
  const browser = await chromium.launch({ headless: false, args: ['--start-maximized'] });
  const ctx = await browser.newContext({ viewport: null });
  await ctx.addCookies(cookies);
  const page = await ctx.newPage();
  
  console.log('Opening Fiverr...');
  await page.goto('https://www.fiverr.com');
  await page.waitForTimeout(2000);
  
  // Go to create gig
  console.log('Going to create gig...');
  await page.goto('https://www.fiverr.com/users/autoflow-lab/manage_gigs');
  await page.waitForTimeout(3000);
  
  // Click "New Gig" or equivalent
  const newGigBtn = page.locator('a[href*="new_gig"], button:has-text("New Gig"), a:has-text("New Gig"), a:has-text("Create a New Gig")').first();
  if (await newGigBtn.isVisible()) {
    await newGigBtn.click();
    console.log('Clicked New Gig');
  } else {
    await page.goto('https://www.fiverr.com/gigs/new');
  }
  await page.waitForTimeout(3000);
  
  // Step 1: Overview - Title
  console.log('Filling title...');
  const titleInput = page.locator('input[placeholder*="title" i], input[name*="title" i], textarea[placeholder*="title" i]').first();
  if (await titleInput.isVisible({ timeout: 5000 })) {
    await titleInput.click();
    await titleInput.fill('');
    await titleInput.type(GIG.title, { delay: 30 });
    console.log('Title filled');
  }
  
  await page.waitForTimeout(1000);
  
  // Save screenshot of current state
  await page.screenshot({ path: 'C:\\clawy\\fiverr_step1.png', fullPage: false });
  console.log('Screenshot saved: fiverr_step1.png');
  
  // Keep browser open for manual continuation
  console.log('PAUSING - check screenshot and browser state');
  await page.waitForTimeout(30000);
  
  await browser.close();
})();
