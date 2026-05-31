// Flat ESLint config for the UI app.
//
// NOTE (temporary compatibility pin): `eslint` is pinned to ^9.x in
// package.json. ESLint 10 currently crashes here because the
// `eslint-plugin-react` bundled by `eslint-config-next` still calls the
// pre-10 rule-context API (`context.getFilename`), which was removed in
// ESLint 10 ("contextOrFilename.getFilename is not a function").
// Revert the pin to the latest ESLint once eslint-config-next ships a
// plugin set compatible with ESLint 10.
import nextVitals from "eslint-config-next/core-web-vitals";

const eslintConfig = [
  ...nextVitals,
];

export default eslintConfig;
