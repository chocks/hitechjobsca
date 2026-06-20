# The 2020 Webpack 1 toolchain can't build on modern Node, so we serve the
# prebuilt static assets (bundle.js + index.html + static/style/seo) directly.
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY index.html /usr/share/nginx/html/index.html
COPY bundle.js  /usr/share/nginx/html/bundle.js
COPY static     /usr/share/nginx/html/static
COPY style      /usr/share/nginx/html/style
COPY seo        /usr/share/nginx/html/seo

EXPOSE 80
