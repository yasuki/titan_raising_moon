// @ts-check
import { defineConfig } from '@vivliostyle/cli';

export default defineConfig({
  title: "Titan_and_Moon",
  author: "Yatsuki.Yasuki",
  language: "ja",
  theme: "@vivliostyle/theme-bunko@^2.0.1",
  browser: "chrome@145.0.7632.26",
  image: "ghcr.io/vivliostyle/cli:10.3.1",
  entry: ["manuscript.md"],
});
