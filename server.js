// Tiny zero-dependency static server for the Media Clean landing (Railway).
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const ROOT = path.join(__dirname, 'public');
const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.ico': 'image/x-icon',
};

function siteUrl(req) {
  if (process.env.SITE_URL) return process.env.SITE_URL.replace(/\/$/, '');
  const host = req.headers['x-forwarded-host'] || req.headers.host || 'localhost';
  const proto = req.headers['x-forwarded-proto'] || 'https';
  return `${proto.split(',')[0]}://${host.split(',')[0]}`;
}

function send(res, code, body, type, extra = {}) {
  res.writeHead(code, {
    'Content-Type': type,
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    ...extra,
  });
  res.end(body);
}

http
  .createServer((req, res) => {
    const url = new URL(req.url, 'http://x');
    let p = decodeURIComponent(url.pathname);
    if (p === '/healthz') return send(res, 200, 'ok', TYPES['.txt']);
    if (p.includes('..')) return send(res, 400, 'bad request', TYPES['.txt']);
    if (p.endsWith('/')) p += 'index.html';
    let file = path.join(ROOT, p);
    if (!path.extname(file)) {
      if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
        res.writeHead(301, { Location: p + '/' });
        return res.end();
      }
      file += '.html';
    }
    fs.readFile(file, (err, data) => {
      if (err) {
        return fs.readFile(path.join(ROOT, '404.html'), (e2, d2) =>
          send(res, 404, e2 ? 'Not found' : d2.toString().split('__SITE__').join(siteUrl(req)), TYPES['.html'])
        );
      }
      const ext = path.extname(file);
      const type = TYPES[ext] || 'application/octet-stream';
      const textual = ['.html', '.xml', '.txt'].includes(ext);
      const body = textual ? data.toString().split('__SITE__').join(siteUrl(req)) : data;
      const cache = ext === '.png' || ext === '.svg' ? 'public, max-age=86400' : 'public, max-age=300';
      send(res, 200, body, type, { 'Cache-Control': cache });
    });
  })
  .listen(PORT, () => console.log('media-clean landing on :' + PORT));
