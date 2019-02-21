function login(){
	var username = document.getElementById("username");
    var pass = document.getElementById("pass");

    if (username.value == "") {         
    	alert("Please input username!");     
    } 
    else if (pass.value  == "") {         
    	alert("Please input API Key!");     
    } 
    else if(username.value == "admin" && pass.value == "123456"){         
    	window.location.href="chatbot.html";     
    } 
    else {         
    	alert("Please input the right username and key!")     
    }

}