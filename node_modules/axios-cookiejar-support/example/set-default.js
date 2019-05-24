'use strict';

const axios = require('axios').default;
const tough = require('tough-cookie');
const axiosCookieJarSupport = require('../').default;

axiosCookieJarSupport(axios);

const cookieJar = new tough.CookieJar();
axios.defaults.jar = cookieJar;
axios.defaults.withCredentials = true;

axios
  .get('https://google.com')
  .then(response => {
    const config = response.config;
    // axios.defaults.jar === config.jar
    console.log(config.jar.toJSON());
  })
  .catch(err => {
    console.error(err.stack || err);
  });
