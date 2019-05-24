"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _toughCookie = _interopRequireDefault(require("tough-cookie"));

var _pify = _interopRequireDefault(require("pify"));

var _isAbsoluteURL = _interopRequireDefault(require("axios/lib/helpers/isAbsoluteURL"));

var _combineURLs = _interopRequireDefault(require("axios/lib/helpers/combineURLs"));

var _symbol = require("../symbol");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function requestInterceptor(config, instance) {
  return new Promise(function ($return, $error) {
    let local;
    local = config[_symbol.COOKIEJAR_SUPPORT_LOCAL] || {};
    config[_symbol.COOKIEJAR_SUPPORT_LOCAL] = local;
    local.backupOptions = local.backupOptions || {};

    if (instance.defaults.jar === true) {
      instance.defaults.jar = new _toughCookie.default.CookieJar();
    }

    if (!local.jar) {
      if (config.jar === true) {
        local.jar = instance.defaults.jar || new _toughCookie.default.CookieJar();
      } else if (config.jar === false) {
        local.jar = false;
      } else {
        local.jar = config.jar || instance.defaults.jar;
      }
    } // Redirect Setup


    Object.assign(local, {
      redirectCount: isFinite(config.maxRedirects) ? config.maxRedirects : 5
    });
    Object.assign(local.backupOptions, config, local.backupOptions);
    Object.assign(config, {
      maxRedirects: 0
    });
    delete config.validateStatus; // Cookies Setup

    if (local.jar && config.withCredentials) {
      let getCookieString, requestUrl, cookieString;
      getCookieString = (0, _pify.default)(local.jar.getCookieString.bind(local.jar));
      requestUrl = config.baseURL && !(0, _isAbsoluteURL.default)(config.url) ? (0, _combineURLs.default)(config.baseURL, config.url) : config.url;
      return Promise.resolve(getCookieString(requestUrl)).then(function ($await_2) {
        try {
          cookieString = $await_2;

          if (cookieString) {
            if (config.headers) {
              let currentCookie;
              currentCookie = config.headers['Cookie'];
              config.headers['Cookie'] = [currentCookie, cookieString].filter(c => !!c).join(';\x20');
            } else {
              config.headers = {
                'Cookie': cookieString
              };
            }
          }

          return $If_1.call(this);
        } catch ($boundEx) {
          return $error($boundEx);
        }
      }.bind(this), $error);
    }

    function $If_1() {
      return $return(config);
    }

    return $If_1.call(this);
  });
}

var _default = requestInterceptor;
exports.default = _default;