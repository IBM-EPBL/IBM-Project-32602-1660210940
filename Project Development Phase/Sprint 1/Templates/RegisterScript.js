document.getElementById("Login").onclick = function() {
    window.location.replace('Login.html');
}

document.getElementById("form1").onsubmit = function() {

    if(document.getElementById("password").value){
        var x = document.getElementById("password").value;
        var y = document.getElementById("cnfpassword").value;
        var format = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
        var num = /[1234567890]/;
        var cap = /[ABCDEFGHIJKLMNOPQRSTUVWXYZ]/;
        if(x.length>8 && format.test(x) && num.test(x) && cap.test(x)){
            if(y === x){
                // window.location.replace("UserDetails.html");
                window.location.replace('UserDetails.html');
                return false;
            }
            else{
                Swal.fire({
                    title: '"Re-enter Password Correctly"',
                    showClass: {
                      popup: 'animate__animated animate__fadeInDown'
                    },
                    hideClass: {
                      popup: 'animate__animated animate__fadeOutUp'
                    }
                })
                // alert("Re-enter Password Correctly");
                document.getElementById("cnfpassword").value = "";
                return false;
            }
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
            // alert("Wrong Password\r\nPassword length greaster than 8 and must contains atleast:\r\n1.One Upppercase Letter\r\n2.One Number\r\n3.One Symbol");
            document.getElementById("password").value = "";
            document.getElementById("cnfpassword").value = "";
            return false;
        }
    }

}