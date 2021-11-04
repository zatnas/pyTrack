let signupButton = sb;
signupButton.addEventListener("click", function(e) {
	e.preventDefault();

	let formdata = new FormData();
	formdata.append("username", ui.value);
	formdata.append("password", pi.value);

	let ajax = new XMLHttpRequest();
	ajax.onload = function () {
		console.log(this.response);
	}

	ajax.open("POST", "/signup", true);
	ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	ajax.send(formdata);
});

let loginButton = lb;
loginButton.addEventListener("click", function(e) {
	e.preventDefault();
	console.log("clicked login");
});
