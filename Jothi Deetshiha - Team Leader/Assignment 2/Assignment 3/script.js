function validateForm() {
    let fname = document.forms["myForm"]["fname"].value;
    let email = document.forms["myForm"]["email"].value;
    let address = document.forms["myForm"]["address"].value;
    let pass = document.forms["myForm"]["pass"].value;
    let gender = document.forms["myForm"]["gender"].value;
    if (fname == "") {
        swal("Username!", "...check username");
      return false;
    }if (email == "") {
        swal("email!", "...please enter your email");
      return false;
    }
    if (address == "") {
        swal("address!", "...please enter your address");
      return false;
    }
    if (gender == "") {
        swal("Gender", "...please choose your gender");
      return false;
    }
    if (pass == "") {
        swal("password!", "...password is empty");
      return false;
    }
    if (pass.length<8) {
        swal("password!", "...password is too short");
      return false;
    }
    if (pass.length >15) {
        swal("password!", "...password is too long");
      return false;
    }
  }