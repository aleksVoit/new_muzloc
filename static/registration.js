document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('register-form');
    const messageBox = document.getElementById('message-box');
    alert('register_document')


    form.addEventListener('submit', function (event) {
        event.preventDefault();
        alert('register_submit')
        const formData = new FormData(form);
        const action = formData.get('action');
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            password: formData.get('password')
        };
        alert(data)

         if (action === 'register') {
            alert('register')
            handleRegistration(data);
        } else if (data.error) {
                messageBox.innerText = data.error;
            }
    });


    function handleRegistration(data) {
        fetch('/register_new_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                window.location.href = '/new_user_confirmation';
            } else if (data.error) {
                messageBox.innerText = data.error;
            }
        })
        .catch(error => console.error('Ошибка при логине:', error));
    }


     function handleAddFoto(data) {
        fetch('/user_add_foto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                window.location.href = '/new_user_confirmation';
            } else if (data.error) {
                messageBox.innerText = data.error;
            }
        })
        .catch(error => console.error('Ошибка при логине:', error));
    }

});