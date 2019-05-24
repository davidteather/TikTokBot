'use strict';

const axios = require('axios').default;
const tough = require('tough-cookie');
const axiosCookieJarSupport = require('../').default;

axiosCookieJarSupport(axios);

const cookieJar = new tough.CookieJar();

axios
  .get('https://google.com', {
    jar: cookieJar,
    withCredentials: true,
  })
  .then(response => {
    const config = response.config;
    console.log(config.jar.toJSON());
  })
  .catch(err => {
    console.error(err.stack || err);
  });
