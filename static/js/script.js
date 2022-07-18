// Initialise and load toasts on windows load
// CREDIT: Bootstrap Documentation
// URL: https://getbootstrap.com/docs/5.0/components/toasts/#usage
window.onload = (event) => {
  let toastElementList = [].slice.call(document.querySelectorAll('.toast'));
  let toastList = toastElementList.map(function (toastElement) {
    return new bootstrap.Toast(toastElement).show();
  });
};