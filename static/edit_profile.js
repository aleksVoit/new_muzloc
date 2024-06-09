document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('profile-form');
    const messageBox = document.getElementById('message-box');
/*    const username = {{ username }};
    const account_id = {{ account_id }};*/
    alert('edit_profile js');
    /*alert('user>>>: ', username, account_id)*/


    form.addEventListener('submit', function (event) {
            event.preventDefault();
            alert('update_get');
            const formData = new FormData(form);
            const action = formData.get('action');
            const data = {
                birthday: formData.get('birthday'),
                bio: formData.get('bio'),
                location: formData.get('location'),
                photo: formData.get('photo'),
                video: formData.get('video'),
                music: formData.get('music'),
                post: formData.get('post'),
            };
            alert(data)

             if (action === 'update') {
                alert('update check if');
                handleProfileUpdate(data);
            } else if (data.error) {
                    messageBox.innerText = data.error;
                }
        });


        function handleProfileUpdate(data) {
            alert('handleProfileUpdate');
            fetch('/update_profile/' + account_id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                alert('handle profile update in if')
                if (data.message) {
                    window.location.href = '/user/' + account_id;
                } else if (data.error) {
                    messageBox.innerText = data.error;
                }
            })
            .catch(error => console.error('Ошибка при логине:', error));
        }

});
