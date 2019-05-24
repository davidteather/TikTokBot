"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _request = _interopRequireDefault(require("./interceptors/request"));

var _response = _interopRequireDefault(require("./interceptors/response"));

var _symbol = require("./symbol");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function axiosCookieJarSupport(instance) {
  // Wrap instance when creating new instance.
  if (instance.create) {
    const createInstance = instance.create.bind(instance);

    instance.create = function create(defaultConfig) {
      const newInstance = createInstance(defaultConfig);
      return axiosCookieJarSupport(newInstance);
    };
  } // Skip if already wrapped


  if (instance[_symbol.COOKIEJAR_SUPPORTED]) {
    return instance;
  }

  Object.defineProperty(instance, _symbol.COOKIEJAR_SUPPORTED, {
    configurable: false,
    enumerable: false,
    writable: false,
    value: true
  }); // Prevent utils.merge for defaults.jar

  Object.defineProperty(instance.defaults, 'jar', {
    configurable: false,
    enumerable: false,
    writable: true,
    value: instance.defaults.jar
  }); // Add interceptors

  instance.interceptors.request.use(res => (0, _request.default)(res, instance));
  instance.interceptors.response.use(res => (0, _response.default)(res, instance));
  return instance;
}

var _default = axiosCookieJarSupport;
exports.default = _default;