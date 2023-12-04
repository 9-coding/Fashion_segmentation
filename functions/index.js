const functions = require('firebase-functions');
exports.helloFunction = functions.https.onRequest((request, response) => {
  functions.logger.info('Hello World!');
  const htmlString = `
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="utf-8" />
      <title>Change Title</title>
    </head>
    <body>
      <div>test</div>
      <div>test</div>
      <div>test</div>
    </body>
  </html>
  `;
  response.set('Content-Type', 'text/html');
  response.send(Buffer.from(htmlString));
});