var server_port = 65437;
var server_addr = "192.168.88.17";   // the IP address of your Raspberry PI

var speed = 30
document.getElementById("speed").innerHTML = speed;

function client(){
    const net = require('net');
    var input = document.getElementById("myName").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });
    // get the data from the server
    client.on('data', (data) => {
        if (data.includes("w")) {
            document.getElementById("greet_from_server").innerHTML = "Forward";
        } else if (data.includes("a")) {
            document.getElementById("greet_from_server").innerHTML = "Left";
        } else if (data.includes("s")) {
            document.getElementById("greet_from_server").innerHTML = "Backward";
        } else if (data.includes("d")) {
            document.getElementById("greet_from_server").innerHTML = "Right";
        } else if (data.includes("q")) {
            document.getElementById("greet_from_server").innerHTML = "Stop";
        } else if (data.includes("<")) {
            speed = speed - 1;
            document.getElementById("speed").innerHTML = speed;
        } else if (data.includes(">")) {
            speed = speed + 1;
            document.getElementById("speed").innerHTML = speed;
        } else {
            const uint8Array = new Uint8Array(data);
            const buffer = uint8Array.buffer;
            const dataView = new DataView(buffer);
            const float = dataView.getFloat32(0, false);
            document.getElementById("power").innerHTML = float;
        }
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    // Distance calculation

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

function greeting(){
    // get the element from html
    var name = document.getElementById("myName").value;
    // update the content in html
    document.getElementById("greet").innerHTML = "Hello " + name + " !";
    // send the data to the server 
    client();
    to_server(name);
}
