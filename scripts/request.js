#!/usr/bin/env node

//const fetch = require("node-fetch");
const fetch = require("cross-fetch");
var fs = require('fs');

var args = process.argv.slice(2);
fs.readFile(args[0], 'utf8', function(err, code) {
  if (err) {
    return console.log(err);
  }
	code = fixedEncodeURIComponent(code);

  getData(`https://localhost:5000/execute?code=${code}`)
    .then(data => console.log(data)) // JSON from `response.json()` call
    .catch(error => console.error(error))
});

function getData(url, data) {
  // Default options are marked with *
  return fetch(url, {
    body: JSON.stringify(data), // must match 'Content-Type' header
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, same-origin, *omit
    headers: {
      'content-type': 'application/json;charset=UTF-8'
    },
    method: 'GET', // *GET, POST, PUT, DELETE, etc.
    //mode: 'cors', // no-cors, cors, *same-origin
    //redirect: 'follow', // manual, *follow, error
    //referrer: 'no-referrer', // *client, no-referrer
  })
  .then(response => response.json()) // 輸出成 json
}

function fixedEncodeURIComponent(str) {
  return encodeURIComponent(str).replace(/[!'()*]/g, function(c) {
    return '%' + c.charCodeAt(0).toString(16);
  });
}



