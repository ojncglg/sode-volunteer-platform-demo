const loginPanel = document.getElementById('login-panel');
const signupPanel = document.getElementById('signup-panel');
const verificationPanel = document.getElementById('verification-panel');

function show(panel) {
  [loginPanel, signupPanel, verificationPanel].forEach((item) => item.classList.add('hidden'));
  panel.classList.remove('hidden');
}

document.getElementById('show-signup').addEventListener('click', () => show(signupPanel));
document.getElementById('show-login').addEventListener('click', () => show(loginPanel));
document.getElementById('verification-back').addEventListener('click', () => show(loginPanel));

if (window.initialAuthState === 'verification') show(verificationPanel);

const toast = document.getElementById('toast');
document.querySelectorAll('[data-toast]').forEach((button) => {
  button.addEventListener('click', () => {
    toast.textContent = button.dataset.toast;
    toast.classList.add('show');
    window.setTimeout(() => toast.classList.remove('show'), 2400);
  });
});
