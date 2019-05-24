"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _url = _interopRequireDefault(require("url"));

var _settle = _interopRequireDefault(require("axios/lib/core/settle"));

var _pify = _interopRequireDefault(require("pify"));

var _isRedirect = _interopRequireDefault(require("is-redirect"));

var _symbol = require("../symbol");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function responseInterceptor(response, instance) {
  return new Promise(function ($return, $error) {
    var config, headers, statusCode, local, setCookie, setCookiePromiseList, cookies, cookie;
    config = response.config;
    headers = response.headers;
    statusCode = response.status;
    local = config[_symbol.COOKIEJAR_SUPPORT_LOCAL];

    if (!local) {
      return $return(response);
    }

    if (local.jar && headers['set-cookie']) {
      setCookie = (0, _pify.default)(local.jar.setCookie.bind(local.jar));
      setCookiePromiseList = [];

      if (Array.isArray(headers['set-cookie'])) {
        cookies = headers['set-cookie'];
        cookies.forEach(function (cookie) {
          setCookiePromiseList.push(setCookie(cookie, config.url));
        });
      } else {
        cookie = headers['set-cookie'];
        setCookiePromiseList.push(setCookie(cookie, config.url));
      }

      return Promise.resolve(Promise.all(setCookiePromiseList)).then(function ($await_2) {
        try {
          return $If_1.call(this);
        } catch ($boundEx) {
          return $error($boundEx);
        }
      }.bind(this), $error);
    } // Redirect


    function $If_1() {
      Object.assign(local.backupOptions, config, local.backupOptions);
      delete config.baseURL;
      config.url = _url.default.resolve(config.url, headers['location'] || '');
      local.redirectCount--;

      if (local.redirectCount >= 0 && (0, _isRedirect.default)(statusCode) && !!headers['location']) {
        if (response.status !== 307) {
          config.method = 'get';
        }

        config.maxRedirects = local.redirectCount;
        return $return(instance.request(config));
      } // Restore


      if (local.backupOptions) {
        Object.assign(config, local.backupOptions);
      }

      if (local.jar) {
        if (instance.defaults.jar && (!config.jar || config.jar === true)) {
          instance.defaults.jar = local.jar;
        }

        config.jar = local.jar;
      }

      delete config[_symbol.COOKIEJAR_SUPPORT_LOCAL]; // Validate

      return Promise.resolve(new Promise(function (resolve, reject) {
        (0, _settle.default)(resolve, reject, response);
      })).then(function ($await_3) {
        try {
          return $return(response);
        } catch ($boundEx) {
          return $error($boundEx);
        }
      }, $error);
    }

    return $If_1.call(this);
  });
}

var _default = responseInterceptor;
exports.default = _default;