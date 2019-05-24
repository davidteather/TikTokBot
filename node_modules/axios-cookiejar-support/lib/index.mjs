import requestInterceptor from './interceptors/request';
import responseInterceptor from './interceptors/response';
import { COOKIEJAR_SUPPORTED } from './symbol';

function axiosCookieJarSupport(instance) {
  // Wrap instance when creating new instance.
  if (instance.create) {
    const createInstance = instance.create.bind(instance);
    instance.create = function create(defaultConfig) {
      const newInstance = createInstance(defaultConfig);
      return axiosCookieJarSupport(newInstance);
    };
  }

  // Skip if already wrapped
  if (instance[COOKIEJAR_SUPPORTED]) {
    return instance;
  }
  Object.defineProperty(instance, COOKIEJAR_SUPPORTED, {
    configurable: false,
    enumerable: false,
    writable: false,
    value: true,
  });

  // Prevent utils.merge for defaults.jar
  Object.defineProperty(instance.defaults, 'jar', {
    configurable: false,
    enumerable: false,
    writable: true,
    value: instance.defaults.jar,
  });

  // Add interceptors
  instance.interceptors.request.use(res => requestInterceptor(res, instance));
  instance.interceptors.response.use(res => responseInterceptor(res, instance));

  return instance;
}

export default axiosCookieJarSupport;
