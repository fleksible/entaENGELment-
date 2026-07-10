const { getSafeExternalUrl } = require('../../electron-url-policy');

describe('getSafeExternalUrl', () => {
  test.each([
    ['https://example.org/path', 'https://example.org/path'],
    ['http://example.org', 'http://example.org/'],
  ])('allows and normalizes %s', (input, expected) => {
    expect(getSafeExternalUrl(input)).toBe(expected);
  });

  test.each([
    'file:///etc/passwd',
    'javascript:alert(1)',
    'data:text/html,hello',
    'mailto:test@example.org',
    'custom-protocol://payload',
    'not a url',
    '',
  ])('rejects %s', (input) => {
    expect(getSafeExternalUrl(input)).toBeNull();
  });
});
