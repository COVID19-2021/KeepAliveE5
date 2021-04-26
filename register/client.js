const puppeteer = require("puppeteer");
const config = require("../config/app.json");

const sleep = (seconds) =>
  new Promise((resolve) => setTimeout(resolve, (seconds || 1) * 1000));

const run = (async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox"],
  });
  const page = await browser.newPage();
  await page.goto(
    `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=${config.client_id}&scope=offline_access%20User.Read&response_type=code&redirect_uri=${config.redirect_uri}`
  );

  try {
    // email
    await page.waitForSelector("input[type=email]");
    await page.type("input[type=email]", config.username);
    // next
    await sleep(1);
    await page.click('[type="submit"]');

    // password
    await page.waitForSelector("input[type=password]");
    await page.type("input[type=password]", config.password);
    // login
    await sleep(3);
    await page.click("[type=submit]");
    await page.waitForNavigation();

    // consent
    await page.waitForSelector("[type=checkbox]");
    await sleep(1);
    await page.click("[type=checkbox]");

    // accept
    await page.waitForSelector("[type=submit]");
    await page.click("[type=submit]");
    // request redirect uri
    await sleep(3);
    // await page.waitForNavigation();
  } catch (error) {
    console.error("error: ", error);
  }

  await browser.close();
})();
