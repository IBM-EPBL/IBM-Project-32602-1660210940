document.getElementById("NewAccount").onclick = function() {
    window.location.replace('Register.html');
}

document.getElementById("form1").onsubmit = function() {

    if(document.getElementById("userName").value){
        if(document.getElementById("password").value){
            var x = document.getElementById("password").value;
            var format = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
            var num = /[1234567890]/;
            var cap = /[ABCDEFGHIJKLMNOPQRSTUVWXYZ]/;
            if(x.length>8 && format.test(x) && num.test(x) && cap.test(x)){
                window.location.replace('UserDetails.html');
                // window.location.replace("UserDetails.html");
                return false;
            }
            else{
                Swal.fire({
                    title: 'Wrong Password\r\nPassword length greaster than 8 \r\n Must contains atleast:\r\n',
                    html: '1.One Upppercase Letter<br>2.One Number<br>3.One Symbol',
                    showClass: {
                      popup: 'animate__animated animate__fadeInDown'
                    },
                    hideClass: {
                      popup: 'animate__animated animate__fadeOutUp'
                    },
                    swalTitle: {
                        fontSize: 'medium'
                    }
                })
                document.getElementById("password").value = "";
                return false;
            }
        }
    }
    else{
        Swal.fire({
            title: 'Enter Username...',
            showClass: {
              popup: 'animate__animated animate__fadeInDown'
            },
            hideClass: {
              popup: 'animate__animated animate__fadeOutUp'
            }
        })
    }
}