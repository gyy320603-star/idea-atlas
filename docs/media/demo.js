const copyButton = document.querySelector('.copy-prompt');
const installPrompt = document.querySelector('#install-prompt');
const copyStatus = document.querySelector('.copy-status');

copyButton.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(installPrompt.value);
    copyButton.textContent = copyButton.dataset.success;
    copyStatus.textContent = copyStatus.dataset.success;
  } catch {
    installPrompt.focus();
    installPrompt.select();
    copyButton.textContent = copyButton.dataset.failure;
    copyStatus.textContent = copyStatus.dataset.failure;
  }
});
