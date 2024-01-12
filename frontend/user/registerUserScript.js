var details_Hospital;

async function showHospitals(){
    const response = await axios.get("http://127.0.0.1:8000/getHospital");
    details_Hospital=response.data;
    const dropdown = document.getElementById('apiData');
    dropdown.innerHTML = '';
            const defaultOption = document.createElement('option');
            defaultOption.text = 'Select an option';
            dropdown.add(defaultOption);
            details_Hospital.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id; 
                option.text = item.hospital_name; 
                dropdown.add(option);
            });
   
}
showHospitals();
async function validateDate(){
    var fname = document.getElementById('FirstName').value;
    var lname = document.getElementById('LastName').value;
    var email = document.getElementById('Email').value;
    var phone = document.getElementById('ContactNumber').value;
    var gender = document.getElementById('gender').value;
    var addresss = document.getElementById('address').value;
    var bloodGroupp = document.getElementById('bloodgroup').value;
    var hospital_id=document.getElementById('apiData').value;
    var aliveStatus = document.getElementById('alive').value;
    var pass=document.getElementById('password').value;
    if (fname.trim() === '' || lname.trim() === '' || email.trim() === '' || phone.trim() === '' || gender.trim() === '' || addresss.trim() === '' || bloodGroupp.trim() === '' || hospital_id.trim() === '' || pass.trim() === '' || aliveStatus === '') {
        document.getElementById('errorMessage').innerText = '*All fields must be filled out';
    } else if (!/^\d{10}$/.test(phone)) {
        document.getElementById('errorMessage').innerText = '*Invalid phone number format';
    } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
        document.getElementById('errorMessage').innerText = '*Invalid email format';
    } else {
        
        try {
            var statusAlive;
            if(aliveStatus==="Alive")
                statusAlive=true;
            else
                statusAlive=false;
            const spinner = document.getElementById("spinner");
            spinner.classList.toggle("d-none");
            const dataToSent = {
                first_name: fname,
                last_name: lname,
                email: email,
                mobile: phone,
                password: pass,
                address: addresss,
                bloodGroup: bloodGroupp,
                hospital_id: hospital_id,
                isAlive:statusAlive
            }
            const response = await axios.post("http://127.0.0.1:8000/registerUser",dataToSent)
            const data=response.data;
            console.log(data)
            // showNotification();
            window.alert("User is registered");
            // window.location.href = "userLogin.html";

            
          } catch (err) {
            window.alert("Some error occurred");
            console.error('Error:',err);
          }
          finally{
            spinner.classList.toggle("d-none");
          }
    }
}
//  function showNotification() {
//      Swal.fire({
//       icon: 'success',
//       text: 'Registered Successfully',
//       timer: 20000, 
//       showConfirmButton: false, 
//     }).then(() => {
//      
//       
//     });
// }