/** @type {import('vls').VeturConfig} */
module.exports = {
  settings: {
    "vetur.useWorkspaceDependencies": true,
    "vetur.experimental.templateInterpolationService": true,
    "vetur.validation.template": true,
    "vetur.validation.script": true,
    "vetur.validation.style": true,
    "vetur.format.enable": true,
    "vetur.format.defaultFormatter.html": "prettier",
    "vetur.format.defaultFormatter.css": "prettier",
    "vetur.format.defaultFormatter.postcss": "prettier",
    "vetur.format.defaultFormatter.scss": "prettier",
    "vetur.format.defaultFormatter.less": "prettier",
    "vetur.format.defaultFormatter.stylus": "stylus-supremacy",
    "vetur.format.defaultFormatter.js": "prettier",
    "vetur.format.defaultFormatter.ts": "prettier",
    "vetur.format.defaultFormatterOptions": {
      "prettier": {
        "singleQuote": true,
        "semi": false
      }
    }
  },
  projects: [
    './packages/repo2',
    {
      root: './packages/repo1',
      package: './package.json',
      jsconfig: './jsconfig.json',
      tsconfig: './tsconfig.json', // Добавлено для TypeScript проектов
      snippetFolder: './.vscode/vetur/snippets',
      globalComponents: [
        './src/components/**/*.vue'
      ]
    }
  ]
}