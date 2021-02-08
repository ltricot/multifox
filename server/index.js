const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const port = process.env.PORT || 3000;


io.on('connection', socket => {
	socket.on('code', msg => {
		io.sockets.emit('code', msg);
	});
});

http.listen(port, () => console.log('listening on port ' + port));
