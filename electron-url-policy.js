'use strict';

const ALLOWED_EXTERNAL_PROTOCOLS = new Set(['https:', 'http:']);

/**
 * Return a normalized external URL only when its protocol is explicitly allowed.
 * Malformed URLs and host-level/custom schemes fail closed.
 *
 * @param {string} rawUrl
 * @returns {string|null}
 */
function getSafeExternalUrl(rawUrl) {
  try {
    const parsed = new URL(rawUrl);
    if (!ALLOWED_EXTERNAL_PROTOCOLS.has(parsed.protocol)) {
      return null;
    }
    return parsed.href;
  } catch {
    return null;
  }
}

module.exports = { getSafeExternalUrl };
