const usernameField = document.querySelector('#usernameField')
const emailField = document.querySelector('#emailField')
const passwordField = document.querySelector('#passwordField')
const feedBackArea = document.querySelector('.invalid-feedback')
const emailFeedBackArea = document.querySelector('.emailFeedBackArea')
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput')
const showPasswordToggle = document.querySelector('.showPasswordToggle')


const handleToggleInput = (e) => {

	if (showPasswordToggle.textContent === 'Show Password'){
		showPasswordToggle.textContent = 'Hide Password'

		passwordField.setAttribute('type', 'text')
	}else{
		showPasswordToggle.textContent = 'Show Password'
		passwordField.setAttribute('type', 'password')

	}




}

showPasswordToggle.addEventListener('click',handleToggleInput)


emailField.addEventListener('keyup',(e) => {
	const emailVal = e.target.value

	emailField.classList.remove('is-invalid')
	emailFeedBackArea.style.display='none'

	if (emailVal.length > 0){
		fetch('/authentication/validate-email',{
			body: JSON.stringify({ email: emailVal }),
			method: 'POST'
		})
			.then(response => response.json())
			.then(data => {
				console.log(data)
				if (data.email_error){
					emailField.classList.add('is-invalid')
					emailFeedBackArea.style.display='block'
					emailFeedBackArea.innerHTML=`<p>${data.email_error}</p>`
				}
			})
	}
})

usernameField.addEventListener('keyup',(e)=>{
	
	console.log('typing......')

	const usernameVal = e.target.value

	usernameSuccessOutput.style.display='block'


	usernameSuccessOutput.textContent = `Checking ${usernameVal}`

	usernameField.classList.remove('is-invalid')
	feedBackArea.style.display='none'

	if (usernameVal.length > 0){
		fetch('/authentication/validate-username',{
			body: JSON.stringify({ username: usernameVal }),
			method: 'POST'
		})
			.then(response => response.json())
			.then(data => {
				console.log(data)
				usernameSuccessOutput.style.display='none'
				if (data.username_error){
					usernameField.classList.add('is-invalid')
					feedBackArea.style.display='block'
					feedBackArea.innerHTML=`<p>${data.username_error}</p>`
				}
			})
	}
})