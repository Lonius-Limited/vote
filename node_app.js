var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);
//var cookie = require('cookie');
//var fs = require('fs');
//var path = require('path');
//var request = require('superagent');
var { get_conf, get_redis_subscriber } = require('../../apps/frappe/node_utils');

const log = console.log; // eslint-disable-line

var conf = get_conf();

// var subscriber = redis.createClient(conf.redis_socketio || conf.redis_async_broker_port);
// alternatively one can try:
var subscriber = get_redis_subscriber();

// serve socketio
server.listen(15000, function () {
	log('listening on *:', 15000); //eslint-disable-line
});

// on socket connection
io.on('connection', function (socket) {
    log('User connected');
});

subscriber.on("message", function (channel, message) {
    message = JSON.parse(message);
    log("The Message:", message, channel)
    if (message.event == "election") {
        log("Got the Message:", message, channel)
        io.emit(message.event, message.message);
    }
});