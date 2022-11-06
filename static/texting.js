//Socket code for when a new room is made
document.addEventListener('DOMContentLoaded', ()=>{
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	socket.on('connect', ()=>{
		document.getElementById('newroombutton').onclick = ()=>{
			var rname= document.getElementById('nc').value
			document.getElementById('nc').value=""
			socket.emit('nc',{'rname':rname})
		}
	});
	socket.on('newroom', data =>{
		const n = document.createElement('a')
		const m = document.createElement('p')
		n.href=`/cr/${data.room}`
		n.style.color='wheat'
		m.innerHTML=`${data.room}`
		n.className="channels"
		n.append(m)
		//console.log('hi')
		document.getElementById('loc').append(n)
	});

});

document.addEventListener('DOMContentLoaded',() =>{
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	socket.on('connect', () =>{
		document.getElementById('sendtext').onclick = ()=>{
			var text=document.getElementById('textinputfield').value;
			document.getElementById('textinputfield').value = "";
			socket.emit('sent' , {"message":text,'url':document.URL});
		}
	});
	socket.on('recieved', messages =>{
		const et=document.createElement('div');
		et.className="eachtext";
		const s=document.createElement('p');
		s.className="sender";
		const sl=document.createElement('a')
		sl.innerHTML=`${messages.sender}`;
		sl.href=`/cpm/${messages.sender}`
		s.append(sl)
		et.append(s);
		const t=document.createElement('p');
		t.className="time";
		t.innerHTML=`${messages.time}`;
		et.append(t);
		const m=document.createElement('p');
		m.className="message";
		m.innerHTML=`${messages.message}`;
		et.append(m);
		document.getElementById('alltexts').append(et);
	});
});

//change room of socket
document.addEventListener('DOMContentLoaded', ()=>{
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	socket.on('connect', ()=>{
		socket.emit('change_room_s',{'url':document.URL});
	});
	socket.on('room_changed', data =>{
	});

});