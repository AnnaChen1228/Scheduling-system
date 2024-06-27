function redirectToPage(page) {
    window.location.href = page;
}

/**function boss_login(event) {
    event.preventDefault();  // 阻止表單的預設提交行為

    // 獲取用戶輸入的用戶名和密碼
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // 簡單的用戶名和密碼判斷
    if (username === 'boss' && password === '1234') {
        alert('Login successful!');
        window.location.href = 'boss.html';
    } else {
        alert('Login failed. Please check your username and password.');
        window.location.href = 'boss_login.html';
    }
}

function staff_login(event) {
    event.preventDefault();  // 阻止表單的預設提交行為

    // 獲取用戶輸入的用戶名和密碼
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // 簡單的用戶名和密碼判斷
    if (username === 'staff' && password === '1234') {
        alert('Login successful!');
        window.location.href = 'staff.html';
    } else {
        alert('Login failed. Please check your username and password.');
        window.location.href = 'staff_login.html';
    }
}**/
