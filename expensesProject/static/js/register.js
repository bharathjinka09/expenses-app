const usernameField = document.querySelector('#usernameField')

usernameField.addEventListener('keyup',(e)=>{
	
	console.log('typing......')

	const usernameVal = e.target.value

	if (usernameVal.length > 0){
		fetch('/authentication/validate-username',{
			body: JSON.stringify({ username: usernameVal }),
			method: 'POST'
		})
			.then(response => response.json())
			.then(data => {
				console.log(data)
			})
	}
})