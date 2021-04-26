const fs = require("fs");
const qs = require("qs");
const axios = require("axios");
const express = require("express");
const configFile = "../config/app.json";
const config = require(configFile);
const app = express();

app.get("/", async (req, res) => {
  res.send(req.query.code);
  console.log(req.query.code);

  const resp = await axios.post(
    "https://login.microsoftonline.com/common/oauth2/v2.0/token",
    qs.stringify({
      client_id: config.client_id,
      client_secret: config.client_secret,
      code: req.query.code,
      redirect_uri: config.redirect_uri,
      grant_type: "authorization_code",
    })
  );

  server.close(() => {
    config.refresh_token = resp.data.refresh_token;
    fs.writeFileSync(configFile, JSON.stringify(config));

    console.log(resp.data);
  });
});

const server = app.listen(config.redirect_uri.match(/\d+/)[0], () => {
  console.log(`Server app listening at ${config.redirect_uri}`);
});
