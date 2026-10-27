// Flat ESLint config for the UI app.
//
// eslint-config-next 16.4.2 adapts legacy React/import rule contexts for
// ESLint 10. Keep this preset: direct, unwrapped plugin use has a different
// compatibility boundary. The root Node engine range matches ESLint 10.
import nextVitals from "eslint-config-next/core-web-vitals";

const eslintConfig = [
  ...nextVitals,
];

export default eslintConfig;
