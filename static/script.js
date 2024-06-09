document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');
    const messageBox = document.getElementById('message-box');


    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(form);
        const action = formData.get('action');
        const data = {
            email: formData.get('email'),
            password: formData.get('password')
        };

        if (action === 'login') {
            alert('login');
            handleLogin(data);
        } else if (action === 'register') {
            alert('register');
            window.location.href = '/register-page';
        }
    });


    function handleLogin(data) {
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            const account_id = data.account_id;
            alert(account_id);
            if (data.message) {
                window.location.href = '/user/' + account_id; /*${form.email}*/
            } else if (data.error) {
                alert(data.message);
                messageBox.innerText = data.error;
            }
        })
        .catch(error => console.error('Ошибка при логине:', error));
    }


});
