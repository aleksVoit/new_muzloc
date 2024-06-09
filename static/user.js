document.addEventListener('DOMContentLoaded', function () {
    alert('user.js')
    const messageBox = document.getElementById('message-box');
    const updateButton = document.getElementById('to_edit_profile');
    const form = document.getElementById('edit_profile_button');

    fetch(`/user/${account_id}`)
                .then(response => response.json())
                .then(data => {
                    const profileInfo = document.getElementById('profile-info');
                    profileInfo.innerHTML = `
                        <img src="${data.photo}" alt="Фото пользователя">
                        <h2>${data.name}</h2>
                        <p>${data.about}</p>
                    `;
                    // Добавление видео и музыкальных записей
                    const videoSection = document.createElement('section');
                    videoSection.innerHTML = '<h3>Видео</h3>';
                    data.videos.forEach(video => {
                        const videoElement = document.createElement('video');
                        videoElement.src = video;
                        videoElement.controls = true;
                        videoSection.appendChild(videoElement);
                    });
                    profileInfo.appendChild(videoSection);

                    const musicSection = document.createElement('section');
                    musicSection.innerHTML = '<h3>Музыкальные записи</h3>';
                    data.music.forEach(track => {
                        const audioElement = document.createElement('audio');
                        audioElement.src = track;
                        audioElement.controls = true;
                        musicSection.appendChild(audioElement);
                    });
                    profileInfo.appendChild(musicSection);
                })
                .catch(error => console.error('Ошибка:', error));


    if (updateButton) {
        updateButton.addEventListener('click', function(event) {
            // Добавьте вашу логику для обработки нажатия кнопки
            event.preventDefault();
            alert('user.js update button');
            // Например, переход на страницу редактирования профиля
            //const accountId = '{{ account_id }}'; // Получение account_id из шаблона
            window.location.href = '/update-profile-page/' + account_id;
        });
    }


});