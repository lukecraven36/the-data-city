// Convenience entry screen only. Public static files are not access-protected.
(() => {
  'use strict';
  const root = document.querySelector('#review-entry');
  if (!root) return;
  const config = JSON.parse(document.querySelector('#review-access-config').content.textContent);
  const form = document.querySelector('#review-entry-form');
  const email = document.querySelector('#review-email');
  const error = document.querySelector('#review-entry-error');
  const submit = document.querySelector('#review-enter');
  const signOut = document.querySelector('#review-sign-out');
  let checking = false;
  function unlock(focus) {
    root.hidden = true;
    document.documentElement.classList.remove('review-required');
    if (focus) {
      const main = document.querySelector('#main');
      main.tabIndex = -1;
      main.focus();
    }
  }
  function lock() {
    try { sessionStorage.removeItem(config.storageKey); } catch { /* Storage can be disabled. */ }
    document.querySelectorAll('dialog[open]').forEach(dialog => dialog.close());
    document.documentElement.classList.add('review-required');
    root.hidden = false;
    root.scrollTop = 0;
    email.value = '';
    error.textContent = '';
    email.removeAttribute('aria-invalid');
    window.scrollTo(0, 0);
    email.focus();
  }
  try {
    if (config.allowedEmailHashes.includes(sessionStorage.getItem(config.storageKey))) unlock(false);
  } catch { /* Remain on the entry screen when storage is unavailable. */ }
  submit.disabled = false;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (checking) return;
    const value = email.value.trim().toLowerCase();
    email.value = value;
    error.textContent = '';
    email.removeAttribute('aria-invalid');
    if (!value || !email.validity.valid) {
      error.textContent = 'Enter a valid email address.';
      email.setAttribute('aria-invalid', 'true');
      email.focus();
      return;
    }
    checking = true;
    submit.disabled = true;
    try {
      const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
      const hash = [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
      if (!config.allowedEmailHashes.includes(hash)) {
        error.textContent = 'This email is not on the review list. Please check the address or contact Luke.';
        email.setAttribute('aria-invalid', 'true');
        email.focus();
        return;
      }
      try { sessionStorage.setItem(config.storageKey, hash); } catch { /* Current page still works. */ }
      unlock(true);
    } catch {
      error.textContent = 'The email check could not run. Open the HTTPS link in a current browser and try again.';
    } finally {
      checking = false;
      submit.disabled = false;
    }
  });
  signOut?.addEventListener('click', lock);
})();
